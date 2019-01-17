# -*- encoding: utf-8 -*-
########################################################################################
#                                                                                      #
#    RASS - Reporting As Service                                                       #
#       Módulo creado por David Roldán & Carlos Palacio - Transfiriendo S.A MANIZALES  #
#           Generación de reportes en PDF a partir de una plantilla en libreOffice     #
#                                                                                      #
########################################################################################
{
    'name': 'Rass',
    'summary': 'Reporting as Service',
    'license': 'AGPL-3',
    'version': '9.0.1.0.0',
    'author': "David Roldan & Carlos Palacio",
    'category': 'Report',
    'description': """
IFactura - RASS
============================
RASS - Reporting As Service                                                       
Módulo creado por David Roldán & Carlos Palacio - Transfiriendo S.A MANIZALES  
Generación de reportes en PDF a partir de una plantilla en libreOffice
    """,
    'depends': [
        'base', 'report', 'website', 'report_aeroo'
    ],
    'data': [
        'views/report.xml'
    ],
    'demo': [],
    'test': [],
    'installable': True
}
