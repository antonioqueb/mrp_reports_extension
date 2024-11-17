from odoo import models, fields, api

class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    efficiency_percentage = fields.Float(
        string="Eficiencia (%)",
        compute='_compute_efficiency',
        store=True,
    )

    @api.depends('workorder_ids.duration_expected', 'workorder_ids.duration')
    def _compute_efficiency(self):
        """
        Calcula la eficiencia de la orden de fabricación basada en las órdenes de trabajo asociadas.
        """
        for record in self:
            planned_time = sum(record.workorder_ids.mapped('duration_expected'))
            actual_time = sum(record.workorder_ids.mapped('duration'))
            if actual_time > 0:
                record.efficiency_percentage = (planned_time / actual_time) * 100
            else:
                record.efficiency_percentage = 0.0
