odoo.define('odoo_prototyper_inspect.InnerEditKanban', function (require) {
    "use strict";

    var core = require('web.core');
    var FieldOne2Many = require('web.relational_fields').FieldOne2Many;
    var KanbanRenderer = require('web.KanbanRenderer');
    var KanbanRecord = require('web.KanbanRecord');
    var registry = require('web.field_registry');
    var BasicModel = require('web.BasicModel');
    var InnerChatter = require('mail.Chatter');
    var InnerEditorView = require('odoo_prototyper_inspect.InnerEditorView');
    var QWeb = core.qweb;
    var config = require('web.config');
    var ajax = require('web.ajax');

    ajax.loadXML('/odoo_prototyper_inspect/static/src/xml/innerChatter.xml', QWeb);

    var InnerEditKanban = FieldOne2Many.extend({
        events: _.extend({}, FieldOne2Many.prototype.events, {
            'click span.add_record': '_onAddRecord',
        }),
        init: function (parent, name, record, options) {
            this._super.apply(this, arguments);
            this.m2mValues = this.record.specialData[this.name];
            // this.Model = this.m2mValues.model;
            this.title = record.fields[name].string;
        },
        _render: function () {
            var self = this;
            if (!this.renderer) {
                this.renderer = new InnerEditKanbanRenderer(this, this.value, {
                    arch: this.view.arch,
                    viewType: 'kanban',
                    record_options: {
                        editable: false,
                        deletable: false,
                        read_only_mode: this.isReadonly,
                    },
                });
                this.renderer.appendTo(this.$el);
            }
            return this._super.apply(this, arguments).then(function () {
                if (self.control_panel) {
                    var deff = [];

                    if (!self.$el.find('.o_edit_buttons').length) {
                        var $title = self.field_title();
                        self.$buttons = self.edit_buttons();

                        deff.push(self.control_panel.$el.prepend($title));
                        deff.push(self.$el.append(self.$buttons));
                    }

                    return $.when(deff).then(function () {
                        // self.on('click', 'span.add_record', self._onAddRecord.bind(self));
                    });
                }
            });
        },
        _onAddRecord: function (ev) {
            var self = this;
            ev.stopPropagation();

            if (!this.activeActions.create) {
                if (ev.data.onFail) {
                    ev.data.onFail();
                }
            } else if (!this.creatingRecord) {
                this.creatingRecord = true;
                this._setValue({
                    operation: 'CREATE',
                    position: this.editable,
                }).always(function () {
                    self.creatingRecord = false;
                });
            }
        },
        field_title: function () {
            var $title = '';
            if (this.title) {
                $title = $('<h4>' + this.title + '</h4>');
            }
            return $title;
        },
        edit_buttons: function () {
            var $buttons = $('<div class="o_edit_buttons">' +
                '<span class="add_record"><i class="fa fa-plus-square-o"/>新增</span>' +
                '</div>');
            return $buttons;
        },
    });

    var InnerEditKanbanRenderer = KanbanRenderer.extend({
        // 添加编辑,删除按钮, 消息插件
        _renderUngrouped: function (fragment, records) {
            var editable = this.getParent().editable;
            var self = this,
                deffs = [];
            _.each(records || this.state.data, function (record) {
                var kanbanRecord = new InnerEditKanbanRecord(
                    self, record, _.extend(self.recordOptions, {model: self.getParent().Model}));
                self.widgets.push(kanbanRecord);
                kanbanRecord.appendTo(fragment);
                // deffs.push(kanbanRecord.willStart().then(function () {
                //     kanbanRecord.start();
                // }).then(function () {
                //
                //     // dom.append(fragment, kanbanRecord.$el);
                // }));
            });
            return $.when(deffs);
        },
        _renderView11: function () {
            var oldWidgets = this.widgets;
            this.widgets = [];
            // this.$el.empty();

            var displayNoContentHelper = !this._hasContent() && !!this.noContentHelp;
            // this.$el.toggleClass('o_kanban_nocontent', displayNoContentHelper);
            if (displayNoContentHelper) {
                // display the no content helper if there is no data to display
                this._renderNoContentHelper();
            } else {
                var isGrouped = !!this.state.groupedBy.length;
                // this.$el.toggleClass('o_kanban_grouped', isGrouped);
                // this.$el.toggleClass('o_kanban_ungrouped', !isGrouped);
                var fragment = document.createDocumentFragment();
                // render the kanban view
                if (isGrouped) {
                    this._renderGrouped(fragment);
                    this.$el.append(fragment);
                } else {
                    var self = this;
                    this._renderUngrouped(fragment).then(function () {
                        // self.$el.append(fragment);
                    });
                }
            }

            return this._super.apply(this, arguments).then(_.invoke.bind(_, oldWidgets, 'destroy'));
        },
    });

    var InnerEditKanbanRecord = KanbanRecord.extend({
        // xmlDependencies: ['/odoo_prototyper_inspect/static/src/xml/innerChatter.xml'],
        events: _.extend({}, KanbanRecord.prototype.events, {
            'click .o_edit_record': '_onOpenRecord',
        }),
        init: function (parent, state, options) {
            this._super.apply(this, arguments);
            var field = parent.getParent();
            var onSaved = field._setValue.bind(field, {operation: 'UPDATE', id: state.id}, {});

            this.viewOptions = {
                model: options.model,
                context: state.context,
                // domain: data.domain,
                res_id: state.res_id,
                res_model: state.model,
                parentID: state.parentID,
                recordID: state.id,
                // fields_view: data.fields_view,
                on_saved: onSaved,
                readonly: false,
                title: '',
                state: state,
                shouldSaveLocally: true,
            };
            this.mailFields = {
                "mail_thread": "message_ids",
                // "mail_activity": "activity_ids",
                // "mail_followers": "message_follower_ids",
            };
            this.chatter = null;
        },
        _render: function () {
            var self = this;
            self._super.apply(self, arguments);
            self.$el.addClass('o_kanban_record11');
            self.$record_bar = self._record_edit_bar();
            $.when(self.$el.append(self.$record_bar)).then(function () {
                self.$el.on('click', '.o_chatter_button_new_message', function (e) {
                    e.stopPropagation();
                    if (!self.chatter) {
                        self._renderChatter();
                    }
                    else {
                        self.chatter._onOpenComposerMessage();
                    }
                    self.chatter.do_show();
                });
                self.$el.on('click', '.o_chatter_button_log_note', function (e) {
                    e.stopPropagation();
                    self._renderChatter();
                    if (!self.chatter) {
                        self._renderChatter();
                    }
                    else {
                        self.chatter._onOpenComposerNote();
                    }
                    self.chatter.do_show();
                });
                self.$el.on('click', '.o_chatter_button_schedule_activity', function (e) {
                    e.stopPropagation();
                    if (!self.chatter) {
                        self._renderChatter();
                    }
                    else {
                        self.chatter._onScheduleActivity();
                    }
                });
                self.$el.on('click', '.toggle_chatter', function (e) {
                    e.stopPropagation();
                    if (!self.chatter) {
                        self._renderChatter();
                        self.chatter.do_hide();
                    }
                    self.chatter.do_toggle();
                });
            });
        },
        _renderChatter: function () {
            var self = this;
            if (!self.chatter) {
                self.chatter = new InnerChatter(self.getParent(), self.state, self.mailFields, {
                    isEditable: true,
                });
                self.chatter.appendTo($('<div>'));
                // self._handleAttributes(this.chatter.$el, node);
                self.$el.append(self.chatter.$el)
            } else {
                self.chatter.update(self.state);
            }
        },
        _record_edit_bar: function () {
            var $buttons = QWeb.render('innerChatter.Buttons', {
                new_message_btn: true,
                log_note_btn: false,
                schedule_activity_btn: true,
                isMobile: config.device.isMobile,
                message_qty: this.state.data.message_qty || 0,
                activity_qty: this.state.data.activity_qty || 0,
            });
            return $buttons;
        },
        _onOpenRecord: function () {
            var self = this;
            self.editor = new InnerEditorView(self, self.viewOptions);
            self.editor.insertAfter(self.$el).then(function () {
                self.do_hide();
            });
        },
    });

    BasicModel.include({
        _fetchSpecialOne2ManyHierarchy2: function (record, fieldName) {
            var self = this;
            var result = {model: self};

            return $.when().then(function () {
                return result;
            });
        },
    });

    registry.add('innerEdit_kanban', InnerEditKanban);

    return {
        InnerEditKanbanRecord: InnerEditKanbanRecord,
        InnerEditKanbanRenderer: InnerEditKanbanRenderer,
        InnerEditKanban: InnerEditKanban,
    };
});