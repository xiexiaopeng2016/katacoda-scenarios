odoo.define('web.ListFormRenderer', function (require) {
    "use strict";

    var ListRenderer = require('web.ListRenderer');
    var FormRenderer = require('web.FormRenderer');

    var ListFormRenderer = ListRenderer.extend({
        className: 'o_listform_view',
        events: {
            'click tbody tr.o_data_row': '_onRowClicked',
            'click tfoot': '_onFooterClick',
            'click tr .o_list_record_delete': '_onTrashIconClick',
            'click .o_field_x2many_list_row_add a': '_onAddRecord',
        },

        /**
         * 渲染与记录对应的行
         * Render a row, corresponding to a record.
         *
         * @private
         * @param {Object} record
         * @returns {jQueryElement} a <tr> element
         */
        _renderRow: function (record) {
            var self = this;
            this.defs = []; // TODO maybe wait for those somewhere ?
            // 渲染每个单元格
            // var $cells = _.map(this.columns, function (node, index) {
            //     return self._renderBodyCell(record, node, index, {mode: 'readonly'});
            // });
            // delete this.defs;

            // 把列表的每行渲染成form视图
            if (!record.renderer){
                record.renderer = new FormRenderer(self, record, {
                    activeActions: {
                        create: true,
                        delete: true,
                        duplicate: true,
                        edit: true
                    },
                    mailFields: {
                        mail_activity: 'activity_ids',
                        mail_followers: 'message_follower_ids',
                        mail_thread: 'message_ids'
                    },
                    arch: self.arch,
                    mode: 'readonly',
                    viewType: 'listform',
                });
            } else {
                record.renderer._renderView();
            }

            // 把单元格添加到一行
            var $tr = $('<tr/>', {class: 'o_data_row'}).data('id', record.id);
            record.renderer.appendTo($tr);

            this._setDecorationClasses(record, $tr);
            return $tr;
        },
        _renderEditRow: function (record, mode) {
            var self = this;
            this.defs = []; // TODO maybe wait for those somewhere ?
            // 渲染每个单元格
            // var $cells = _.map(this.columns, function (node, index) {
            //     return self._renderBodyCell(record, node, index, {mode: 'readonly'});
            // });
            // delete this.defs;

            // 把列表的每行渲染成form视图
            if (record.renderer){
                record.renderer.mode = 'edit';
                record.renderer._renderView();
            }

            // 把单元格添加到一行
            var $tr = $('<tr/>', {class: 'o_data_row'}).data('id', record.id);
            record.renderer.appendTo($tr);

            this._setDecorationClasses(record, $tr);
            return $tr;
        },
        /**
         * 列表的主渲染函数。 它呈现为一个表。现在, 此方法不等待字段小部件就绪
         * Main render function for the list.  It is rendered as a table. For now,
         * this method does not wait for the field widgets to be ready.
         *
         * @override
         * @private
         * returns {Deferred} this deferred is resolved immediately
         */
        _renderView: function () {
            var self = this;
            // destroy the previously instantiated pagers, if any
            _.invoke(this.pagers, 'destroy');
            this.pagers = [];

            var $table = $('<table>').addClass('o_listform_view table table-condensed table-striped');
            this.$el.empty().append($table);
            // $table.toggleClass('o_list_view_grouped', is_grouped);
            // $table.toggleClass('o_list_view_ungrouped', !is_grouped);
            $table.append(this._renderBody())

            if (this.selection.length) {
                var $checked_rows = this.$('tr').filter(function (index, el) {
                    return _.contains(self.selection, $(el).data('id'));
                });
                $checked_rows.find('.o_list_record_selector input').prop('checked', true);
            }
            return this._super();
        },
        _renderBody: function () {
            var $rows = this._renderRows();
            return $('<tbody>').append($rows);
        },
        /**
         * 单击<tr>标签时触发
         * @private
         * @param {MouseEvent} event
         */
        _onRowClicked: function (event) {
            // The special_click property explicitely allow events to bubble all
            // the way up to bootstrap's level rather than being stopped earlier.
            if (this._isEditable()) {
                if (!$(event.target).prop('special_click')) {
                    var id = $(event.currentTarget).data('id');
                    if (id) {
                        // 点击的单元格
                        var $tr = $(event.currentTarget);
                        // 第几行
                        var rowIndex = this.$('.o_data_row').index($tr);
                        if (rowIndex === this.currentRow) {
                            event.stopPropagation();
                        } else {
                            // 第几列
                            var colIndex = 0;
                            this.currentFieldIndex = colIndex;
                            this._selectCell(rowIndex, colIndex, {event: event});
                        }
                    }
                }
            }
        },
        setRowMode: function (recordID, mode) {
            var self = this;
            var rowIndex = _.findIndex(this.state.data, {id: recordID});
            if (rowIndex < 0) {
                return $.when();
            }
            var editMode = (mode === 'edit');
            var record = this.state.data[rowIndex];

            this.currentRow = editMode ? rowIndex : null;
            var $row = this.$('.o_data_row:nth(' + rowIndex + ')');
            var oldWidgets = _.clone(this.allFieldWidgets[record.id]);

            // Switch each cell to the new mode; note: the '_renderBodyCell'
            // function might fill the 'this.defs' variables with multiple deferred
            // so we create the array and delete it after the rendering.
            var defs = [];
            this.defs = defs;
            // 重新渲染行
            var $newrow = this._renderEditRow(record, mode);
            $row.replaceWith($newrow);
            delete this.defs;

            // Destroy old field widgets
            _.each(oldWidgets, this._destroyFieldWidget.bind(this, record));

            // Toggle selected class here so that style is applied at the end
            $row.toggleClass('o_selected_row', editMode);

            return $.when.apply($, defs);
        },
    });

    return ListFormRenderer;
});
