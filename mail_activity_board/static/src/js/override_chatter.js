/* Copyright 2018 David Juaneda
 * License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl). */

odoo.define('mail.Chatter.activity', function(require){
    "use strict";

    var Chatter = require('mail.Chatter');
    var core = require('web.core');
    var Model = require('web.DataModel');
    var _t = core._t;
    var QWeb = core.qweb;

    Chatter.include({
        start: function() {
            this.$('button.o_chatter_button_list_activity').click(
                this.proxy('_onListActivity')
            );
            return this._super.apply(this, arguments);
        },
        _onListActivity: function (event) {
            var res_model = this.view.dataset.model;
            var res_id = this.view.datarecord.id;
            var ResModel = new Model(res_model);

            ResModel.call('redirect_to_activities',
                [],
                {'context': {'default_id':res_id,
                            'default_model':res_model}}
            ).then($.proxy(this, "do_action"));
        },
    });
});
