odoo.define('web.relational_fieldsX', function (require) {
    "use strict";

    var relational_fields = require('web.relational_fields');
    var FieldOne2Many = relational_fields.FieldOne2Many;
    var ListFormRenderer = require('web.ListFormRenderer');

    FieldOne2Many.include({
        _render: function () {
            if (!this.view) {
                return this._super();
            }
            if (this.renderer) {
                this.renderer.updateState(this.value, {});
                this.pager.updateState({size: this.value.count});
                return $.when();
            }
            var arch = this.view.arch;
            // 加上listform类型
            if (arch.tag === 'listform') {
                this.renderer = new ListFormRenderer(this, this.value, {
                    arch: arch,
                    mode: this.mode,
                    addCreateLine: !this.isReadonly && this.activeActions.create,
                    addTrashIcon: !this.isReadonly && this.activeActions.delete,
                    viewType: 'listform',
                });
            }
            return this.renderer ? this.renderer.appendTo(this.$el) : this._super();
        },
    });

});