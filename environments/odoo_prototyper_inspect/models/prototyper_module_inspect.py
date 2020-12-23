# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import models, api
import odoo.tools as tools
import ast
import os
import inspect
from collections import OrderedDict
from odoo.modules.migration import load_script
from odoo.tools import pycompat


class PrototyperModuleInspect(models.AbstractModel):
    _name = 'prototyper.module.inspect'
    _description = '模块解析'

    @api.model
    def parse_module_source(self, module_path):
        result = OrderedDict({
            'module_name': module_path.split(os.path.sep)[-1],
        })
        model_files = self.get_module_files(module_path) or []

        for model_file in model_files:
            result_file = result.setdefault(model_file, {})
            try:
                model_file_object = None
                file_name, ext = os.path.splitext(os.path.basename(model_file))
                fullmodel_file = '%s%s%s' % (module_path.split(os.path.sep)[-1], os.path.sep, model_file)
                full_model_file = '%s%s%s' % (module_path, os.path.sep, model_file)
                model_file_object = load_script(fullmodel_file, file_name + ext)
                if file_name == '__manifest__' or file_name == '__openerp__':
                    # 读取文件内容
                    f = tools.file_open(full_model_file, mode='rb')
                    try:
                        result.update(ast.literal_eval(pycompat.to_text(f.read())))
                    finally:
                        f.close()
                    continue

                result_class = self.with_context(pathfile=full_model_file)._parse_model(model_file_object, module_path)
                result_file.update({'class': result_class})
                result_function = self._parse_function(model_file_object)
                result_file.update({'function': result_function})
            except:
                raise
            finally:
                if model_file_object:
                    del model_file_object
        return result

    @api.model
    def get_module_files(self, path, dir='.'):
        if not path:
            return False
        dir = os.path.normpath(dir)
        if dir == '.':
            dir = ''
        if dir.startswith('..') or (dir and dir[0] == os.path.sep):
            raise Exception('Cannot access file outside the module')
        files = tools.osutil.listdir(path, True)
        files.sort()
        tree = []
        for f in files:
            if not f.startswith(dir):
                continue
            # 忽略的目录
            pos = f.find(os.path.sep)
            if pos > 0 and f[0: pos] in ['data', 'demo', 'doc', 'i18n', 'static', 'tests']:
                continue
            if not f.endswith('.py'):
                continue
            if f.endswith('__init__.py'):
                continue
            tree.append(f)
        return tree

    @api.model
    def _parse_model_file(self, model_file_object):
        result = OrderedDict({})
        for model_name, model_object in inspect.getmembers(model_file_object, inspect.isclass):
            # 通过import语句导入的
            if model_object.__module__ != model_file_object.__name__:
                continue
            model = self._parse_model(model_object)
            result.update(model)
        return result

    @api.model
    def _parse_model(self, model_file_object, module_path):
        result = OrderedDict({})
        for model_name, model_object in inspect.getmembers(model_file_object, inspect.isclass):
            # 通过import语句导入的
            if model_object.__module__ != model_file_object.__name__:
                continue

            class_name, attributes = self._parse_model_attributes(model_object)
            fields = self._parse_model_fields(model_object)
            methods = self._parse_model_methods(model_object)

            files = tools.osutil.listdir(module_path + '/doc/image', True)
            model_name = attributes.get('_name', attributes.get('_inherit')).replace('.', '_')

            result.update({
                class_name: {
                    'attributes': attributes,
                    'fields': fields,
                    'methods': methods,
                    'images': [x for x in files if x[:x.rindex('_')] == model_name]
                }
            })
        return result

    @api.model
    def _parse_model_attributes(self, model_object):
        def get_attr(attr):
            if hasattr(model_object, attr):
                return getattr(model_object, attr)
            return None

        class_name = model_object.__name__
        attributes = OrderedDict({
            x: get_attr(x) for x in [
                '_name', '_inherit', '_inherits', '_table', '_order',
                '_auto', '_rec_name', '_sql_constraints', '_transient', '_abstract',
                '_description',
            ]
            if get_attr(x)
        })
        # 模型注释
        attributes['doc'] = model_object.__doc__ or ''

        if not attributes.get('_name'):
            _inherit = attributes.get('_inherit')
            if _inherit and isinstance(_inherit, list):
                _inherit = _inherit[0]
            attributes['_name'] = _inherit or class_name

        return class_name, attributes

    # 模型中定义的字段
    @api.model
    def _parse_model_fields(self, class_object):
        result = OrderedDict({})
        model_fields = inspect.getmembers(
            class_object, lambda x: hasattr(x, 'type'))

        for field_name, field in model_fields:
            field_attr = result.setdefault(field_name, {'name': field_name, 'type': field.type})
            for attr_name, value in field.args.items():
                if attr_name in ['_module', '_sequence']:
                    continue
                if callable(value):
                    if value.__name__ == '<lambda>':
                        value = inspect.getsource(value).strip()
                    else:
                        # TODO _digits
                        value = value.__name__
                field_attr.update({attr_name: value})
        return result

    @api.model
    def _parse_model_methods(self, class_object):
        """模型中定义的方法"""
        result = OrderedDict({})
        pathfile = self._context.get('pathfile', '').lower()
        # class_methods = inspect.getmembers(
        #     class_object,
        #     lambda x: (inspect.ismethod(x) or inspect.isfunction(x)) and
        #               inspect.getabsfile(
        #                   getattr(x, 'original_func', None) or getattr(x, '__wrapped__', None) or x
        #               ) == pathfile)
        class_methods = [
            x for x in inspect.getmembers(class_object) if
            (inspect.ismethod(x[1]) or inspect.isfunction(x[1])) and
            inspect.getabsfile(
                getattr(x[1], 'original_func', None) or getattr(x[1], '__wrapped__', None) or
                getattr(x[1], '_orig', None) or x[1]) == pathfile
        ]

        for method_name, method in class_methods:
            # TODO 方法带装饰器时, 取到的是装饰器方法的代码
            result.update({
                method_name: {
                    'name': method_name,
                    'code': inspect.getsource(
                        method.original_func if hasattr(method, 'original_func') else method),
                    'doc': inspect.getdoc(method.original_func if hasattr(method, 'original_func') else method),
                }
            })
        return result

    @api.model
    def _parse_function(self, model_file_obj):
        """python文件中定义的函数"""
        result = OrderedDict({})
        for func_name, func_object in inspect.getmembers(model_file_obj, inspect.isfunction):
            # 用import语句导入的方法
            if func_object.__module__ != model_file_obj.__name__:
                continue

            # 方法的代码
            code = inspect.getsource(func_object)
            result.update({func_name: code})

        return result
