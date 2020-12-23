# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import models, api, fields, tools
import operator
import copy
from datetime import datetime


class PrototyperIrUiMenu(models.Model):
    _name = 'prototyper.ir.ui.menu'
    _inherit = 'ir.ui.menu'
    _description = '菜单'

    _parent_store = True

    parent_id = fields.Many2one(
        string='上级菜单',
        comodel_name='prototyper.ir.ui.menu',
        ondelete='restrict')
    child_ids = fields.One2many(
        string='子菜单',
        comodel_name='prototyper.ir.ui.menu',
        inverse_name='parent_id')
    menu_style = fields.Selection(
        string='菜单样式',
        selection=[
            ('classic', 'classic'),
            ('mega', 'mega'),
            ('mega-full', 'mega-full'),
        ])
    is_sider_menu = fields.Boolean(string='侧边菜单')
    groups_id = fields.Many2many(
        string='权限组',
        comodel_name='res.groups',
        relation='prototyper_ir_ui_menu_groups_rel',
        column1='menu_id',
        column2='group_id')

    @api.model
    @tools.ormcache_context('self._uid', keys=('lang',))
    def load_menus_root(self):
        print('加载菜单....')
        fields = [
            'name', 'sequence', 'parent_id', 'action', 'web_icon_data',
            'menu_style', 'is_sider_menu'
        ]
        menu_roots = self.get_user_roots()
        menu_roots_data = menu_roots.read(fields) if menu_roots else []

        menu_root = {
            'id': False,
            'name': 'root',
            'parent_id': [-1, ''],
            'children': menu_roots_data,
            'all_menu_ids': menu_roots.ids,
        }

        menu_roots._set_menuitems_xmlids(menu_root)

        return menu_root

    @api.model
    @tools.ormcache_context('self._uid', 'debug', keys=('lang',))
    def load_menus(self, debug):
        """ Loads all menu items (all applications and their sub-menus).

        :return: the menu root
        :rtype: dict('children': menu_nodes)
        """
        print('加载菜单....', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        fields = [
            'name', 'sequence', 'parent_id', 'action', 'web_icon', 'web_icon_data',
            'menu_style', 'is_sider_menu'
        ]
        menu_roots = self.search([('parent_id', '=', False)])
        menu_roots_data = menu_roots.read(fields) if menu_roots else []
        menu_root = {
            'id': False,
            'name': 'root',
            'parent_id': [-1, ''],
            'children': menu_roots_data,
            'all_menu_ids': menu_roots.ids,
            'sider_menus': [],
        }

        if not menu_roots_data:
            return menu_root

        # menus are loaded fully unlike a regular tree view, cause there are a
        # limited number of items (752 when all 6.1 addons are installed)
        menus = self.search([('id', 'child_of', menu_roots.ids)])
        menu_items = menus.read(fields)

        # add roots at the end of the sequence, so that they will overwrite
        # equivalent menu items from full menu read when put into id:item
        # mapping, resulting in children being correctly set on the roots.
        menu_items.extend(menu_roots_data)
        menu_root['all_menu_ids'] = menus.ids  # includes menu_roots!

        # make a tree using parent_id
        menu_items_map = {menu_item["id"]: menu_item for menu_item in menu_items}
        for menu_item in menu_items:
            parent = menu_item['parent_id'] and menu_item['parent_id'][0]
            if parent in menu_items_map:
                menu_items_map[parent].setdefault(
                    'children', []).append(menu_item)

        sider_menus = []
        # sort by sequence a tree using parent_id
        for menu_item in menu_items:
            menu_item.setdefault('children', []).sort(key=operator.itemgetter('sequence'))
            if menu_item['is_sider_menu']:
                menu_item1 = copy.deepcopy(menu_item)
                menu_root['sider_menus'].append(menu_item1)
                menu_item['children'] = []

        (menu_roots + menus)._set_menuitems_xmlids(menu_root)

        # for menu_top in menu_root['children']:
        #     if menu_top['menu_style'] == 'mega':
        #         # 将children拆成3份
        #         children = menu_top['children']
        #         n = math.ceil(len(children) / 3)
        #         menu_top['children'] = [children[i:i + n] for i in range(0, len(children), n)]

        # if self.env.user.company_id.background_image:
        #     menu_root['background_image'] = True
        print('加载菜单完毕.', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        return menu_root

    @api.returns('self')
    def _filter_visible_menus(self):
        return self
