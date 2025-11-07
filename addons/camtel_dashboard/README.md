# CAMTEL Dashboard Module

## Overview

The **CAMTEL Dashboard** module provides comprehensive analytics and insights for warehouse management operations in Odoo 19. It offers real-time KPIs, interactive charts, and detailed analytics for inventory, purchase orders, and stock movements.

## Features

### 📊 Main Dashboard
- **Real-time KPI Cards** with beautiful gradient designs
- **Inventory Overview**: Total value, product count, low stock alerts, out-of-stock items
- **Purchase Order Metrics**: Pending orders, pending value, received orders
- **Movement Tracking**: Incoming shipments, outgoing shipments, internal transfers
- Interactive buttons to drill down into detailed analytics

### 📦 Inventory Analysis
- SQL-based analytics view for high performance
- Multiple visualization types: bar charts, pivot tables, detailed lists
- Filters for low stock, out of stock, incoming/outgoing quantities
- Group by product, category, warehouse, or location
- Track available quantity, incoming, and outgoing quantities
- Color-coded list views (red for out-of-stock, yellow for low stock)

### 🛒 Purchase Order Analytics
- Comprehensive purchase order insights
- Multiple chart types: bar, line, and pie charts
- Track order status, vendor performance, and procurement trends
- Analyze by vendor, product, category, or time period
- Monitor order delays and fulfillment metrics
- Filter by status: RFQ, To Approve, Purchase Order, Done

### 🚚 Stock Movement Analytics
- Inter-warehouse movement tracking
- Visualize incoming, outgoing, and internal transfers
- Timeline analysis with daily, weekly, and monthly views
- Filter by operation type, time period
- Group by operation type, partner, or scheduled date

## Installation

1. **Place the module** in your Odoo addons directory:
   ```
   addons/camtel_dashboard/
   ```

2. **Update the apps list**:
   - Go to Apps menu
   - Click "Update Apps List"

3. **Install the module**:
   ```bash
   ./odoo-bin -d your_database -i camtel_dashboard
   ```
   Or install through the Apps menu in Odoo interface.

## Usage

### Accessing the Dashboard

After installation, you'll find a new top-level menu called **"CAMTEL Dashboard"** with the following sub-menus:

1. **Dashboard** - Main KPI overview
2. **Analytics**
   - Inventory Analysis
   - Purchase Analysis
   - Movement Analysis

### Understanding the Dashboard

#### Main Dashboard
The main dashboard provides an at-a-glance view of your warehouse operations:

- **Inventory Section**: Shows total inventory value, number of products, low stock alerts, and out-of-stock items
- **Purchase Orders Section**: Displays pending orders, their total value, and orders received this month
- **Stock Movements Section**: Tracks incoming/outgoing shipments and internal transfers

You can filter by warehouse to see specific warehouse metrics.

#### Inventory Analysis
- Use **graph view** for visual trends by category or warehouse
- Use **pivot view** for cross-tabulated data analysis
- Use **list view** for detailed product-level information
- Apply filters to find low stock or out-of-stock items quickly

#### Purchase Analysis
- **Graph view**: Visualize purchase trends over time
- **Pivot view**: Analyze purchases by vendor, product, or time period
- **List view**: See detailed purchase order lines with quantities and values

#### Movement Analysis
- Track all stock movements with various chart types
- Filter by movement type (incoming/outgoing/internal)
- Group by time periods to see movement trends

## Technical Details

### Models

1. **camtel.dashboard** - Main dashboard model with computed KPIs
2. **camtel.stock.analytics** - SQL view for inventory analytics
3. **camtel.purchase.analytics** - SQL view for purchase analytics

### SQL Views

The module uses PostgreSQL views for optimal performance when analyzing large datasets:

- **camtel_stock_analytics**: Aggregates stock quants with product information
- **camtel_purchase_analytics**: Aggregates purchase order lines with vendor and product data

### Dependencies

- `base` - Odoo base module
- `stock` - Inventory management
- `purchase` - Purchase management
- `web` - Web interface
- `camtel_core` - CAMTEL core module (for warehouse access control)

### Permissions

Access rights are configured for:
- **Stock Users**: Read-only access to dashboards and analytics
- **Stock Managers**: Full access including create/update permissions for dashboards

## Customization

### Adding Custom KPIs

To add custom KPIs to the main dashboard:

1. Add computed fields to `camtel.dashboard` model in `models/dashboard.py`
2. Update the form view in `views/dashboard_views.xml` to display the new KPIs
3. Add corresponding CSS classes in `static/src/css/dashboard.css` for styling

### Modifying Analytics Views

The SQL views can be customized in:
- `models/stock_analytics.py` - Inventory analytics
- `models/purchase_analytics.py` - Purchase analytics

After modifying SQL views, upgrade the module to recreate them.

### Styling

Custom styles are defined in `static/src/css/dashboard.css`:
- KPI card colors and gradients
- Responsive design breakpoints
- Hover effects and animations

## Screenshots

The dashboard features:
- Modern, responsive design
- CAMTEL brand colors (#09AEEF primary color)
- Interactive charts and graphs
- Color-coded KPI cards
- Gradient backgrounds with hover effects

## Support

For issues or questions:
- Check the module logs in Odoo
- Verify all dependencies are installed
- Ensure proper access rights are configured

## Version History

- **19.0.1.0.0** - Initial release
  - Main dashboard with KPI cards
  - Inventory analytics
  - Purchase analytics
  - Movement analytics
  - Beautiful UI with CAMTEL branding

## License

LGPL-3

## Author

CAMTEL - Cameroon Telecommunications

---

**Note**: This module integrates seamlessly with the `camtel_core` module for warehouse-specific access control, ensuring users only see data for their assigned warehouses.
