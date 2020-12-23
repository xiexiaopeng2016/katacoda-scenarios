odoo.define('odoo_prototyper_inspect.form_renderer', function (require) {
    "use strict";

    var FormRenderer = require('web.FormRenderer');
    var UMLGraph = require('odoo_prototyper_inspect.UMLGraph');

    FormRenderer.include({
        /**
         * @override
         */
        init: function (parent, state, params) {
            this._super.apply(this, arguments);
            // this.mailFields = params.mailFields;
            // this.umlGraph = undefined;
        },
        _renderNode: function (node) {
            if (node.tag === 'div' && node.attrs.class === 'o_UmlGraph') {
                if (this.mode === 'edit' && !this.state.data.id) {
                    // there is no chatter in create mode
                    var $div = $('<div>');
                    this._handleAttributes($div, node);
                    return $div;
                } else {
                    if (!this.umlGraph) {
                        this.umlGraph = new UMLGraph(this, this.state, this.mailFields, {
                            isEditable: this.activeActions.edit,
                        });
                        this.umlGraph.appendTo($('<div>'));
                        this._handleAttributes(this.umlGraph.$el, node);
                    } else {
                        // this.umlGraph.update(this.state);
                    }
                    return this.umlGraph.$el;
                }
            } else {
                return this._super.apply(this, arguments);
            }
        },
        // _updateView: function () {
        //     if (this.umlGraph) {
        //         this.umlGraph.$el.detach();
        //     }
        //     return this._super.apply(this, arguments);
        // },
    });

});
