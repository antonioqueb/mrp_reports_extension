from odoo import models, fields, api

class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    efficiency_percentage = fields.Float(
        string="Eficiencia (%)",
        compute='_compute_efficiency',
        store=True,
    )

    @api.depends('workorder_ids')
    def _compute_efficiency(self):
        """
        Calcula la eficiencia de la orden de fabricación basada en las órdenes de trabajo asociadas.
        """
        for record in self:
            planned_time = sum(record.workorder_ids.mapped('duration_expected'))  # Duración planificada total
            actual_time = sum(record.workorder_ids.mapped('duration'))  # Duración real total
            if actual_time > 0:
                record.efficiency_percentage = (planned_time / actual_time) * 100
            else:
                record.efficiency_percentage = 0.0


class MrpProductEfficiencyReport(models.TransientModel):
    _name = 'mrp.product.efficiency.report'
    _description = 'Reporte de Eficiencia por Producto'

    product_id = fields.Many2one('product.product', string='Producto')
    total_quantity = fields.Float(string='Cantidad Total Producida')
    total_planned_duration = fields.Float(string='Duración Planificada Total')
    total_real_duration = fields.Float(string='Duración Real Total')
    average_efficiency = fields.Float(string='Eficiencia Promedio (%)')

    @api.model
    def generate_report_data(self):
        """
        Genera datos agrupados de eficiencia por producto a partir de las órdenes de fabricación.
        """
        query = """
            SELECT 
                product_id,
                SUM(product_qty) AS total_quantity,
                SUM(planned_duration) AS total_planned_duration,
                SUM(real_duration) AS total_real_duration,
                AVG(efficiency_percentage) AS average_efficiency
            FROM (
                SELECT 
                    production.product_id,
                    production.product_qty,
                    SUM(workorder.duration_expected) AS planned_duration,
                    SUM(workorder.duration) AS real_duration,
                    CASE 
                        WHEN SUM(workorder.duration) > 0 THEN
                            (SUM(workorder.duration_expected) / SUM(workorder.duration)) * 100
                        ELSE 0
                    END AS efficiency_percentage
                FROM mrp_production production
                LEFT JOIN mrp_workorder workorder ON production.id = workorder.production_id
                GROUP BY production.id, production.product_id
            ) AS product_summary
            GROUP BY product_id
        """
        self.env.cr.execute(query)
        results = self.env.cr.dictfetchall()

        # Crear registros transitorios
        self.env['mrp.product.efficiency.report'].search([]).unlink()
        for row in results:
            self.create({
                'product_id': row['product_id'],
                'total_quantity': row['total_quantity'],
                'total_planned_duration': row['total_planned_duration'],
                'total_real_duration': row['total_real_duration'],
                'average_efficiency': row['average_efficiency'],
            })
