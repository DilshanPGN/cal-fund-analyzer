/**
 * Chart Component
 * Manages Chart.js visualization with clean encapsulation
 * Implements the Component Pattern
 */

class ChartComponent {
    /**
     * Initialize Chart Component
     * @param {HTMLCanvasElement} canvas - Canvas element for chart
     * @param {Object} config - Configuration object
     */
    constructor(canvas, config) {
        this.canvas = canvas;
        this.config = config.chart;
        this.chart = null;
        this.currentData = null;
    }

    /**
     * Initialize the chart
     * @param {Object} options - Chart initialization options
     */
    initialize(options = {}) {
        const defaultOptions = {
            type: 'line',
            data: {
                labels: [],
                datasets: [{
                    label: 'Price (LKR)',
                    data: [],
                    borderColor: this.config.defaultColors.primary,
                    backgroundColor: this.config.defaultColors.background,
                    borderWidth: 2,
                    tension: 0.1,
                    pointRadius: 4,
                    pointHoverRadius: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                animation: this.config.animation,
                plugins: {
                    legend: {
                        display: true,
                        position: 'top'
                    },
                    tooltip: {
                        mode: 'index',
                        intersect: false,
                        callbacks: {
                            label: (context) => {
                                return `Price: ${context.parsed.y.toFixed(4)} LKR`;
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        type: 'time',
                        time: {
                            unit: 'month',
                            displayFormats: {
                                month: 'MMM yyyy'
                            }
                        },
                        title: {
                            display: true,
                            text: 'Date'
                        }
                    },
                    y: {
                        title: {
                            display: true,
                            text: 'Price (LKR)'
                        },
                        beginAtZero: false
                    }
                }
            }
        };

        const mergedOptions = this._deepMerge(defaultOptions, options);
        this.chart = new Chart(this.canvas, mergedOptions);
    }

    /**
     * Update chart with new data
     * @param {Array} dates - Array of date strings
     * @param {Array} prices - Array of price values
     * @param {string} label - Dataset label
     */
    updateData(dates, prices, label = 'Price (LKR)') {
        if (!this.chart) {
            this.initialize();
        }

        // Convert dates to Date objects
        const dateObjects = dates.map(d => new Date(d));

        this.chart.data.labels = dateObjects;
        this.chart.data.datasets[0].data = prices;
        this.chart.data.datasets[0].label = label;
        
        this.currentData = { dates, prices, label };
        this.chart.update();
    }

    /**
     * Update chart title
     * @param {string} title - New chart title
     */
    updateTitle(title) {
        if (!this.chart) return;
        
        if (!this.chart.options.plugins.title) {
            this.chart.options.plugins.title = { display: true };
        }
        
        this.chart.options.plugins.title.text = title;
        this.chart.update();
    }

    /**
     * Filter data by date range
     * @param {string} startDate - Start date (YYYY-MM-DD)
     * @param {string} endDate - End date (YYYY-MM-DD)
     */
    filterByDateRange(startDate, endDate) {
        if (!this.currentData) return;

        const start = new Date(startDate);
        const end = new Date(endDate);

        const filtered = this.currentData.dates.reduce((acc, date, index) => {
            const d = new Date(date);
            if (d >= start && d <= end) {
                acc.dates.push(date);
                acc.prices.push(this.currentData.prices[index]);
            }
            return acc;
        }, { dates: [], prices: [] });

        this.updateData(filtered.dates, filtered.prices, this.currentData.label);
    }

    /**
     * Reset chart to original data
     */
    reset() {
        if (!this.currentData) return;
        this.updateData(
            this.currentData.dates,
            this.currentData.prices,
            this.currentData.label
        );
    }

    /**
     * Destroy chart instance
     */
    destroy() {
        if (this.chart) {
            this.chart.destroy();
            this.chart = null;
            this.currentData = null;
        }
    }

    /**
     * Export chart as image
     * @returns {string} Base64 encoded image
     */
    exportAsImage() {
        if (!this.chart) return null;
        return this.canvas.toDataURL('image/png');
    }

    /**
     * Get current visible data range
     * @returns {Object} Visible range info
     */
    getVisibleRange() {
        if (!this.chart || !this.currentData) return null;

        const xScale = this.chart.scales.x;
        const min = new Date(xScale.min);
        const max = new Date(xScale.max);

        return {
            startDate: min.toISOString().split('T')[0],
            endDate: max.toISOString().split('T')[0],
            dataPoints: this.currentData.dates.filter(d => {
                const date = new Date(d);
                return date >= min && date <= max;
            }).length
        };
    }

    /**
     * Deep merge objects
     * @private
     */
    _deepMerge(target, source) {
        const output = { ...target };
        if (this._isObject(target) && this._isObject(source)) {
            Object.keys(source).forEach(key => {
                if (this._isObject(source[key])) {
                    if (!(key in target)) {
                        Object.assign(output, { [key]: source[key] });
                    } else {
                        output[key] = this._deepMerge(target[key], source[key]);
                    }
                } else {
                    Object.assign(output, { [key]: source[key] });
                }
            });
        }
        return output;
    }

    /**
     * Check if value is object
     * @private
     */
    _isObject(item) {
        return item && typeof item === 'object' && !Array.isArray(item);
    }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ChartComponent;
}

