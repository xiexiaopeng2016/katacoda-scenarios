odoo.define('odoo_prototyper_inspect.DocumentMenuTree', function (require) {
    "use strict";

    var Widget = require('web.Widget');
    var core = require('web.core');

    var Selector = {
        tree: '.page-sidebar-menu',
        treeview: '.nav-item:not(.nav-leaf)',
        treeviewMenu: '.sub-menu',
        open: '.open',
        li: 'li',
        data: '[data-widget="tree"]',
        active: '.active',
        editMenu: '.o_web_edit_menu',
        mainHeader: '.page-header',
    };

    var ClassName = {
        open: 'open',
        active: 'active',
        tree: 'tree'
    };

    var Event = {
        collapsed: 'collapsed.tree',
        expanded: 'expanded.tree'
    };

    var DocumentMenuTree = Widget.extend({
        init: function (parent, element) {
            this._super.apply(this, arguments);

            this.element = element;
            this.options = {
                animationSpeed: 500,
                accordion: true,
                followLink: false,
                trigger: '.nav-item a'
            };

            $(this.element).addClass(ClassName.tree);
            $(Selector.treeview + Selector.active, this.element).addClass(ClassName.open);

            $(Selector.tree).slimScroll({
                height: ($(window).height() - $(Selector.mainHeader).height()) + 'px',
                color: 'rgba(0,0,0,0.2)',
                size: '5px'
            });

            this._setUpListeners();
        },
        toggle: function (link, event) {
            var treeviewMenu = link.next(Selector.treeviewMenu);
            var parentLi = link.parent();
            var isOpen = parentLi.hasClass(ClassName.open);

            if (!parentLi.is(Selector.treeview)) {
                parentLi.parent().parent().addClass(ClassName.active);
                event.stopPropagation();
                return;
            }

            if (!this.options.followLink || link.attr('href') == '#') {
                event.preventDefault();
            }

            if (isOpen) {
                this.collapse(treeviewMenu, parentLi);
            } else {
                this.expand(treeviewMenu, parentLi);
            }
        },
        expand: function (tree, parent) {
            var expandedEvent = $.Event(Event.expanded);

            if (this.options.accordion) {
                var openMenuLi = parent.siblings(Selector.open);
                var openTree = openMenuLi.children(Selector.treeviewMenu);
                this.collapse(openTree, openMenuLi);
            }

            parent.addClass(ClassName.open);
            tree.slideDown(this.options.animationSpeed, function () {
                $(this.element).trigger(expandedEvent);
            }.bind(this));
        },
        collapse: function (tree, parentLi) {
            var collapsedEvent = $.Event(Event.collapsed);

            tree.find(Selector.open).removeClass(ClassName.open);
            parentLi.removeClass(ClassName.open);
            parentLi.removeClass(ClassName.active);
            tree.slideUp(this.options.animationSpeed, function () {
                tree.find(Selector.open + ' > ' + Selector.treeview).slideUp();
                $(this.element).trigger(collapsedEvent);
            }.bind(this));
        },
        _setUpListeners: function () {
            var that = this;

            $(this.element).on('click', this.options.trigger, function (event) {
                that.toggle($(this), event);
                that._on_menu_click(event);
            });

            $(this.element).on('click', Selector.editMenu, function (event) {
                var menu_id = $(event.currentTarget).data('current_primary_menu');
                core.bus.trigger('trigger_edit_menu', menu_id);
            });
        },
        _on_menu_click: function (ev) {
            var menu_id = $(ev.currentTarget).data('menu');
            var action_id = $(ev.currentTarget).data('action-id');
            if (action_id) {
                this.trigger_up('menu_clicked', {
                    id: menu_id,
                    action_id: action_id,
                    previous_menu_id: this.current_secondary_menu,
                });
                this.current_secondary_menu = menu_id;
            }
        },
    });

    return DocumentMenuTree;

});
