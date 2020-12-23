odoo.define('odoo_prototyper_inspect.DocumentHomePage', function (require) {

    var AbstractAction = require('web.AbstractAction');
    var core = require('web.core');
    var config = require('web.config');
    var session = require('web.session');
    var DocumentMenu = require('odoo_prototyper_inspect.DocumentMenu');
    var SidebarMenu = require('odoo_prototyper_inspect.DocumentSideMenu');
    var Tree = require('odoo_prototyper_inspect.DocumentMenuTree');


    var DocumentHomePage = AbstractAction.extend({
        // xmlDependencies: ['/odoo_prototyper_inspect/static/src/xml/document_homepage.xml'],
        template: 'Document.Home.Page',
        start: function() {
            var self = this;
            return this._super.apply(this, arguments).then(function () {
                // web_client.setElement($(document.body));
                self.instanciate_menu_widgets().then(function () {
                    self.Tree = new Tree(self, self.$('ul.page-sidebar-menu'));
                });
                // web_client.start().then(function () {
                //     web_client.action_manager.setElement(self.$('.o_main_content'));
                //     self.setParent(web_client.action_manager);
                // });
            });
        },
        load_menus: function () {
            return this._rpc({
                model: 'prototyper.ir.ui.menu',
                method: 'load_menus',
                args: [config.debug],
                context: session.user_context,
            }).then(function(menu_data) {
                // Compute action_id if not defined on a top menu item
                for (var i = 0; i < menu_data.children.length; i++) {
                    var child = menu_data.children[i];
                    if (child.action === false) {
                        while (child.children && child.children.length) {
                            child = child.children[0];
                            if (child.action) {
                                menu_data.children[i].action = child.action;
                                break;
                            }
                        }
                    }
                }
                return menu_data;
            });
        },
        instanciate_menu_widgets: function () {
            var self = this;
            var defs = [];
            return this.load_menus().then(function (menu_data) {
                self.menu_data = menu_data;

                if (self.menu) {
                    self.menu.destroy();
                }

                // 实例化菜单
                self.menu = new DocumentMenu(self, menu_data);
                defs.push(self.menu.prependTo(self.$('.page-header-menu')));

                // self.Layout = new Layout(self);
                self.SidebarMenu = new SidebarMenu(self, menu_data);
                defs.push(self.SidebarMenu.prependTo(self.$el.parents().find('.page-sidebar-wrapper')));

                return $.when.apply($, defs);
            });
        },
    });

    core.action_registry.add('document_homepage_action', DocumentHomePage);

    return DocumentHomePage;

});