/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component } from "@odoo/owl";

/**
 * CAMTEL Dashboard JavaScript
 *
 * This module provides additional interactivity for the dashboard.
 * Currently handles auto-refresh and dynamic updates.
 */

// Dashboard refresh functionality
class DashboardController {
    setup() {
        // Auto-refresh interval (optional)
        this.refreshInterval = null;
    }

    startAutoRefresh(interval = 300000) {
        // Refresh every 5 minutes by default
        if (this.refreshInterval) {
            clearInterval(this.refreshInterval);
        }
        this.refreshInterval = setInterval(() => {
            this.refresh();
        }, interval);
    }

    stopAutoRefresh() {
        if (this.refreshInterval) {
            clearInterval(this.refreshInterval);
            this.refreshInterval = null;
        }
    }

    refresh() {
        // Trigger a reload of the current view
        if (this.model && this.model.load) {
            this.model.load();
        }
    }
}

// Export for use in other modules
export default {
    DashboardController,
};

console.log('CAMTEL Dashboard module loaded');
