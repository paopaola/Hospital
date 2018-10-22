# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Klinikë Mjekësore',
    'version': '1.0',
    'category': 'Health',
    'sequence': 75,
    'summary': 'Regjistrimi/Menaxhimi i Pacientëve/Orareve',
    'description': "",
    'website': 'www.commprog.com',
    'images': [

    ],
    'depends': [

    ],
    'data': [
        'views/pacienti_views.xml',
        'views/doktori_views.xml',
        'views/departamenti_views.xml',
        'views/konsulta_views.xml',
    ],

    'demo': [

    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'qweb': [],
}
