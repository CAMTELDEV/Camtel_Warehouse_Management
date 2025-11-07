{
    'name': 'CAMTEL Dashboard',
    'version': '19.0.1.0.0',
    'category': 'Warehouse',
    'summary': 'Comprehensive Dashboard for Warehouse Management Analytics',
    'description': """
        CAMTEL Warehouse Management Dashboard
        ======================================

        Provides comprehensive analytics and insights for:
        * Stock and Inventory Management
        * Purchase Order Analysis
        * Inter-Warehouse Movements
        * Real-time KPIs and Metrics
        * Visual Charts and Graphs

        Features:
        ---------
        * Interactive dashboard with multiple chart types
        * Inventory value and turnover analysis
        * Purchase order tracking and performance
        * Stock movement analytics
        * Warehouse efficiency metrics
    """,
    'author': 'CAMTEL',
    'website': 'https://www.camtel.cm',
    'depends': [
        'base',
        'stock',
        'purchase',
        'web',
        'camtel_core',  # For warehouse access control
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/dashboard_views.xml',
        'views/stock_analytics_views.xml',
        'views/purchase_analytics_views.xml',
        'views/movement_analytics_views.xml',
        'views/menu_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'camtel_dashboard/static/src/css/dashboard.css',
            'camtel_dashboard/static/src/js/dashboard.js',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
