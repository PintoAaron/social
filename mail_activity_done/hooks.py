# Copyright 2018 Eficent Business and IT Consulting Services S.L.
# Copyright 2018 Odoo, S.A.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from openerp.addons.mail_activity.models.mail_activity import MailActivity
from openerp.addons.mail_activity.models.mail_activity import \
    message_post_with_view


def pre_init_hook(cr):
    """
    The objective of this hook is to default to false all values of field
    'done' of mail.activity
    """
    cr.execute("""SELECT column_name
    FROM information_schema.columns
    WHERE table_name='mail_activity' AND
    column_name='done'""")
    if not cr.fetchone():
        cr.execute(
            """
            ALTER TABLE mail_activity ADD COLUMN done boolean;
            """)

    cr.execute(
        """
        UPDATE mail_activity
        SET done = False
        """
    )


def post_load_hook():

    def new_action_feedback(self, feedback=False):

        if 'done' not in self._fields:
            return self.action_feedback_original(feedback=feedback)

        message = self.env['mail.message']
        if feedback:
            self.write(dict(feedback=feedback))
        for activity in self:
            record = self.env[activity.res_model].browse(activity.res_id)
            # ----  START OF PATCH
            activity.done = True
            activity.date_done = fields.Date.today
            # ----  END OF PATCH
            message_post_with_view(
                record,
                'mail.message_activity_done',
                values={'activity': activity},
                subtype_id=self.env.ref('mail.mt_activities').id,
                mail_activity_type_id=activity.activity_type_id.id,
            )
            message |= record.message_ids[0]
        # ----  START OF PATCH
        # self.unlink()
        # ----  END OF PATCH
        return {'type': 'ir.actions.act_window_close'}

    if not hasattr(MailActivity, 'action_feedback_original'):
        MailActivity.action_feedback_original = MailActivity.action_feedback

        MailActivity.action_feedback = new_action_feedback
