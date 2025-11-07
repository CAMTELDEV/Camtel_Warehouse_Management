"""Purchase Analytics Model for PO Insights"""

from odoo import fields, models, tools


class CamtelPurchaseAnalytics(models.Model):
    """Analytics model for purchase order data"""

    _name = 'camtel.purchase.analytics'
    _description = 'Purchase Analytics'
    _auto = False  # SQL view
    _order = 'order_date desc'

    # Dimensions
    order_date = fields.Date(string='Order Date', readonly=True)
    date_approve = fields.Datetime(string='Confirmation Date', readonly=True)
    partner_id = fields.Many2one('res.partner', string='Vendor', readonly=True)
    user_id = fields.Many2one('res.users', string='Purchase Representative', readonly=True)
    company_id = fields.Many2one('res.company', string='Company', readonly=True)
    product_id = fields.Many2one('product.product', string='Product', readonly=True)
    product_tmpl_id = fields.Many2one('product.template', string='Product Template', readonly=True)
    category_id = fields.Many2one('product.category', string='Category', readonly=True)

    # Order info
    order_id = fields.Many2one('purchase.order', string='Purchase Order', readonly=True)
    state = fields.Selection([
        ('draft', 'RFQ'),
        ('sent', 'RFQ Sent'),
        ('to approve', 'To Approve'),
        ('purchase', 'Purchase Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled')
    ], string='Status', readonly=True)

    # Measures
    quantity = fields.Float(string='Quantity', readonly=True)
    qty_received = fields.Float(string='Received Qty', readonly=True)
    qty_invoiced = fields.Float(string='Billed Qty', readonly=True)
    unit_price = fields.Float(string='Unit Price', readonly=True)
    price_total = fields.Monetary(string='Total', readonly=True, currency_field='currency_id')
    price_subtotal = fields.Monetary(string='Untaxed Total', readonly=True, currency_field='currency_id')

    delay = fields.Float(string='Days to Confirm', readonly=True)
    delay_pass = fields.Float(string='Days to Receive', readonly=True)

    currency_id = fields.Many2one('res.currency', string='Currency', readonly=True)

    def init(self):
        """Create SQL view for purchase analytics"""
        tools.drop_view_if_exists(self.env.cr, self._table)
        query = """
            CREATE OR REPLACE VIEW camtel_purchase_analytics AS (
                SELECT
                    pol.id,
                    po.date_order as order_date,
                    po.date_approve,
                    po.partner_id,
                    po.user_id,
                    po.company_id,
                    pol.product_id,
                    pp.product_tmpl_id,
                    pt.categ_id as category_id,
                    po.id as order_id,
                    po.state,
                    pol.product_qty as quantity,
                    pol.qty_received,
                    pol.qty_invoiced,
                    pol.price_unit as unit_price,
                    pol.price_total,
                    pol.price_subtotal,
                    EXTRACT(EPOCH FROM (po.date_approve - po.date_order))/(24*60*60) as delay,
                    0 as delay_pass,
                    po.currency_id
                FROM
                    purchase_order_line pol
                    JOIN purchase_order po ON pol.order_id = po.id
                    JOIN product_product pp ON pol.product_id = pp.id
                    JOIN product_template pt ON pp.product_tmpl_id = pt.id
                WHERE
                    po.state != 'cancel'
            )
        """
        self.env.cr.execute(query)
