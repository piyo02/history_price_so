from odoo import api, exceptions, fields, models, _

import logging
_logger = logging.getLogger(__name__)

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    history_price_ids = fields.One2many('sale.order.line.history', 'line_id', string='Riwayat Harga Jual')

    @api.multi
    @api.depends('product_id')
    def get_history_price(self):
        order_lines = self.env["sale.order.line"].search( [ ("product_id", "=", self.product_id.id ), ("order_id.partner_id", "=", self.order_id.partner_id.id ) ] )
        ids = sum( [order_lines.ids], [] ) 
        result = {
            'type': 'ir.actions.act_window',
            'res_model': 'sale.order.line',
            'view_type': 'tree',
            'view_mode': 'tree',
            'res_id': 'sale_order_line_history',
            'target': 'new',
            'domain': "[('id','in',[" + ','.join(map(str, ids )) + "])]"
        }
        return result

    @api.multi
    @api.onchange('product_id')
    def record_history_price(self):
        lines = []
        order_lines = self.env["sale.order.line"].search( [ ("product_id", "=", self.product_id.id ), ("order_id.partner_id", "=", self.order_id.partner_id.id ) ] )
        for line in order_lines:
            val = {
                'order_id': line.order_id,
                'date': line.order_id.date_order,
                'product_id': line.product_id,
                'price_unit': line.price_unit
            }
            lines.append((0, 0, val))
        self.history_price_ids = lines

    @api.model
    def create(self, values):
        res = super(SaleOrderLine, self).create(values)
        res.update({
            'history_price_ids': None
        })
        return res

class SaleOrderLineHistory(models.Model):
    _name = 'sale.order.line.history'

    order_id = fields.Many2one('sale.order', string='Order Reference', required=True, ondelete='cascade', index=True, copy=False)
    date = fields.Date(string="Tanggal Pembelian")
    line_id = fields.Many2one('sale.order.line', string='Order Line Reference', required=True, ondelete='cascade', index=True, copy=False)
    product_id = fields.Many2one('product.product', string='Product', domain=[('sale_ok', '=', True)], change_default=True, ondelete='restrict', required=True)
    price_unit = fields.Integer(string='Harga')
