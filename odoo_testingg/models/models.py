from odoo import models, fields, api

class Supplier(models.Model):
    _name = 'supplier'
    name = fields.Char(string='Name', required=True)
    material_ids = fields.One2many('material', 'supplier_id', string='Materials')

class Material(models.Model):
    _name = 'material'
    _description = 'Material for Sale'
    _rec_name = 'code'

    code = fields.Char(string='Material Code', required=True, index=True)
    name = fields.Char(string='Material Name', required=True)
    type = fields.Selection([('fabric', 'Fabric'), ('jeans', 'Jeans'), ('cotton', 'Cotton')], string='Material Type', required=True)
    buy_price = fields.Float(string='Material Buy Price', required=True, digits=(6, 2), help='Material Buy Price must be greater than or equal to 100')
    supplier_id = fields.Many2one('supplier', string='Related Supplier', required=True)

    @api.constrains('buy_price')
    def _check_buy_price(self):
        for material in self:
            if material.buy_price < 100:
                raise models.ValidationError('Material Buy Price must be greater than or equal to 100!')

