# Copyright 2018 Camptocamp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Statechart display state',
    'description': """Prototype for displaying states to end users.""",
    'version': '11.0.1.0.0',
    'license': 'AGPL-3',
    'author': 'Camptocamp,Odoo Community Association (OCA)',
    'website': 'https://github.com/acsone/scobidoo',
    'depends': [
        'statechart',
    ],
    'data': [
        'security/statechart_display_state.xml',
        'views/statechart_display_state.xml',
    ],
}
