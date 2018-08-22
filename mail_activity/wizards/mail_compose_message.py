# -*- coding: utf-8 -*-
# Copyright 2016 Odoo SA <https://www.odoo.com>
# Copyright 2018 Eficent <http://www.eficent.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
from openerp import api, fields, models


class MailComposer(models.TransientModel):
    _name = 'mail.compose.message'
    _inherit = ['mail.compose.message', 'mail.message']

    # This field is already in v10 onwards.
    subtype_id = fields.Many2one(
        default=lambda self: self.sudo().env.ref('mail.mt_comment',
                                                 raise_if_not_found=False).id)

    @api.multi
    def get_mail_values(self, res_ids):
        res = super(MailComposer, self).get_mail_values(res_ids)
        for res_id in res_ids:
            if res_id in res:
                res[res_id]['mail_activity_type_id'] = \
                    self.mail_activity_type_id.id
        return res
