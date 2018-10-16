# Copyright 2018 Eficent Business and IT Consulting Services S.L.
# Copyright 2018 Tecnativa, S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from openerp import api, SUPERUSER_ID


def update_date_done_activities(env):
    """Update the field 'date_done' in mail_activity for the activities
    that have been completed."""

    env.cr.execute("""
        UPDATE mail_activity
        SET date_done = date_deadline
        WHERE done = True
    """)


def migrate(cr, version):
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})
        update_date_done_activities(env)

