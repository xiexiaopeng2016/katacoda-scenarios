# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Odoo原型设计',
    'category': '',
    'summary': '',
    'version': '13.0.1.0.0',
    'website': '2248079054@qq.com',
    'author': 'xiexiaopeng',
    'depends': [
        'web',
        'mail',
    ],
    'data': [
        'security/user_group.xml',
        'security/ir.model.access.csv',
        'views/prototyper_model_view.xml',
        'views/model_fields_view.xml',
        'views/prototyper_model_access_view.xml',
        'views/project_view.xml',
        'views/action_menu.xml',
        'views/templates.xml',
        'wizard/prototyper_module_reverser_wizard_view.xml',
        'views/prototyper_module_view.xml',
        'views/prototyper_module_doc_view.xml',
        'views/prototyper_model_doc_view.xml',
        'views/model_fields_doc_view.xml',
        'views/prototyper_model_doc_js_view.xml',
        'views/model_fields_doc_js_view.xml',
        'data/module_data.xml',
    ],
    'qweb': [
        "static/src/xml/*.xml",
    ],
    'images': [],
    'license': 'AGPL-3',
    'installable': True,
    'sequence': 20,
}
