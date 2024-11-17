from odoo import models, fields, api

class MrpReportEfficiency(models.Model):
    _inherit = 'mrp.production'

    efficiency_percentage = fields.Float(string="Eficiencia (%)", compute='_compute_efficiency')

    @api.depends('workorder_ids')
    def _compute_efficiency(self):
        for record in self:
            # Usa el campo correcto para el tiempo planificado
            planned_time = sum(record.workorder_ids.mapped('duration_expected'))
            actual_time = sum(record.workorder_ids.mapped('duration'))
            record.efficiency_percentage = (planned_time / actual_time) * 100 if actual_time else 0
