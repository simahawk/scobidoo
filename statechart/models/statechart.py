# -*- coding: utf-8 -*-
# Copyright 2016 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import io
import logging

from odoo import api, fields, models
from odoo import tools

from sismic.exceptions import StatechartError
from sismic import io as sismic_io

_logger = logging.getLogger(__name__)


class Statechart(models.Model):

    _name = 'statechart'
    _description = 'Statechart'

    name = fields.Char(
        readonly=True,
        store=True,
        compute='_compute_name',
    )
    model_ids = fields.One2many(
        comodel_name='ir.model',
        inverse_name='statechart_id',
        string='Models',
        ondelete='restrict',
    )
    yaml = fields.Text(
        help="YAML representation of the state chart."
             "Currently it is the input, to become a computed field "
             "from a future record-based representation of "
             "the statechart.",
    )

    _sql_constraint = [
        ('unique_name',
         'unique(name)',
         'Statechart name must be unique')
    ]

    @api.depends('yaml')
    def _compute_name(self):
        for rec in self:
            rec.name = rec.get_statechart().name

    @api.multi
    def get_statechart(self):
        self.ensure_one()
        _logger.debug("loading statechart model for %s", self.display_name)
        with io.StringIO(self.yaml) as f:
            try:
                return sismic_io.import_from_yaml(f)
            except StatechartError:
                # TODO better error message
                raise

    @api.model
    @tools.ormcache('name')
    def statechart_by_name(self, name):
        """Load and parse the statechart for an Odoo model."""
        statechart = self.search([('name', '=', name)])
        if not statechart:
            raise RuntimeError("Statechart %s not found" % name)
        return statechart.get_statechart()

    @api.multi
    def write(self, vals):
        self.statechart_by_name.clear_cache(self)
        return super(Statechart, self).write(vals)

    @api.multi
    def unlink(self):
        self.statechart_by_name.clear_cache(self)
        return super(Statechart, self).unlink()
