# -*- coding: utf-8 -*-

from openerp import api, fields, models, _
from openerp.exceptions import ValidationError


class ConfigReport(models.Model):
    _name = "report_rass.configuration"
    _description = 'Report'

    BusinessName = fields.Char(string="Nombre Compañía IFactura")
    BusinessId = fields.Char(string="Nit compañía IFactura")
    InvoiceType = fields.Selection([('factura venta', 'Factura Venta'), ('nota credito', 'Nota Débito'),('nota debito', 'Nota Crédito')],string="Tipo Factura")
    TemplateBusiness = fields.Many2one('ir.actions.report.xml', string="Plantilla por compañía")

    


class ConvertDini(models.Model):
    _name = "report_rass.dini"
    _description = 'Report Dini'

    QR = fields.Many2one('report_rass.images', string='Código QR')
    IdDocumentTributario = fields.Char(string='Código documento tributario', required=True)
    TypeIdentification = fields.Char(string='Tipo Identificación')
    Identification = fields.Char(string='Identificación', required=True)
    SocialReasonBuyer = fields.Char(string='Razon social comprador')
    TypeEmision = fields.Char(string='Tipo emisión')
    SocialReason = fields.Char(string='Razon social')
    Cufe = fields.Char(string='Cufe', required=True)
    DocumentNumber = fields.Char(string='Número documento')
    DateEmision = fields.Date(string='Fecha emisión', required=True)
    AddressMatriz = fields.Char(string='Dirección matriz')
    TotalWithOutTax = fields.Float(string='Total sin impuestos')    
    TotalDiscount = fields.Float(string='Total descuento')
    TotalAmount = fields.Float(string='Importe total')
    MotiveNoteCredit = fields.Char(string='Nota')
    TaxTotal = fields.Float(string='Iva total')
    IdClient = fields.Char(string='Código cliente')
    Address = fields.Char(string='Dirección')
    IdCompany = fields.Char(string='Código empresa')
    TotalProduct = fields.Char(string='Totl productos')
    BaseTax = fields.Char(string='Base imponible iva')
    IdDocument = fields.Char(string='Código documento')
    TypeDocument = fields.Char(string='Tipo documento')
    BaseTaxC = fields.Float(string='Total iva C')
    TarifeTaxC = fields.Float(string='Tarifa iva C')
    AmountTotalCal = fields.Float(string='Total importe Cal')
    Reference1 = fields.Char(string='Referencia 1')
    Reference2 = fields.Char(string='Referencia 2')
    #CodeQr = fields.Binary()
    NameContribuyente = fields.Char(string='Nombre contribuyente')
    IdentificationContribuyente = fields.Char(string='Identificación contribuyente')
    AdditionalInfo = fields.Many2many('report_rass.aditional', string='Adicionales cabecera')
    Prefix = fields.Char(string='Prefijo')
    Neighborhood = fields.Char(string='Barrio')
    City = fields.Char(string='Ciudad')
    ValueNeto = fields.Float(string='Valor Neto')
    SinceNumeration = fields.Char(string='Numeracion desde')
    UntilNumeration = fields.Char(string='Numeracion hasta')
    BillingAuthorization = fields.Char(string='Autorización de facturación')
    SinceBillingAuthorization = fields.Char(string='Autorización de facturación desde')
    UntilBillingAuthorization = fields.Char(string='Autorización de facturación hasta')
    NumberRelatedDocument = fields.Char(string='NumberRelatedDocument')
    DateEmisionInvoice = fields.Char(string='Fecha emisión factura')
    Telephone1 = fields.Integer(string='Teléfono 1')
    TelephoneBuyer = fields.Integer(string='Teléfono comprador')
    Currency = fields.Char(string='Moneda')
    Email = fields.Char(string='Correo')
    Country = fields.Char(string='País')
    AdditionalInfoImpuestos = fields.Many2many('report_rass.aditionalimp', string='Adicionales impuestos cabecera')
    DocumentLines = fields.Many2many('report_rass.documentlines', string='Detalles')
    ImpuestosDetalle = fields.Many2one('report_rass.impuestos_detalle', string='Impuestos detalle')
    ImpuestosDetalle2 = fields.Many2one('report_rass.impuestos_detalle2', string='Impuestos detalle2')
    EstadoCuenta = fields.Many2one('report_rass.estado_cuenta', string='Estado cuenta')

class Images(models.Model):
    _name = "report_rass.images"
    _description = 'Report Dini Images'

    CodeQr = fields.Binary(string='Código QR')

class AdditionalInformation(models.Model):
    _name = "report_rass.aditional"
    _description = 'Report Dini Aditional'

    position = fields.Integer(string='Posición')
    value = fields.Char(string='Valor')
   #to DO constraint

class AdditionalImpuestos(models.Model):
    _name = "report_rass.aditionalimp"
    _description = 'Report Dini Aditional Impuestos'

    position = fields.Integer(string='Posición')
    value = fields.Char(string='Valor')
   #to DO constraint
        
class DocumentLines(models.Model):
    _name = "report_rass.documentlines"
    _description = 'Report Dini document lines'

    IdDocumentLine = fields.Char(string='Código detalle')
    IdDocumentTributario = fields.Char(string='Código documento tributario')
    CodeAuxiliar = fields.Char(string='Código auxiliar')
    Description = fields.Char(string='Descripción')
    Quantity = fields.Integer(string='Cantidad')
    PriceUnit = fields.Float(string='Precio unitario')
    Discount = fields.Float(string='Descuento')
    TotalPriceWithOutTax = fields.Float(string='Precio total sin impuesto')
    DocumentdetalleAditional = fields.Many2many('report_rass.documentlinesadi', string='Adicionales detalle')
    PercentIva = fields.Float(string='Porcentaje iva')
    #to DO constraint

class DocumentLinesAditionalInformation(models.Model):
    _name = "report_rass.documentlinesadi"
    _description = 'Report Dini document lines aditional'

    position = fields.Integer(string='Posición')
    value = fields.Char(string='Valor')
    #to DO constraint

class ImpuestosDetalle(models.Model):
    _name = "report_rass.impuestos_detalle"
    _description = 'Report Dini document lines'

    TotalIva = fields.Float(string='Total iva')
    TotalImpCons = fields.Float(string='Total impuesto consumo')
    TotalImpRent = fields.Float(string='Total impuesto renta')
    PorcentIva = fields.Float(string='Porcentaje iva')
    PercentImpCons = fields.Float(string='Porcentaje impuesto consumo')
    PercentImpRent = fields.Float(string='Porcentaje impuesto renta')

class ImpuestosDetalle2(models.Model):
    _name = "report_rass.impuestos_detalle2"
    _description = 'Report Dini document lines'

    IdTax = fields.Char(string='Código impuesto')
    BaseImponible = fields.Float(string='Base imponible')
    ValueTax = fields.Float(string='TValor impuesto')
    TarifeTax = fields.Float(string='Tarifa impuesto')
    QuantityImpLine = fields.Integer(string='Cantidad impuesto detalle')
    BaseUniMesureLine = fields.Float(string='Base unidad medida detalle')
    QuantityImpXUniLine = fields.Integer(string='Cantidad impuesto por unidad')
    PercentImpLine = fields.Float(string='Porcentaje impuesto detalle')

class EstadoCuenta(models.Model):
    _name = "report_rass.estado_cuenta"
    _description = 'Report Dini estado cuenta'

    IdDocumentoTributario = fields.Char(string='Código documento tributario')
    StateAccount = fields.Char(string='Estado cuenta')