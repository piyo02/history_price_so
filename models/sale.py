from odoo import api, exceptions, fields, models, _

import logging
_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit = "sale.order.line"

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
        _logger.warning(result)
        return result