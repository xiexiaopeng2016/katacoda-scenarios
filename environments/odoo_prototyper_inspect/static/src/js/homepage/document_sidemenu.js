odoo.define('odoo_prototyper_inspect.DocumentSideMenu', function (require) {
    "use strict";

    var Widget = require('web.Widget');

    var DocumentSideMenu = Widget.extend({
        template: 'SiderMenu',
        init: function (parent, menu_data) {
            this.menu_data = menu_data;
            this._super.apply(this, arguments);
        },
        start: function () {
            var self = this;
            return this._super.apply(this, arguments).then(function () {
                self.$el.find('.oe_secondary_menu:first-child').removeClass('o_hidden');
            });
        }
    });

    return DocumentSideMenu;
});
