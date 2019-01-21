# -*- coding: utf-8 -*-
from openerp import http, exceptions, _
import json
import logging
import requests
import werkzeug
import base64
import time

from openerp import http
from openerp.http import request, serialize_exception as _serialize_exception, content_disposition
from openerp.exceptions import AccessError, UserError
from openerp.service.report import exp_report, exp_report_get

_logger = logging.getLogger(__name__)

class ReportController(http.Controller):
    @http.route('/rass/dini/', auth='public')
    def index(self, **kw):
        #dini = self.diniRequest()
        return "hello world"
    #metodo para validar token
    def validateAuthorization(self,request):
        try:
            headers = request.httprequest.headers
            _logger.info("headers %s", headers["Authorization"])
            token = ""
            if headers["Authorization"]:
                token = headers["Authorization"].split("bearer")[1]
                exist = request.env['ir.config_parameter'].sudo().get_param('serviceToken')
            if not exist :
                return json.dumps({
                    "error": str([{"codigo":"404", "mensaje no existe":"No autorizado"}]),
                    },encoding='utf-8', indent=4)
            if str(exist).strip() != str(token).strip():
                return json.dumps({
                    "error": str([{"codigo":"404", "mensaje":"No autorizado"}]),
                    },encoding='utf-8', indent=4)
            else:
                return True
        except Exception, e:
            return json.dumps({
                "error": "error "+ str(e),
                "msg":"No autorizado",
                },encoding='utf-8', indent=4) 

    
    @http.route('/api/rass', type='json', auth='public', methods=['POST'], csrf=False)
    
    def rass(self, **args):
        validate = self.validateAuthorization(http.request)
        if validate == True: 
            dini = args.get("dini",False)
            if not dini:
                return json.dumps({
                    "error":"peticion incorrecta"
                })
            else:
                company = http.request.env["report_rass.configuration"].sudo().search([('BusinessId','=',dini["cabecera"]["IdEmpresa"])])
                if not company:
                    return json.dumps({
                        "error": "Esta empresa no esta configurada."
                    })
                else:
                    try:
                        POLLING_DELAY = 1.00
                        rassobj = self.saveModelFromDini(dini)
                        #pepe = http.request.env['report_rass.dini'].sudo().browse(rassobj.id)                    
                    
                        print_ids = [rassobj.id]
                        rep_obj = http.request.env['ir.actions.report.xml']
                        data = {
                                'model': http.request.env['report_rass.dini'],
                                'ids': print_ids,
                                'id': print_ids[0]
                            
                                }
                        action =  {
                                'type': 'ir.actions.report.xml',
                                'report_name': company.TemplateBusiness.report_name,
                                'datas': data,
                                'context': http.request.env.context
                                }                
                        report_data = {}
                        report_ids = [rassobj.id]
                        _logger.info('rass obj id %s', rassobj.id)
                        if 'report_type' in action:
                            report_data['report_type'] ='aeroo'
                        if 'datas' in action:
                            if 'ids' in action['datas']:
                                report_ids = action['datas'].pop('ids')
                            report_data.update(action['datas'])
                        #context = http.request.env.context
                        contexto = {'lang': 'es_CO', 'tz': False, 'uid': 1, 'active_model': 'report_rass.dini'}            
                        #uid = http.request.session.authenticate(http.request.session.db, 'jroldan','admin123')
                        #_logger.info('report id22 %s', report_ids)
                        report_id = exp_report("rass9", 1, str(action["report_name"]), report_ids, report_data, contexto)
                        _logger.info('db2 %s', str(request.session.db))
                        _logger.info('uid2 %s', str(request.session.uid))
                        _logger.info('report name2 %s', str(action["report_name"]))
                        _logger.info('reports id2 %s', str(report_ids))
                        _logger.info('report data2 %s', str(report_data))
                        _logger.info('contexto2 %s', str(contexto))
                        _logger.info('report id2 %s', str(report_id))   
                        report_struct = None
                        report_struct = exp_report_get("rass9", 1, report_id)
                        
                        while True:
                            _logger.info('sisarras %s', str(contexto))
                            report_struct = exp_report_get("rass9", 1, report_id)
                            if report_struct["state"]:
                                break
                            time.sleep(POLLING_DELAY)
                            
                        _logger.info('reporte base 64 result %s', report_struct['result'])
                        report_fin = str(report_struct['result'])
                        final = report_fin.replace("\n", "")
                        reporte_final = base64.b64decode(report_struct['result'])

                        _logger.info('reporte base 64 %s', str(reporte_final))

                        return json.dumps({
                            "success": str(final)
                        })
                    except Exception, e:  
                        return json.dumps({
                            "userMessage": "La peticion es incorrecta",
                            "error": str(e)
                        }) 
        else:
            return validate
     #return request.session.uid

    def saveModelFromDini(self,dini):
        """interpretara y guardara"""

        #Validación por Nit de empresa
        company = http.request.env["report_rass.configuration"].sudo().search([('BusinessId','=',dini["cabecera"]["IdEmpresa"])])
        if not company:
            return json.dumps({
                "error": "Esta empresa no esta configurada."
            })
        if company:
            #Arreglo de imagenes
            if dini:
                images = http.request.env["report_rass.images"]
                rassimages = images.sudo().create({
                    'CodeQr': dini["images"]["codigoQR"]
                })
            #Creación de los adicionales de cabecera
            if dini:          
                objaditional = []
                aditionaldini = http.request.env["report_rass.aditional"]
                for aditional in dini["cabecera"]["AdditionalInfo"]:
                    rassobjaditional = aditionaldini.sudo().create({
                        'position': aditional["Position"],
                        'value': aditional["Value"]
                    })
                    objaditional.append(rassobjaditional.id)
            #Creación de los adicionales impuestos de cabecera
            if dini:          
                objaditionalimp = []
                aditionalimpdini = http.request.env["report_rass.aditionalimp"]
                for aditional in dini["cabecera"]["AdditionalInfoImpuestos"]:
                    rassobjaditionalimp = aditionalimpdini.sudo().create({
                        'position': aditional["Position"],
                        'value': aditional["Value"]
                    })
                    objaditionalimp.append(rassobjaditionalimp.id)
            #Creación campos arreglo detalle
            if dini:          
                objdetalles = []
                objdetallesaditional = []
                detallesdini = http.request.env["report_rass.documentlines"]
                detallesadi = http.request.env["report_rass.documentlinesadi"]
                for detalles in dini["detalle"]:
                    rassobjdetalles = detallesdini.sudo().create({
                        'IdDocumentLine': detalles["IdDocumentoDetalle"],
                        'IdDocumentTributario': detalles["IdDocumentoTributario"],
                        'CodeAuxiliar': detalles["CodigoAxiliar"],
                        'Description': detalles["Description"],
                        'Quantity': detalles["Cantidad"],
                        'PriceUnit': detalles["PrecioUnitario"],
                        'Discount': detalles["Descuento"],
                        'TotalPriceWithOutTax': detalles["PrecioTotalSinImpuesto"],
                        'Discount': detalles["Descuento"],
                        'PercentIva': detalles["PorcentajeIva"]
                    })
                    objdetalles.append(rassobjdetalles.id)
                    #Creación adicionales de detalle
                    for detallesadd in detalles["AdditionalInfo"]:
                        rassobjdetallesadi = detallesadi.sudo().create({
                            'position': detallesadd["Position"],
                            'value': detallesadd["Value"]
                        })
                        objdetallesaditional.append(rassobjdetallesadi.id)
                
                rassobjdetalles.write({
                        'DocumentdetalleAditional':[(6,0,objdetallesaditional)]
                        })   
            #Creación de los impuestos detalle              
            if dini:
                imp_detalle = http.request.env["report_rass.impuestos_detalle"]
                rassimp_detalle = imp_detalle.sudo().create({
                    'TotalIva': dini["impuesto_detalle"]["totiva"],
                    'TotalImpCons': dini["impuesto_detalle"]["totimpcons"],
                    'TotalImpRent': dini["impuesto_detalle"]["TotalImpCons"],
                    'PorcentIva': dini["impuesto_detalle"]["percentimpiva"],
                    'PercentImpCons': dini["impuesto_detalle"]["percentimpcons"],
                    'PercentImpRent': dini["impuesto_detalle"]["percentimprenta"]
                })
            
            #Creación de los impuestos detalle2             
            if dini:
                imp_detalle2 = http.request.env["report_rass.impuestos_detalle2"]
                rassimp_detalle2 = imp_detalle2.sudo().create({
                    'IdTax': dini["impuesto_detalle2"]["IdImpuesto"],
                    'BaseImponible': dini["impuesto_detalle2"]["BaseImponible"],
                    'ValueTax': dini["impuesto_detalle2"]["Valor"],
                    'TarifeTax': dini["impuesto_detalle2"]["Tarifa"],
                    'QuantityImpLine': dini["impuesto_detalle2"]["CantidaImpuestoDetalle"],
                    'BaseUniMesureLine': dini["impuesto_detalle2"]["BaseUnidadMedidaDetalle"],
                    'QuantityImpXUniLine': dini["impuesto_detalle2"]["CantImpuestoporUnidadDetalle"],
                    'PercentImpLine': dini["impuesto_detalle2"]["PorcentajeImpuestoDetalle"]
                })

            #Creación de los estado cuenta            
            if dini:
                estado_cuenta = http.request.env["report_rass.estado_cuenta"]
                rassestado_cuenta = estado_cuenta.sudo().create({
                    'IdDocumentoTributario': dini["estado_cuenta"]["IdDocumentoTributario"],
                    'StateAccount': dini["estado_cuenta"]["EstadoCuenta"]
                })

            #autocommit
            http.request.env.cr.commit() 
            try:
                #_logger.info('parametros %s', args)
                #validate = self.validateAuthorization(http.request)
                #if validate == True:
                if dini:
                    #_logger.info("dini currency %s", dini["cabecera"]["IdBusiness"])
                    _logger.info("diniii %s", dini["impuesto_detalle"]["totiva"])
                    diniobj = http.request.env["report_rass.dini"]
                    rassobj = diniobj.sudo().create({
                        'IdDocumentTributario': dini["cabecera"]["IdDocumentoTributario"],
                        'TypeIdentification': dini["cabecera"]["TipoIdentificacion"],
                        'Identification': dini["cabecera"]["Identificacion"],
                        'SocialReasonBuyer': dini["cabecera"]["RazonSocialComprador"],
                        'TypeEmision': dini["cabecera"]["TipoEmision"],
                        'SocialReason': dini["cabecera"]["RazonSocial"],
                        'Cufe': dini["cabecera"]["Cufe"],
                        'DocumentNumber': dini["cabecera"]["NumeroDocumento"],
                        'DateEmision': dini["cabecera"]["FechaEmision"],
                        'AddressMatriz': dini["cabecera"]["DireccionMatriz"],
                        'TotalWithOutTax': dini["cabecera"]["TotalSinImpuestos"],
                        'TotalDiscount': dini["cabecera"]["TotalDescuento"],
                        'TotalAmount': dini["cabecera"]["ImporteTotal"],
                        'MotiveNoteCredit': dini["cabecera"]["MotivoNotaCredito"],
                        'TaxTotal': dini["cabecera"]["IvaTotal"],
                        'IdClient': dini["cabecera"]["CodigoCliente"],
                        'Address': dini["cabecera"]["Direccion"],
                        'IdCompany': dini["cabecera"]["IdEmpresa"],
                        'TotalProduct': dini["cabecera"]["TotalProductos"],
                        'BaseTax': dini["cabecera"]["BaseImponibleIva"],
                        'IdDocument': dini["cabecera"]["CodigoDocumento"],
                        'TypeDocument': dini["cabecera"]["TipoDocumento"],
                        'BaseTaxC': dini["cabecera"]["BaseIvaC"],
                        'AmountTotalCal': dini["cabecera"]["ImporteTotalCal"],
                        'Reference1': dini["cabecera"]["Referencia1"],
                        'Reference2': dini["cabecera"]["Referencia2"],
                        'NameContribuyente': dini["cabecera"]["NombreContribuyente"],
                        'IdentificationContribuyente': dini["cabecera"]["IdentificacionContribuyente"],
                        'Prefix': dini["cabecera"]["Prefix"],
                        'Neighborhood': dini["cabecera"]["Barrio"],
                        'City': dini["cabecera"]["Ciudad"],
                        'Department': dini["cabecera"]["Depto"],
                        'ValueNeto': dini["cabecera"]["ValorNeto"],
                        'SinceNumeration': dini["cabecera"]["NumeracionDesde"],
                        'UntilNumeration': dini["cabecera"]["NumeracionHasta"],
                        'BillingAuthorization': dini["cabecera"]["AutorizacionFacturacion"],
                        'SinceBillingAuthorization': dini["cabecera"]["AutorizacionFacturacionDesde"],
                        'UntilBillingAuthorization': dini["cabecera"]["AutorizacionFacturacionHasta"],
                        'NumberRelatedDocument': dini["cabecera"]["NumberRelatedDocument"],
                        'DateEmisionInvoice': dini["cabecera"]["FechaEmisionFactura"],
                        'Telephone1': dini["cabecera"]["Telefono1"],
                        'TelephoneBuyer': dini["cabecera"]["TelefonoComprador"],
                        'Currency': dini["cabecera"]["Moneda"],
                        'Email': dini["cabecera"]["EmailAdquiriente"],
                        'Country': dini["cabecera"]["Pais"]                                         
                    })
                    rassobj.write({
                        'QR':rassimages.id,
                        'AdditionalInfo':[(6,0,objaditional)],
                        'AdditionalInfoImpuestos':[(6,0,objaditionalimp)],
                        'DocumentLines':[(6,0,objdetalles)],
                        'ImpuestosDetalle':rassimp_detalle.id,
                        'ImpuestosDetalle2':rassimp_detalle2.id,
                        'EstadoCuenta':rassestado_cuenta.id                        
                        })
                    # tod do
                    #commit para retornar el obj y registrar el obj de la caché
                    http.request.env.cr.commit() 
                    return rassobj

            except Exception, e:
                http.request.env.cr.rollback() 
                return json.dumps({
                    "userMessage": "La peticion incorrecta al guardar",
                    "error": str(e)
                })                 