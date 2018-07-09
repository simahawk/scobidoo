# Copyright 2018 Camptocamp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _


class StatechartDisplayState(models.Model):
    """Display human friendly states to your users."""

    _name = 'statechart.display_state'
    _description = 'Statechart display state'

    # TODO: add statechart_id to limit states to specific sc
    name = fields.Char(required=True, translate=True)
    description = fields.Text(translate=True)
    key = fields.Char(required=True, index=True)

    _sql_constraint = [
        ('unique_key',
         'unique(key)',
         _('Statechart display state key must be unique'))
    ]