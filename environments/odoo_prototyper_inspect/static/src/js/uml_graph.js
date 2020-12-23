odoo.define('odoo_prototyper_inspect.UMLGraph', function (require) {
    "use strict";

    var Widget = require('web.Widget');
    var rpc = require("web.rpc");

    var UMLGraph = Widget.extend({
        init: function () {
            this.get_uml_data();
            return this._super.apply(this, arguments);
        },
        get_uml_data: function () {
            var self = this;
            var module_id = 33;
            rpc.query({
                model: 'prototyper.ir.module.module.doc',
                method: 'get_uml_data',
                args: [module_id],
            }).then(function (result) {
                self.create_graph(result);
            });
        },
        create_graph: function (data) {
            var self = this;
            var graph = new joint.dia.Graph();
            var paper = new joint.dia.Paper({
                el: $('#paper'),
                width: 800,
                height: 600,
                gridSize: 1,
                model: graph
            });


            var classes = {};
            _.each(data.classes, function (cls) {
                classes[cls.name] = self.create_class(cls);
            });

            var relations = [];
            _.each(data.relations, function (relation) {
                var source = relation.source,
                    target = relation.target;
                if (classes[source[0]] && classes[target[0]]) {
                    var options = {
                        source: {id: classes[source[0]]['id']},
                        target: {id: classes[target[0]]['id']},
                        type: 'a',
                    };
                    relations.push(self.create_relation(options));
                }
            });

            _.each(classes, function (c) {
                graph.addCell(c);
            });

            _.each(relations, function (r) {
                graph.addCell(r);
            });
        },
        create_class: function (cls) {
            var uml = joint.shapes.uml;
            var x, y;
            [x, y] = cls.position.split(",");
            return new uml.Class({
                position: {x: Number(x), y: Number(y)},
                size: {width: 220, height: (cls.attributes.length + cls.methods.length + 4) * 12},
                name: cls.name,
                attributes: cls.attributes,
                methods: cls.methods,
                attrs: {
                    '.uml-class-name-rect': {
                        fill: '#ff8450',
                        stroke: '#fff',
                        'stroke-width': 0.5,
                    },
                    '.uml-class-attrs-rect, .uml-class-methods-rect': {
                        fill: '#fe976a',
                        stroke: '#fff',
                        'stroke-width': 0.5
                    },
                    '.uml-class-attrs-text': {
                        ref: '.uml-class-attrs-rect',
                        'ref-y': 0.5,
                        'y-alignment': 'middle'
                    },
                    '.uml-class-methods-text': {
                        ref: '.uml-class-methods-rect',
                        'ref-y': 0.5,
                        'y-alignment': 'middle'
                    }
                }
            });
        },
        create_relation: function (options) {
            var uml = joint.shapes.uml;
            if (options.type === 'g') {
                return new uml.Generalization({source: {id: options.source}, target: {id: options.target}});
            } else if (options.type === 'i') {
                return new uml.Implementation({source: {id: options.source}, target: {id: options.target}});
            } else if (options.type === 'a') {
                return new uml.Aggregation({source: {id: options.source}, target: {id: options.target}});
            } else if (options.type === 'i') {
                return new uml.Composition({source: {id: options.source}, target: {id: options.target}});
            }
        },
    });

    return UMLGraph;
});

