# -*- coding: utf-8 -*-
{
    'name': "Autorisations",
    'sequence': 400,
    'version': '1.0',

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
 
    # any module necessary for this one to work correctly
    'depends': ['base','hr','hr_holidays'],

    # always loaded
    'data': [
        
        'security/authorisation_security.xml',
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        #'data/user_exist_cron.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
