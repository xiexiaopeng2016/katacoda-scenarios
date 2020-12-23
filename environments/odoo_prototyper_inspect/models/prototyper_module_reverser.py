# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import models, fields, api
import odoo
from odoo.tools import pycompat
from odoo.addons.odoo_prototyper_inspect.models.prototyper_icon import get_random_icon
import logging
import platform
import os

_logger = logging.getLogger(__name__)


class PrototyperModuleReverser(models.AbstractModel):
    _name = 'prototyper.module.reverser'
    _description = '模块逆向'

    @api.model
    def action_module_reverser(self, module_path, project_id):
        if module_path.endswith('addons/'):
            # 没有指定模块
            return

        self.project_id = project_id
        result = self.env['prototyper.module.inspect'].parse_module_source(module_path)

        if platform.system() == 'Windows':
            pofile = module_path + '\\i18n\\zh_CN.po'
        else:
            pofile = module_path + '/i18n/zh_CN.po'

        translate_obj = self.env['prototyper.translate']
        translate_obj.trans_load(pofile, 'zh_CN', module_name='account')
        self._module_id = self._reverser_prototyper_module(result)
        menu_seq = 0
        for file_name, content in result.items():
            if not isinstance(content, dict):
                continue

            _logger.info('开始处理文件 %s', file_name)

            menu_name = file_name.replace('.py', '')
            menu_seq += 10
            parent_menu_id = self._create_model_parent_menu(
                self._module_id, menu_name, menu_seq).id

            modeles = content.get('class', {})
            functions = content.get('function', {})

            self._reverser_prototyper_model(modeles, self._module_id, parent_menu_id)
            self._reverser_prototyper_function(functions, self._module_id, parent_menu_id)
        return self._module_id

    @api.model
    def _reverser_prototyper_module(self, module_data):
        module_obj = self.env['prototyper.ir.module.module.doc']
        module = module_obj.search(
            [
                ('project_id', '=', self.project_id),
                ('name', '=', module_data.get('module_name'))], limit=1)

        values = {
            'project_id': self.project_id,
            'name': module_data.get('module_name'),
            'shortdesc': module_data.get('name'),
            'note': module_data.get('summary'),
            'author': module_data.get('author'),
            'depends': module_data.get('depends'),
            'website': module_data.get('website'),
            'sequence': module_data.get('sequence'),
        }
        if not module:
            module = self.env['prototyper.ir.module.module.doc'].create(values)
        else:
            module.write(values)

        return module

    @api.model
    def _reverser_prototyper_model(self, modeles, module_id, parent_menu_id):
        for class_name, model in modeles.items():
            attributes = model.get('attributes', {})
            model_type = 'm'
            if not attributes:
                model_type = 'c'
            else:
                if attributes.get('_transient', False):
                    model_type = 't'
                elif attributes.get('_abstract', False):
                    model_type = 'a'

            translate_obj = self.env['prototyper.translate']
            _name = attributes.get('_name', '')
            _inherit = attributes.get('_inherit', '')

            _description = attributes.get('_description', '')
            if not _description:
                _description = self.env['ir.model'].search([('model', '=', _name or _inherit)], limit=1).name

            if _description:
                _description = translate_obj.translate(
                    imd_name='model_%s' % _name.replace('.', '_'),
                    name='ir.model,name',
                    src=_description,
                    type='model')
            # if _description.encode( 'UTF-8' ).isalpha():
            #     # 没有翻译
            #     _description = self.env['ir.translation'].search([
            #         ('src', '=', _description), ('lang', '=', 'zh_CN'),
            #         ('name', '=', 'ir.model,name'),
            #         ('value', '!=', False)
            #     ],limit=1).value or _description

            _logger.info('开始处理模型 %s, 字段 %s, 方法 %s.', _name,
                         len(model.get('fields', {})), len(model.get('methods', {})))

            model_obj = self.env['prototyper.ir.model.doc']
            record = model_obj.search(
                [('module_id', '=', module_id.id), ('model', '=', _name),
                 ('class_name', 'in', [class_name, False])], limit=1)

            values = {
                'class_name': class_name,
                'name': _description,
                'model': _name,
                'inherit': _inherit,
                'inherits': attributes.get('_inherits', ''),
                'is_inherit': not not (attributes.get('_inherit', '') or attributes.get('_inherits', '')),
                'order_field': attributes.get('_order', 'id'),
                'rec_name': attributes.get('_rec_name', ''),
                'create_auto': attributes.get('_auto', True),
                'module_id': module_id.id,
                'model_type': model_type,
                'note': attributes.get('doc'),
                'image_ids': [(5, 0, 0)] + [
                    (0, 0, {'url': '../doc/image/%s' % x}) for x in model.get('images', [])
                ]
            }

            if not record:
                record = model_obj.with_context(parent_menu_id=parent_menu_id).create(values)
            else:
                record.write(values)

            self._reverser_prototyper_model_fields(model.get('fields', {}), record)
            self._reverser_prototyper_method(model.get('methods', {}), record)

    @api.model
    def _reverser_prototyper_model_fields(self, fieldes, model_id=False):
        translate_obj = self.env['prototyper.translate']
        i = 0
        for field_name, field in fieldes.items():
            i += 1

            fields_obj = self.env['prototyper.ir.model.fields.doc']
            record = fields_obj.search(
                [('model_id', '=', model_id.id), ('name', '=', field_name)], limit=1)

            values = {
                'model_id': model_id.id,
                'name': field_name,
                'field_description': translate_obj.translate(
                    imd_name='field_%s__%s' % (model_id.model.replace('.', '_'), field_name),
                    name='ir.model.fields,field_description',
                    src=field.get('string'),
                    type='model') or '',
                'help': translate_obj.translate(
                    imd_name='field_%s__%s' % (model_id.model.replace('.', '_'), field_name),
                    name='ir.model.fields,help',
                    src=field.get('help'),
                    type='model'),
                'ttype': field.get('type'),
                'selection': self._translate_selection(
                    model_id.model, field, field_name, attr='selection'),
                'selection_add': self._translate_selection(
                    model_id.model, field, field_name, attr='selection_add'),
                'required': field.get('required', False),
                'readonly': field.get('readonly', False),
                'index': field.get('index', False),
                'translate': field.get('translate', False),
                'track_visibility': field.get('track_visibility'),
                'size': field.get('size'),
                'digits': field.get('digits'),
                'groups': field.get('groups'),
                'comodel_name': field.get('comodel_name'),
                'inverse_name': field.get('inverse_name'),
                'on_delete': field.get('ondelete'),
                'domain': field.get('domain'),
                'relation_field': field.get('related'),
                'relation_table': field.get('relation'),
                'column1': field.get('column1'),
                'column2': field.get('column2'),
                'auto_join': field.get('auto_join', False),
                'limit': field.get('limit'),
                'is_compute_field': not not field.get('compute', False),
                'compute_method': field.get('compute', False),
                'inverse_method': field.get('inverse', False),
                'search_method': field.get('search', False),
                'can_copy': self._field_default_attr(field, 'copy'),
                'store': self._field_default_attr(field, 'store'),
                'compute_sudo': field.get('compute_sudo', False),
                'is_related_field': not not field.get('related', False),
                'related_field': field.get('related'),
                'related_sudo': field.get('related_sudo', False),
                'default_value': self._field_default_value(field.get('default', '')),
                'is_attachment': field.get('attachment', False),
                'currency_field': field.get('currency_field', False),
                'change_default': field.get('change_default', False),
                'company_dependent': field.get('company_dependent', False),
                'group_operator': field.get('group_operator', ''),
                'group_expand': field.get('group_expand', ''),
                'states': field.get('states', ''),
                'depends': field.get('depends', ''),
            }
            if not record:
                values.update({'sequence': i})
                fields_obj.create(values)
            else:
                record.write(values)

    @api.model
    def _reverser_prototyper_method(self, methods, model_id=False):
        i = 0
        for _, method in methods.items():
            i += 1
            method_obj = self.env['prototyper.ir.model.method.doc']
            record = method_obj.search(
                [('model_id', '=', model_id.id), ('name', '=', method.get('name'))], limit=1)
            values = {
                'sequence': i,
                'model_id': model_id.id,
                'name': method.get('name') or '',
                'description': method.get('doc') or '',
                'code': method.get('code')
            }
            if not record:
                method_obj.create(values)
            else:
                record.write(values)

    @api.model
    def _translate_selection(self, model_name, field, field_name, attr):
        translate_obj = self.env['prototyper.translate']
        if field.get('type') != 'selection':
            return ''

        selection = field.get(attr, [])
        if isinstance(selection, str):
            return selection
        if callable(selection):
            return selection.__name__

        for index, item in enumerate(selection):
            value = translate_obj.translate(
                imd_name=None,
                name='%s,%s' % (model_name, field_name),
                src=item[1],
                type='selection')
            selection[index] = (item[0], value or item[1])
        return selection

    @api.model
    def _field_default_value(self, value):
        if not isinstance(value, str):
            return value

        start = value.find('default=')
        if start >= 0:
            end = value.find(',')
            value = value[start + 8:end]
        return value

    @api.model
    def _create_model_parent_menu(self, module, menu_name, menu_seq, parent_id=False):
        parent_menu_id = parent_id or module.menu_id.id

        menu_obj = self.env['prototyper.ir.ui.menu']
        menus = menu_name.split(os.path.sep)

        for name in menus:
            record = menu_obj.search([('parent_id', '=', parent_menu_id), ('name', '=', name)], limit=1)
            if not record:
                values = {
                    'name': name,
                    'parent_id': parent_menu_id,
                    'web_icon': get_random_icon(),
                    'sequence': menu_seq or 10,
                }
                record = menu_obj.create(values)
            parent_menu_id = record.id

        return record

    @api.model
    def _field_default_attr(self, field, attr_name):
        value = field.get(attr_name, None)
        # store,copy 属性的默认值
        if value == None:

            value = True
            if attr_name == 'copy' and field.get('ttype') == 'one2many':
                value = False
            elif any([
                field.get('compute', False),
                field.get('related', False),
                field.get('company_dependent', False)]):
                value = False
        return value

    @api.model
    def _reverser_prototyper_function(self, functions, module_id, parent_menu_id):
        for function_name, code in functions.items():
            pass
