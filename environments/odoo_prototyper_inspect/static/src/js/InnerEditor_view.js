odoo.define('odoo_prototyper_inspect.InnerEditorView', function (require) {
    "use strict";

    var Widget = require('web.Widget');
    var view_registry = require('web.view_registry');
    var data = require('web.data');
    var dom = require('web.dom');
    var core = require('web.core');
    var _t = core._t;

    var InnerEditorView = Widget.extend({
        xmlDependencies: ['/odoo_prototyper_inspect/static/src/xml/InnerEditor_view.xml'],
        template: 'InnerEditorView',

        init: function (parent, options) {
            this._super(parent);

            options = _.defaults(options || {}, {
                title: _t('Odoo'), subtitle: '',
                dialogClass: '',
                $content: false,
                technical: true,
            });

            this.title = options.title;
            this.subtitle = options.subtitle;
            this.dialogClass = options.dialogClass;
            this.technical = options.technical;

            this.res_model = options.res_model || null;
            this.domain = options.domain || [];
            this.context = options.context || {};
            this.options = _.extend(this.options || {}, options || {});
            this.state = options.state || {};
            this.res_id = options.res_id || null;
            this.on_saved = options.on_saved || (function () {
                });
            this.context = options.context;
            this.model = options.model;
            this.parentID = options.parentID;
            this.recordID = options.recordID;
            this.shouldSaveLocally = options.shouldSaveLocally;

            // FIXME: remove this once a dataset won't be necessary anymore to interact
            // with data_manager and instantiate views
            this.dataset = new data.DataSet(this, this.res_model, this.context);
        },
        /**
         * Wait for XML dependencies and instantiate the modal structure (except
         * modal-body).
         *
         * @override
         */
        willStart: function () {
            var self = this;
            return this._super.apply(this, arguments).then(function () {
                return self.create_editor();
            }).then(function (view) {
                self.form_view = view;
                // Render modal once xml dependencies are loaded
                // self.$editor = $(QWeb.render('InnerEditor', {
                //     title: self.title,
                //     subtitle: self.subtitle,
                //     technical: self.technical,
                // }));
                // self.on('hidden.bs.modal', _.bind(self.destroy, self));
            });
        },
        /**
         * @override
         */
        renderElement: function () {
            this._super();
            if (this.form_view) {
                this.form_view.appendTo(this.$('.editor-body'));
                this.$footer = this.$('.editor-footer');
                this.set_buttons(this.buttons);
            }
            this.$el.addClass(this.dialogClass);
        },
        /**
         * @param {Object[]} buttons - @see init
         */
        set_buttons: function (buttons) {
            var self = this;
            var readonly = _.isNumber(self.res_id) && self.readonly;
            buttons = [{
                text: (readonly ? _t("Close") : _t("Discard")),
                classes: "btn-default o_form_button_cancel",
                close: true,
                click: function () {
                    if (!readonly) {
                        self.form_view.model.discardChanges(self.form_view.handle, {
                            rollback: self.shouldSaveLocally,
                        });
                    }
                },
            }];

            if (!readonly) {
                buttons.unshift({
                    text: _t("Save"),
                    classes: "btn-primary",
                    click: function () {
                        this._save().then(self.close.bind(self));
                    }
                });
            }

            self.$footer.empty();
            _.each(buttons, function (buttonData) {
                var $button = dom.renderButton({
                    attrs: {
                        class: buttonData.classes || (buttons.length > 1 ? 'btn-default' : 'btn-primary'),
                        disabled: buttonData.disabled,
                    },
                    icon: buttonData.icon,
                    text: buttonData.text,
                });
                $button.on('click', function (e) {
                    var def;
                    if (buttonData.click) {
                        def = buttonData.click.call(self, e);
                    }
                    if (buttonData.close) {
                        $.when(def).always(self.close.bind(self));
                    }
                });
                self.$footer.append($button);
            });
        },
        set_title: function (title, subtitle) {
            this.title = title || "";
            if (subtitle !== undefined) {
                this.subtitle = subtitle || "";
            }

            var $title = this.$el.find('.editor-title').first();
            var $subtitle = $title.find('.o_subtitle').detach();
            $title.html(this.title);
            $subtitle.html(this.subtitle).appendTo($title);

            return this;
        },
        close: function () {
            this.destroy();
        },
        create_editor: function () {
            var self = this;
            // var _super = this._super.bind(this);
            var FormView = view_registry.get('form');
            var fields_view_def;
            if (self.fields_view) {
                fields_view_def = $.when(self.fields_view);
            } else {
                fields_view_def = self.loadFieldView(
                    self.dataset, self.view_id, 'form');
            }

            return fields_view_def.then(function (viewInfo) {
                if (self.recordID) {
                    self.model.addFieldsInfo(self.recordID, viewInfo);
                }
                var formview = new FormView(viewInfo, {
                    modelName: self.res_model,
                    context: self.context,
                    ids: self.res_id ? [self.res_id] : [],
                    currentId: self.res_id || undefined,
                    index: 0,
                    mode: 'edit',
                    footer_to_buttons: true,
                    default_buttons: false,
                    model: self.model,
                    parentID: self.parentID,
                    recordID: self.recordID,
                });
                if (!self.state.fieldsInfo) {
                    // _loadData 方法会出错
                    self.state.fieldsInfo = formview.loadParams.fieldsInfo;
                }
                return formview.getController(self);
            }).then(function (formView) {
                if (self.recordID && self.shouldSaveLocally) {
                    self.model.save(self.recordID, {savePoint: true});
                }
                return formView;
            });
        },
        _save: function () {
            var self = this;
            var def;
            if (this.options.on_save) {
                if (this.form_view.canBeSaved()) {
                    return $.Deferred().reject();
                }
                def = this.options.on_save(this.form_view.model.get(this.form_view.handle));
            } else {
                def = this.form_view.saveRecord(this.form_view.handle, {
                    stayInEdit: true,
                    reload: false,
                    savePoint: this.shouldSaveLocally,
                    viewType: 'form',
                });
            }
            return $.when(def).then(function () {
                // record might have been changed by the save (e.g. if this was a new record, it has an
                // id now), so don't re-use the copy obtained before the save
                self.on_saved(self.form_view.model.get(self.form_view.handle));
            });
        },
    });

    return InnerEditorView;
});