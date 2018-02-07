# Copyright 2018 Eficent Business and IT Consulting Services S.L.
#   (http://www.eficent.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    'name': 'Mass mailing exclusion',
    'summary': """Exclude mass mailing targets that are in other campaigns already performed.""",
    'version': '11.0.1.0.0',
    'license': 'AGPL-3',
    'author': 'Eficent, Odoo Community Association (OCA)',
    'website': 'https://github.com/OCA/social',
    'depends': [
        'mass_mailing',
    ],
    'data': [
        'views/mass_mailing_exclusion.xml',
        ],
    'images': [
        'static/description/preview.png',
    ]
}