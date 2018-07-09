# Copyright 2018 Camptocamp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _


class DisplayStateNotFound(Exception):
    pass


class StatechartMixin(models.AbstractModel):

    _inherit = 'statechart.mixin'

    sc_display_state_id = fields.Many2one(
        comodel_name='statechart.display_state'
    )
    sc_display_state = fields.Char(
        compute='_compute_sc_display_state')
    sc_display_state_desc = fields.Char(
        compute='_compute_sc_display_state')

    @api.depends('sc_display_state_id')
    def _compute_sc_display_state(self):
        for rec in self:
            if rec.sc_display_state_id:
                state = rec.sc_display_state_id.name
                desc = rec.sc_display_state_id.description
            else:
                state = super(StatechartMixin, rec)._compute_sc_display_state()
                # TODO: any better thing here?
                desc = ''
            rec.update({
                'sc_display_state': state,
                'sc_display_state_desc': desc,
            })

    @api.multi
    def sc_update_display_state(self, key, raise_if_missing=True):
        """Retrieve state via its unique key.
        
        You are supposed to use this in "on entry" declaration 
        of your statechart, for instance:

            states:
            - name: draft
                transitions:
                - event: make_published
                    target: published
                    action: |
                    o.make_published.origin(o)
                    on entry: |
                    o.sc_update_display_state("my_unique_key")
        """
        self.ensure_one()
        # TODO: assign possible display states to statecharts
        # and search only by current statechart
        state = \
            self.env['statechart.display_state'].search([('key', '=', key)])
        if not state and raise_if_missing:
            raise DisplayStateNotFound(key)
        self.sc_display_state_id = state
