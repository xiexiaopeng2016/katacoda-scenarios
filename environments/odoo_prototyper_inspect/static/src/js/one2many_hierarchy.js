odoo.define('odoo_prototyper_inspect.FieldOne2manyHierarchy', function (require) {
    "use strict";

    var data = require('web.data');
    var Widget = require('web.Widget');
    var AbstractRenderer = require('web.AbstractRenderer');
    var FieldOne2Many = require('web.relational_fields').FieldOne2Many;
    var BasicModel = require('web.BasicModel');
    var registry = require('web.field_registry');
    var view_registry = require('web.view_registry');

    var One2ManyHierarchyItem = Widget.extend({
        xmlDependencies: ['/odoo_prototyper_inspect/static/src/xml/one2many_hierarchy.xml'],
        template: 'One2ManyHierarchyItem',
        events: {
            click: '_onClick',
        },
        init: function (parent, state, options) {
            this._super.apply(this, arguments);
            this._setState(state);
            this.viewOptions = {
                model: options.model,
                context: state.context,
                res_id: state.res_id,
                res_model: state.model,
                parentID: state.parentID,
                recordID: state.id,
                dataset: new data.DataSet(this, state.model, state.context),
            };
        },
        _setState: function (recordState) {
            this.state = recordState;
            this.id = recordState.res_id;
            this.db_id = recordState.id;
            this.recordData = recordState.data;
            this.display_name = recordState.data.display_name || recordState.data.name;
        },
        _onClick: function (ev) {
            ev.stopPropagation();
            this._openRecord();
        },
        _openRecord: function () {
            // var editMode = this.$el.hasClass('oe_kanban_global_click_edit');
            // this.trigger_up('open_record', {
            //     id: this.db_id,
            //     mode: editMode ? 'edit' : 'readonly',
            // });
            this.open();
        },
        open: function () {
            var self = this;
            // var _super = this._super.bind(this);
            var FormView = view_registry.get('form');
            var fields_view_def;
            if (this.viewOptions.fields_view) {
                fields_view_def = $.when(this.viewOptions.fields_view);
            } else {
                fields_view_def = this.loadFieldView(
                    this.viewOptions.dataset, this.viewOptions.view_id, 'form');
            }

            fields_view_def.then(function (viewInfo) {
                if (self.viewOptions.recordID) {
                    self.viewOptions.model.addFieldsInfo(self.viewOptions.recordID, viewInfo);
                }
                var formview = new FormView(viewInfo, {
                    modelName: self.viewOptions.res_model,
                    context: self.viewOptions.context,
                    ids: self.viewOptions.res_id ? [self.viewOptions.res_id] : [],
                    currentId: self.viewOptions.res_id || undefined,
                    index: 0,
                    mode: 'readonly',
                    footer_to_buttons: true,
                    default_buttons: false,
                    model: self.viewOptions.model,
                    parentID: self.viewOptions.parentID,
                    recordID: self.viewOptions.recordID,
                });
                if (!self.state.fieldsInfo) {
                    // _loadData 方法会出错
                    self.state.fieldsInfo = formview.loadParams.fieldsInfo;
                }
                return formview.getController(self);
            }).then(function (formView) {
                self.form_view = formView;
                var fragment = document.createDocumentFragment();
                if (self.recordID && self.shouldSaveLocally) {
                    self.model.save(self.recordID, {savePoint: true});
                }
                self.form_view.appendTo(fragment).then(function () {
                    var $buttons = $('<div>');
                    self.form_view.renderButtons($buttons);
                    $(fragment).appendTo(self.getParent().$el.parent().find('.main-context').empty());
                    // self.opened().always(function () {
                    //     if ($buttons.children().length) {
                    //         self.$footer.empty().append($buttons.contents());
                    //     }
                    //     dom.append(self.$el, fragment, {
                    //         callbacks: [{widget: self.form_view}],
                    //         in_DOM: true,
                    //     });
                    // });
                });
            });

            return this;
        },
    });

    var One2ManyHierarchyRenderer = AbstractRenderer.extend({
        template: 'One2ManyHierarchy',
        /**
         * Render the view
         *
         * @override
         * @returns {Deferred}
         */
        _render: function () {
            var oldAllFieldWidgets = this.allFieldWidgets;
            this.allFieldWidgets = {};
            this.allModifiersData = [];
            return this._renderView().then(function () {
                _.each(oldAllFieldWidgets, function (recordWidgets) {
                    _.each(recordWidgets, function (widget) {
                        widget.destroy();
                    });
                });
            });
        },
        /**
         * @override
         * @private
         */
        _renderView: function () {
            var oldWidgets = this.widgets;
            this.widgets = [];
            this.$('.sidebar>ul').empty();

            var fragment = document.createDocumentFragment();
            // render the kanban view
            this._renderOne2ManyHierarchyItem(fragment);
            this.$('.sidebar>ul').append(fragment);

            return $.when(_.invoke.bind(_, oldWidgets, 'destroy'));
        },
        /**
         * Renders kanban records with its children.
         *
         * @private
         * @override
         */
        _renderOne2ManyHierarchyItem: function (fragment, records) {
            var self = this;
            _.each(records || this.state.data, function (record) {
                var kanbanRecord = new One2ManyHierarchyItem(self, record, {model: self.getParent().Model});
                self.widgets.push(kanbanRecord);
                kanbanRecord.appendTo(fragment);
                if (record.children && record.children.length) {
                    // 渲染子记录
                    kanbanRecord.$el.append($('<ul class="treeview-menu"/>')).addClass('treeview');
                    var newFragment = kanbanRecord.$('.treeview-menu');
                    self._renderOne2ManyHierarchyItem(newFragment, record.children);
                }
            });
        }
    });

    var FieldOne2ManyHierarchy = FieldOne2Many.extend({
        specialData: '_fetchSpecialOne2ManyHierarchy',
        fieldsToFetch: {
            display_name: {type: 'char'},
        },

        init: function (parent, name, record, options) {
            this._super.apply(this, arguments);
            this.m2mValues = this.record.specialData[this.name];
            this.Model = this.m2mValues.model;
            delete this.m2mValues.model;
        },
        _render: function () {
            var self = this;
            this._setHierarchyData();
            if (!this.renderer) {
                this.renderer = new One2ManyHierarchyRenderer(this, this.value, {
                    arch: this.view.arch,
                });
                this.renderer.appendTo(this.$el);
            }
            return this._super.apply(this, arguments).then(function () {
                // Move control_panel at bottom
                if (self.control_panel) {
                    return self.control_panel.$el.appendTo(self.$el);
                }
            });
        },
        /**
         * Transforms the widget value into parent and child relationship.
         *
         * @private
         */
        _setHierarchyData: function () {
            var self = this;
            var data = self.value.data;
            _.each(data, function (record) {
                record.children = self.m2mValues[record.id] || [];
            });
        },
    });

    BasicModel.include({
        _fetchSpecialOne2ManyHierarchy: function (record, fieldName) {
            var field = record.fields[fieldName];
            if (!_.contains(["many2one", "many2many", "one2many"], field.type)) {
                return $.when();
            }

            var self = this;
            var view = record.fieldsInfo['form'];
            var options = view ? view[fieldName].options : {child_field: ''};
            var child_field = options['child_field'] || '';
            if (!child_field) {
                return $.when();
            }
            var dd = record.data[fieldName];
            var list = self.localData[dd];
            list.fieldsInfo[list.viewType][child_field].views = {'form': {}};
            return this._fetchX2ManyBatched(list, child_field).then(function () {
                var result = {model: self};
                _.each(list.data, function (datapoint) {
                    var o2m_record = self.localData[datapoint];
                    result[datapoint] = []
                    var child_list = self.localData[o2m_record.data[child_field]];
                    o2m_record.children = [];
                    _.each(child_list.data, function (child_datapoint) {
                        var child_record = self.localData[child_datapoint];
                        result[datapoint].push(child_record);
                    });
                });
                return result;
            });
        },
    });

    registry.add('one2many_hierarchy', FieldOne2ManyHierarchy);

    return FieldOne2ManyHierarchy;
});

// _onRowClicked->open_record->_onOpenRecord->_openFormDialog->_onOpenOne2ManyRecord