"""Stock Analytics Model for Inventory Insights"""

from odoo import fields, models, tools


class CamtelStockAnalytics(models.Model):
    """Analytics model for stock and inventory data"""

    _name = 'camtel.stock.analytics'
    _description = 'Stock Analytics'
    _auto = False  # SQL view, not a regular table
    _order = 'date desc'

    # Dimensions
    date = fields.Date(string='Date', readonly=True)
    product_id = fields.Many2one('product.product', string='Product', readonly=True)
    product_tmpl_id = fields.Many2one('product.template', string='Product Template', readonly=True)
    category_id = fields.Many2one('product.category', string='Category', readonly=True)
    warehouse_id = fields.Many2one('stock.warehouse', string='Warehouse', readonly=True)
    location_id = fields.Many2one('stock.location', string='Location', readonly=True)
    company_id = fields.Many2one('res.company', string='Company', readonly=True)

    # Measures
    quantity = fields.Float(string='Quantity On Hand', readonly=True)
    available_quantity = fields.Float(string='Available Quantity', readonly=True)
    incoming_quantity = fields.Float(string='Incoming Quantity', readonly=True)
    outgoing_quantity = fields.Float(string='Outgoing Quantity', readonly=True)
    inventory_value = fields.Monetary(string='Inventory Value', readonly=True, currency_field='currency_id')

    currency_id = fields.Many2one('res.currency', string='Currency', readonly=True)

    def init(self):
        """Create SQL view for stock analytics"""
        tools.drop_view_if_exists(self.env.cr, self._table)
        query = """
            CREATE OR REPLACE VIEW camtel_stock_analytics AS (
                SELECT
                    row_number() OVER () as id,
                    CURRENT_DATE as date,
                    sq.product_id,
                    pp.product_tmpl_id,
                    pt.categ_id as category_id,
                    sl.warehouse_id,
                    sq.location_id,
                    sq.company_id,
                    sq.quantity,
                    (sq.quantity - sq.reserved_quantity) as available_quantity,
                    COALESCE(incoming.qty, 0) as incoming_quantity,
                    COALESCE(outgoing.qty, 0) as outgoing_quantity,
                    sq.quantity * COALESCE(pt.list_price, 0) as inventory_value,
                    rc.id as currency_id
                FROM
                    stock_quant sq
                    LEFT JOIN product_product pp ON sq.product_id = pp.id
                    LEFT JOIN product_template pt ON pp.product_tmpl_id = pt.id
                    LEFT JOIN stock_location sl ON sq.location_id = sl.id
                    LEFT JOIN res_company comp ON sq.company_id = comp.id
                    LEFT JOIN res_currency rc ON comp.currency_id = rc.id
                    LEFT JOIN LATERAL (
                        SELECT SUM(sm.product_uom_qty) as qty
                        FROM stock_move sm
                        WHERE sm.product_id = sq.product_id
                        AND sm.location_dest_id = sq.location_id
                        AND sm.state IN ('assigned', 'waiting', 'confirmed')
                    ) incoming ON TRUE
                    LEFT JOIN LATERAL (
                        SELECT SUM(sm.product_uom_qty) as qty
                        FROM stock_move sm
                        WHERE sm.product_id = sq.product_id
                        AND sm.location_id = sq.location_id
                        AND sm.state IN ('assigned', 'waiting', 'confirmed')
                    ) outgoing ON TRUE
                WHERE
                    pt.type = 'product'
                    AND sl.usage = 'internal'
            )
        """
        self.env.cr.execute(query)
