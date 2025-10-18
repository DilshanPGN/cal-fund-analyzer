/**
 * UI Components
 * Reusable UI helper functions and components
 */

class UIComponents {
    /**
     * Initialize UI Components
     * @param {Object} config - Configuration object
     */
    constructor(config) {
        this.config = config.ui;
    }

    /**
     * Show loading overlay
     * @param {string} message - Loading message
     */
    showLoading(message = 'Loading...') {
        const overlay = document.getElementById('loadingOverlay');
        const text = document.getElementById('loadingText');
        
        if (overlay && text) {
            text.textContent = message;
            overlay.style.display = 'flex';
        }
    }

    /**
     * Hide loading overlay
     */
    hideLoading() {
        const overlay = document.getElementById('loadingOverlay');
        if (overlay) {
            overlay.style.display = 'none';
        }
    }

    /**
     * Set status message
     * @param {string} message - Status message
     * @param {string} type - Status type (success, error, warning, info, loading)
     */
    setStatus(message, type = 'info') {
        const statusText = document.getElementById('statusText');
        const statusBar = document.getElementById('statusBar');
        
        if (statusText && statusBar) {
            statusText.textContent = message;
            statusBar.className = `status-bar status-${type}`;
        }
    }

    /**
     * Show toast notification
     * @param {string} message - Toast message
     * @param {string} type - Toast type (success, error, warning, info)
     * @param {number} duration - Display duration in ms
     */
    showToast(message, type = 'info', duration = null) {
        const toastDuration = duration || this.config.toastDuration;
        
        // Create toast element
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.textContent = message;
        
        // Add to document
        document.body.appendChild(toast);
        
        // Animate in
        setTimeout(() => toast.classList.add('toast-show'), 10);
        
        // Remove after duration
        setTimeout(() => {
            toast.classList.remove('toast-show');
            setTimeout(() => document.body.removeChild(toast), 300);
        }, toastDuration);
    }

    /**
     * Update stats display
     * @param {Object} stats - Statistics object
     */
    updateStats(stats) {
        const elements = {
            minPrice: document.getElementById('minPrice'),
            maxPrice: document.getElementById('maxPrice'),
            avgPrice: document.getElementById('avgPrice'),
            totalReturn: document.getElementById('totalReturn')
        };

        if (elements.minPrice) elements.minPrice.textContent = stats.min || '-';
        if (elements.maxPrice) elements.maxPrice.textContent = stats.max || '-';
        if (elements.avgPrice) elements.avgPrice.textContent = stats.avg || '-';
        if (elements.totalReturn) {
            elements.totalReturn.textContent = stats.return || '-';
            elements.totalReturn.className = stats.returnValue >= 0 ? 'positive' : 'negative';
        }
    }

    /**
     * Update fund info display
     * @param {Object} info - Fund information object
     */
    updateFundInfo(info) {
        const elements = {
            earliestDate: document.getElementById('earliestDate'),
            dataPoints: document.getElementById('dataPoints'),
            lastUpdated: document.getElementById('lastUpdated')
        };

        if (elements.earliestDate) elements.earliestDate.textContent = info.earliest || '-';
        if (elements.dataPoints) elements.dataPoints.textContent = info.points || '-';
        if (elements.lastUpdated) elements.lastUpdated.textContent = info.updated || '-';
    }

    /**
     * Update storage info display
     * @param {Object} storageInfo - Storage information object
     */
    updateStorageInfo(storageInfo) {
        const element = document.getElementById('storageUsed');
        if (element) {
            element.textContent = `${storageInfo.sizeKB} KB`;
        }
    }

    /**
     * Populate dropdown with options
     * @param {HTMLSelectElement} select - Select element
     * @param {Array} options - Array of options
     * @param {string} placeholder - Placeholder text
     */
    populateSelect(select, options, placeholder = '-- Select --') {
        select.innerHTML = `<option value="">${placeholder}</option>`;
        
        options.forEach((option, index) => {
            const opt = document.createElement('option');
            opt.value = typeof option === 'object' ? option.value : index;
            opt.textContent = typeof option === 'object' ? option.label : option;
            select.appendChild(opt);
        });
    }

    /**
     * Disable element
     * @param {HTMLElement} element - Element to disable
     */
    disable(element) {
        element.disabled = true;
        element.classList.add('disabled');
    }

    /**
     * Enable element
     * @param {HTMLElement} element - Element to enable
     */
    enable(element) {
        element.disabled = false;
        element.classList.remove('disabled');
    }

    /**
     * Show element
     * @param {HTMLElement} element - Element to show
     */
    show(element) {
        element.style.display = '';
        element.classList.remove('hidden');
    }

    /**
     * Hide element
     * @param {HTMLElement} element - Element to hide
     */
    hide(element) {
        element.style.display = 'none';
        element.classList.add('hidden');
    }

    /**
     * Scroll to element smoothly
     * @param {HTMLElement} element - Element to scroll to
     */
    scrollTo(element) {
        element.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }

    /**
     * Format number with commas
     * @param {number} num - Number to format
     * @param {number} decimals - Number of decimal places
     * @returns {string} Formatted number
     */
    formatNumber(num, decimals = 2) {
        return num.toFixed(decimals).replace(/\B(?=(\d{3})+(?!\d))/g, ',');
    }

    /**
     * Format percentage
     * @param {number} value - Value to format
     * @param {number} decimals - Number of decimal places
     * @returns {string} Formatted percentage
     */
    formatPercentage(value, decimals = 2) {
        return `${value >= 0 ? '+' : ''}${value.toFixed(decimals)}%`;
    }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = UIComponents;
}

