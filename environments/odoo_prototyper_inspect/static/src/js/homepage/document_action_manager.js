odoo.define('odoo_prototyper_inspect.ActionManager', function (require) {
    "use strict";

    var ActionManager = require('web.ActionManager');
    var dom = require('web.dom');
    var core = require('web.core');

    ActionManager.include({
        _pushController: function (controller) {
            var self = this;

            // detach the current controller
            if (!this.navigatingInStudio) {
                this._detachCurrentController();
            }

            // push the new controller to the stack at the given position, and
            // destroy controllers with an higher index
            var toDestroy = this.controllerStack.slice(controller.index);
            // reject from the list of controllers to destroy the one that we are
            // currently pushing, or those linked to the same action as the one
            // linked to the controller that we are pushing
            toDestroy = _.reject(toDestroy, function (controllerID) {
                return controllerID === controller.jsID ||
                    self.controllers[controllerID].actionID === controller.actionID;
            });
            if (!this.navigatingInStudio) {
                this._removeControllers(toDestroy);
            }
            this.controllerStack = this.controllerStack.slice(0, controller.index);
            this.controllerStack.push(controller.jsID);

            // append the new controller to the DOM
            this._appendController(controller);

            // notify the environment of the new action
            this.trigger_up('current_action_updated', {
                action: this.getCurrentAction(),
                controller: controller,
            });

            // close all dialogs when the current controller changes
            core.bus.trigger('close_dialogs');

            // toggle the fullscreen mode for actions in target='fullscreen'
            this._toggleFullscreen();
        },
        _appendController: function (controller) {
            var $el = this.$el;
            var $main = $('.o_main_content')
            if (this.navigatingInStudio && $main.length > 0) {
                $el = $main;
                $el.empty();
            }

            dom.append($el, controller.widget.$el, {
                in_DOM: this.isInDOM,
                callbacks: [{widget: controller.widget}],
            });

            if (controller.scrollPosition) {
                this.trigger_up('scrollTo', controller.scrollPosition);
            }
        },
        _executeWindowAction: function (action, options) {
            this.navigatingInStudio = false;
            if (action.res_model == 'prototyper.ir.model.doc' || action.res_model == 'prototyper.ir.module.module.doc') {
                this.navigatingInStudio = true;
            }
            return this._super.apply(this, arguments);
        },
    });

});
