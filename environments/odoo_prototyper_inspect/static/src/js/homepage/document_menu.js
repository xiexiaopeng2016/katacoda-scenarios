odoo.define('odoo_prototyper_inspect.DocumentMenu', function (require) {
    "use strict";

    var dom = require('web.dom');
    // var Menu = require('web.Menu');
    var Menu = require('web_enterprise.Menu');

    var DocumentMenu = Menu.extend({
        template: 'Metronic.Menu',
        menusTemplate: 'Metronic.Menu.sections',
        start: function () {
            var self = this;

            this.$menu_apps = this.$('.o_menu_apps');
            this.$menu_brand_placeholder = this.$('.o_menu_brand');
            this.$section_placeholder = this.$('.o_menu_sections');

            // Navbar's menus event handlers
            var on_secondary_menu_click = function (ev) {
                ev.preventDefault();
                var menu_id = $(ev.currentTarget).data('menu');
                var action_id = $(ev.currentTarget).data('action-id');
                self._on_secondary_menu_click(menu_id, action_id);
            };
            var menu_ids = _.keys(this.$menu_sections);
            var primary_menu_id, $section;
            for (var i = 0; i < menu_ids.length; i++) {
                primary_menu_id = menu_ids[i];
                $section = this.$menu_sections[primary_menu_id];
                $section.on('click', 'a[data-menu]', self, on_secondary_menu_click.bind(this));
            }

            // dom.initAutoMoreMenu(this.$section_placeholder, {
            //     maxWidth: function () {
            //         return self.$el.width() - (self.$menu_apps.outerWidth(true) + self.$menu_brand_placeholder.outerWidth(true) + self.systray_menu.$el.outerWidth(true));
            //     },
            //     sizeClass: 'SM',
            // });
            // xxp

            _.each(this.$menu_sections, function (item) {
                $(item).appendTo(self.$section_placeholder);
            });

            return $.when();
        },
        openFirstApp: function () {
            // this._appsMenu.openFirstApp();
        },
        _on_secondary_menu_click: function () {
            this._super.apply(this, arguments);

            var $current_secondary_menu  = $(".oe_secondary_menu[data-menu-parent='"+ this.current_secondary_menu +"']");
            if ($current_secondary_menu.hasClass('o_hidden')) {
                // $content.addClass('page-full-width');
                $current_secondary_menu.removeClass('o_hidden');
            }
            else {
                return;
            }

            // 隐藏其他菜单
            var $other_secondary_menu  = $(".oe_secondary_menu[data-menu-parent!='"+ this.current_secondary_menu +"']");
            _.each($other_secondary_menu, function (el) {
                if (!$(el).hasClass('o_hidden')) {
                    $(el).addClass('o_hidden');
                }
            });
        },
        _updateMenuBrand: function (brandName) {},
        change_menu_section: function (primary_menu_id) {},
    });

    return DocumentMenu;

});
