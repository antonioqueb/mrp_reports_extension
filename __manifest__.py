{
    'name': 'MRP Reports Extension',
    'version': '1.0',
    'category': 'Manufacturing',
    'summary': 'Extiende los reportes para el módulo MRP en Odoo 17 CE',
    'author': 'Tu Nombre o Empresa',
    'website': 'https://tuweb.com',
    'depends': ['mrp', 'base'],
    'data': [
        'security/ir.model.access.csv',
        'reports/report_templates.xml',
        'reports/report_mrp_efficiency.xml',
        'views/mrp_report_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
