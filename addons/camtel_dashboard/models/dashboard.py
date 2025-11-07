"""Main Dashboard Model with KPIs and Analytics"""

from odoo import api, fields, models


class CamtelDashboard(models.Model):
    """Main dashboard model providing warehouse management KPIs"""

    _name = 'camtel.dashboard'
    _description = 'CAMTEL Warehouse Dashboard'
    _order = 'date desc'

    name = fields.Char(string='Dashboard Name', required=True, default='Warehouse Dashboard')
    date = fields.Date(string='Date', default=fields.Date.today, required=True)
    warehouse_id = fields.Many2one('stock.warehouse', string='Warehouse')

    # Inventory KPIs
    total_inventory_value = fields.Monetary(
        string='Total Inventory Value',
        compute='_compute_inventory_kpis',
        currency_field='currency_id'
    )
    total_products = fields.Integer(
        string='Total Products',
        compute='_compute_inventory_kpis'
    )
    low_stock_products = fields.Integer(
        string='Low Stock Products',
        compute='_compute_inventory_kpis'
    )
    out_of_stock_products = fields.Integer(
        string='Out of Stock Products',
        compute='_compute_inventory_kpis'
    )

    # Purchase Order KPIs
    pending_po_count = fields.Integer(
        string='Pending Purchase Orders',
        compute='_compute_purchase_kpis'
    )
    pending_po_value = fields.Monetary(
        string='Pending PO Value',
        compute='_compute_purchase_kpis',
        currency_field='currency_id'
    )
    received_po_count = fields.Integer(
        string='Received POs (This Month)',
        compute='_compute_purchase_kpis'
    )

    # Movement KPIs
    incoming_shipments = fields.Integer(
        string='Incoming Shipments',
        compute='_compute_movement_kpis'
    )
    outgoing_shipments = fields.Integer(
        string='Outgoing Shipments',
        compute='_compute_movement_kpis'
    )
    internal_transfers = fields.Integer(
        string='Internal Transfers',
        compute='_compute_movement_kpis'
    )

    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        default=lambda self: self.env.company.currency_id
    )

    @api.depends('warehouse_id', 'date')
    def _compute_inventory_kpis(self):
        """Compute inventory-related KPIs"""
        for record in self:
            domain = [('product_id.type', '=', 'product')]

            if record.warehouse_id:
                domain.append(('warehouse_id', '=', record.warehouse_id.id))

            # Get all stock quants
            quants = self.env['stock.quant'].search(domain)

            # Total inventory value
            record.total_inventory_value = sum(
                quant.quantity * quant.product_id.standard_price
                for quant in quants
            )

            # Total unique products
            record.total_products = len(quants.mapped('product_id'))

            # Low stock and out of stock (simplified - comparing to reordering rule)
            out_of_stock = 0
            low_stock = 0

            for quant in quants:
                if quant.quantity <= 0:
                    out_of_stock += 1
                elif quant.quantity < 10:  # Simplified threshold
                    low_stock += 1

            record.out_of_stock_products = out_of_stock
            record.low_stock_products = low_stock

    @api.depends('warehouse_id', 'date')
    def _compute_purchase_kpis(self):
        """Compute purchase order KPIs"""
        for record in self:
            domain = []

            if record.warehouse_id:
                picking_type = self.env['stock.picking.type'].search([
                    ('warehouse_id', '=', record.warehouse_id.id),
                    ('code', '=', 'incoming')
                ], limit=1)
                if picking_type:
                    domain.append(('picking_type_id', '=', picking_type.id))

            # Pending purchase orders
            pending_domain = domain + [('state', 'in', ['draft', 'sent', 'to approve'])]
            pending_pos = self.env['purchase.order'].search(pending_domain)
            record.pending_po_count = len(pending_pos)
            record.pending_po_value = sum(pending_pos.mapped('amount_total'))

            # Received this month
            date_from = fields.Date.today().replace(day=1)
            received_domain = domain + [
                ('state', '=', 'purchase'),
                ('date_approve', '>=', date_from)
            ]
            record.received_po_count = self.env['purchase.order'].search_count(received_domain)

    @api.depends('warehouse_id', 'date')
    def _compute_movement_kpis(self):
        """Compute stock movement KPIs"""
        for record in self:
            domain = [('state', 'not in', ['done', 'cancel'])]

            if record.warehouse_id:
                domain.append(('location_id.warehouse_id', '=', record.warehouse_id.id))

            pickings = self.env['stock.picking'].search(domain)

            record.incoming_shipments = len(pickings.filtered(
                lambda p: p.picking_type_code == 'incoming'
            ))
            record.outgoing_shipments = len(pickings.filtered(
                lambda p: p.picking_type_code == 'outgoing'
            ))
            record.internal_transfers = len(pickings.filtered(
                lambda p: p.picking_type_code == 'internal'
            ))

    def action_view_inventory(self):
        """Open inventory analysis"""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Inventory Analysis',
            'res_model': 'camtel.stock.analytics',
            'view_mode': 'graph,pivot,list',
            'domain': [('warehouse_id', '=', self.warehouse_id.id)] if self.warehouse_id else [],
            'context': {'search_default_group_by_product': 1}
        }

    def action_view_purchases(self):
        """Open purchase analysis"""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Purchase Analysis',
            'res_model': 'camtel.purchase.analytics',
            'view_mode': 'graph,pivot,list',
            'domain': [],
            'context': {'search_default_group_by_month': 1}
        }

    def action_view_movements(self):
        """Open movement analysis"""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Movement Analysis',
            'res_model': 'stock.picking',
            'view_mode': 'graph,pivot,list,form',
            'domain': [('warehouse_id', '=', self.warehouse_id.id)] if self.warehouse_id else [],
            'context': {'search_default_todo': 1}
        }
