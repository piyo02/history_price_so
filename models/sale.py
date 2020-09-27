from odoo import api, exceptions, fields, models, _

import logging
_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit = "sale.order.line"

    @api.multi
    def get_history_price(self):
        ctx = dict(self.env.context)
        self.ensure_one()
        view = self.env.ref('history_price_so.sale_order_line_history')
        # serial = (self.has_tracking == 'serial')
        # only_create = False  # Check picking type in theory
        # show_reserved = any([x for x in self.move_lot_ids if x.quantity > 0.0])
        order_lines = self.env["sale.order.line"].search( [ ("product_id", "=", self.product_id.id ), ("order_id.partner_id", "=", self.order_id.partner_id.id ) ] )
        ids = sum( [order_lines.ids], [] ) 
        result = {
            # 'name': _('Register Lots'),
            'type': 'ir.actions.act_window',
            'res_model': 'sale.order.line',
            'view_type': 'tree',
            'view_mode': 'tree',
            'res_id': 'sale_order_line_history',
            # 'view_id': view.id,
            'target': 'new',
            # 'res_id': [ self.id ],
            'domain': "[('id','in',[" + ','.join(map(str, ids )) + "])]"
            # 'context': ctx,
        }
        _logger.warning(result)
        return result