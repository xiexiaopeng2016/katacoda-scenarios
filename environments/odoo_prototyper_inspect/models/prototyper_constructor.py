# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from io import BytesIO
import base64
import os
import zipfile
import logging
import lxml.etree
import re
import textwrap
from collections import namedtuple
from jinja2 import Environment, FileSystemLoader
from datetime import date
from odoo.tools.safe_eval import safe_eval

_logger = logging.getLogger(__name__)
YEAR = date.today().year


class PrototyperConstructor(object):
    _env = None
    _api_version = None
    _data_files = ()
    _demo_files = ()
    _field_descriptions = None
    template_path = '%s/../templates/' % (os.path.dirname(__file__),)
    File_details = namedtuple('file_details', ['filename', 'filecontent'])

    def action_export(self, module):
        zip_details = self.zip_files(module)
        module.data = base64.encodestring(zip_details.stringIO.getvalue())

    @classmethod
    def action_export_tddoc(cls, module):
        pass

    def zip_files(self, module):
        zip_details = namedtuple('Zip_details', ['zip_file', 'stringIO'])
        out = BytesIO()

        with zipfile.ZipFile(out, 'w') as target:
            for prototype in module:
                self.setup_env('13.0')
                file_details = self.generate_module_files(module)
                for filename, file_content in file_details:
                    if isinstance(file_content, str):
                        file_content = file_content.encode('utf-8')
                    # Prefix all names with module technical name
                    filename = os.path.join(prototype.name, filename)
                    info = zipfile.ZipInfo(filename)
                    info.compress_type = zipfile.ZIP_DEFLATED
                    info.external_attr = 2175008768  # specifies mode 0644
                    target.writestr(info, file_content)

            return zip_details(zip_file=target, stringIO=out)

    def setup_env(self, api_version):
        if self._env is None:
            self._env = Environment(
                lstrip_blocks=True,
                trim_blocks=True,
                loader=FileSystemLoader(
                    os.path.join(self.template_path, '13.0')))
            self._api_version = api_version
        return self._env

    def constructor_file(self, filename, template, module, **kwargs):
        template = self._env.get_template(template)
        # keywords used in several templates.
        kwargs.update({
            'module': module,
            # 用在py文件的表头模板
            'export_year': date.today().year,
            'author': module.author,
            'website': module.website,
            # 'license_text': licenses.get_license_text(self.license),
            # 'cr': self._cr,
            # Utility functions
            # 'fixup_arch': self.fixup_arch,
            # 'is_prefixed': self.is_prefixed,
            # 'wrap': wrap,
        })
        return self.File_details(filename, template.render(kwargs))

    def generate_module_files(self, module):
        assert self._env is not None, \
            'Run set_env(api_version) before to generate files.'

        file_details = []
        # file_details.append(self.generate_module_manifest_file(module))
        # file_details.append(self.generate_module_init_file(module))
        # file_details.extend(self.generate_models_files(module))
        # file_details.append(self.generate_models_access_rules_file(module))
        # file_details.append(self.generate_models_record_rules_file(module))
        # file_details.append(self.generate_module_user_groups_file(module))
        # file_details.append(self.generate_module_action_menu_file(module))
        file_details.append(self.generate_module_dev_doc(module))
        return file_details

    def generate_module_manifest_file(self, module):
        fn_inc_ext = '__manifest__.py'
        return self.constructor_file(
            filename=fn_inc_ext,
            template='%s.template' % fn_inc_ext,
            module=module,
            data_files=self._data_files,
            demo_fiels=self._demo_files)

    def generate_module_init_file(self, module):
        return self.constructor_file(
            filename='__init__.py',
            template='__init__.py.template',
            module=module,
            # TODO 需要判断是否导入models
            models=True,
            wizard=True)

    def generate_models_files(self, module):
        files = []
        files.append(self.generate_models_init_file(module))
        for model in module.model_ids:
            files.append(self.generate_model_file(module, model))
        return files

    def generate_models_init_file(self, module):
        return self.constructor_file(
            filename='models/__init__.py',
            template='models/__init__.py.template',
            module=module,
            models=[
                self.friendly_name(ir_model.model)
                for ir_model in module.model_ids
            ])

    def generate_model_file(self, module, model):
        python_friendly_name = self.friendly_name(self.unprefix(model.model))
        return self.constructor_file(
            filename='models/%s.py' % python_friendly_name,
            template='models/model_name.py.template',
            module=module,
            name=python_friendly_name,
            model=model,
            fields=model.field_ids,
            unprefix=self.unprefix,
            wrap=wrap)

    def generate_models_access_rules_file(self, module):
        return self.constructor_file(
            filename='security/ir.model.access.csv',
            template='security/ir.model.access.csv.template',
            module=module,
            access_rules=module.access_ids,
            bool2num=self.bool2num)

    def generate_models_record_rules_file(self, module):
        return self.constructor_file(
            filename='security/record_rule.xml',
            template='security/record_rule.xml.template',
            module=module,
            bool2num=self.bool2num)

    def generate_module_user_groups_file(self, module):
        return self.constructor_file(
            filename='security/user_groups.xml',
            template='security/user_groups.xml.template',
            module=module,
            join_groups=self.join_groups)

    def generate_module_action_menu_file(self, module):
        return self.constructor_file(
            filename='views/action_menu.xml',
            template='views/action_menu.xml.template',
            module=module,
            join_groups=self.join_groups)

    def generate_module_dev_doc(self, module):

        return self.constructor_file(
            filename='%s.md' % module.shortdesc,
            template='module_dev_doc.md.template',
            module=module,
            name=module.shortdesc,
            models=module.model_ids,
            unprefix=self.unprefix,
            wrap=wrap)

    @classmethod
    def unprefix(cls, name):
        if not name:
            return name
        return re.sub('^x_', '', name)

    @classmethod
    def is_prefixed(cls, name):
        return bool(re.match('^x_', name))

    @classmethod
    def friendly_name(cls, name):
        return name.replace('.', '_')

    @classmethod
    def fixup_domain(cls, domain):
        """ Fix a domain according to unprefixing of fields """
        res = []
        for elem in domain:
            if len(elem) == 3:
                elem = list(elem)
                elem[0] = cls.unprefix(elem[0])
            res.append(elem)
        return res

    @classmethod
    def fixup_arch(cls, archstr):
        doc = lxml.etree.fromstring(archstr)
        for elem in doc.xpath("//*[@name]"):
            elem.attrib["name"] = cls.unprefix(elem.attrib["name"])

        for elem in doc.xpath("//*[@attrs]"):
            try:
                attrs = safe_eval(elem.attrib["attrs"])
            except Exception:
                _logger.error("Unable to eval attribute: %s, skipping",
                              elem.attrib["attrs"])
                continue

            if isinstance(attrs, dict):
                for key, val in attrs.iteritems():
                    if isinstance(val, (list, tuple)):
                        attrs[key] = cls.fixup_domain(val)
                elem.attrib["attrs"] = repr(attrs)

        for elem in doc.xpath("//field"):
            # Make fields self-closed by removing useless whitespace
            if elem.text and not elem.text.strip():
                elem.text = None

        return lxml.etree.tostring(doc)

    @classmethod
    def bool2num(cls, value):
        return 1 if value else 0

    @classmethod
    def join_groups(cls, value):
        return "[(4, ref('base.group_user')),(4, ref('md_partner_base.group_customer_company_user')),(4, ref('md_partner_base.group_customer_person_user'))]"


# Utility functions for rendering templates
def wrap(text, **kwargs):
    """ Wrap some text for inclusion in a template, returning lines

    keyword arguments available, from textwrap.TextWrapper:

        width=70
        initial_indent=''
        subsequent_indent=''
        expand_tabs=True
        replace_whitespace=True
        fix_sentence_endings=False
        break_long_words=True
        drop_whitespace=True
        break_on_hyphens=True
    """
    if not text:
        return []
    wrapper = textwrap.TextWrapper(**kwargs)
    # We join the lines and split them again to offer a stable api for
    # the jinja2 templates, regardless of replace_whitspace=True|False
    text = "\n".join(wrapper.wrap(text))
    return text.splitlines()
