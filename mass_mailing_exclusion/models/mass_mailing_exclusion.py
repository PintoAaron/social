# Copyright 2018 Eficent Business and IT Consulting Services S.L.
#   (http://www.eficent.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models, fields
import logging

_logger = logging.getLogger(__name__)


class MassMailingExclusion(models.Model):
    """

    """
    _inherit = 'mail.mass_mailing'

    mass_mailing_excluded_ids = fields.Many2many('mail.mass_mailing', 'mass_mailing_excluded_rel', 'col1', 'col2',
                                                 string='Exclude mails from Mass mailings')

    def _get_seen_list(self):
        seen_list = super()._get_seen_list()

        self.ensure_one()
        target = self.env[self.mailing_model_real]
        mail_field = 'email' if 'email' in target._fields else 'email_from'
        query = """
                    SELECT lower(substring(%(mail_field)s, '([^ ,;<@]+@[^> ,;]+)'))
                      FROM mail_mail_statistics s
                      JOIN %(target)s t ON (s.res_id = t.id)
                     WHERE substring(%(mail_field)s, '([^ ,;<@]+@[^> ,;]+)') IS NOT NULL
                """
        if self.mass_mailing_excluded_ids:
            query += """
                       AND s.mass_mailing_id IN (%%(mailing_ids)s);
                    """
        query = query % {'target': target._table, 'mail_field': mail_field}
        params = {'mailing_ids': tuple(self.mass_mailing_excluded_ids.ids,)}
        self._cr.execute(query, params)
        seen_list.update(set(m[0] for m in self._cr.fetchall()))
        _logger.info(
            "Mass-mailing %s has already reached %s %s emails", self, len(seen_list), target._name)
        return seen_list
