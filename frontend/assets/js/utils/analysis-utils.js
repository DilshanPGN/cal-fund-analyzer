/**
 * Analysis Utilities
 * Helper functions for fund performance analysis
 */

class AnalysisUtils {
    /**
     * Calculate basic statistics
     * @param {Array<number>} prices - Array of prices
     * @returns {Object} Statistics object
     */
    static calculateStats(prices) {
        if (!prices || prices.length === 0) {
            return null;
        }

        const min = Math.min(...prices);
        const max = Math.max(...prices);
        const sum = prices.reduce((a, b) => a + b, 0);
        const avg = sum / prices.length;
        
        const startPrice = prices[0];
        const endPrice = prices[prices.length - 1];
        const totalReturn = ((endPrice - startPrice) / startPrice) * 100;

        return {
            min: min.toFixed(4),
            max: max.toFixed(4),
            avg: avg.toFixed(4),
            return: totalReturn.toFixed(2),
            returnValue: totalReturn,
            count: prices.length
        };
    }

    /**
     * Calculate volatility (standard deviation of returns)
     * @param {Array<number>} prices - Array of prices
     * @returns {number} Annualized volatility percentage
     */
    static calculateVolatility(prices) {
        if (prices.length < 2) return 0;

        // Calculate returns
        const returns = [];
        for (let i = 1; i < prices.length; i++) {
            returns.push((prices[i] - prices[i-1]) / prices[i-1]);
        }

        // Calculate standard deviation
        const avgReturn = returns.reduce((a, b) => a + b, 0) / returns.length;
        const variance = returns.reduce((sum, r) => sum + Math.pow(r - avgReturn, 2), 0) / returns.length;
        const stdDev = Math.sqrt(variance);

        // Annualize (assuming 252 trading days)
        return stdDev * Math.sqrt(252) * 100;
    }

    /**
     * Analyze trend using linear regression
     * @param {Array<number>} prices - Array of prices
     * @returns {Object} Trend analysis
     */
    static analyzeTrend(prices) {
        if (prices.length < 2) {
            return { direction: 'Unknown', strength: 0, description: 'Insufficient data' };
        }

        const n = prices.length;
        const indices = Array.from({length: n}, (_, i) => i);
        
        // Calculate linear regression
        const sumX = indices.reduce((a, b) => a + b, 0);
        const sumY = prices.reduce((a, b) => a + b, 0);
        const sumXY = indices.reduce((sum, x, i) => sum + x * prices[i], 0);
        const sumX2 = indices.reduce((sum, x) => sum + x * x, 0);
        
        const slope = (n * sumXY - sumX * sumY) / (n * sumX2 - sumX * sumX);
        const avgPrice = sumY / n;
        const trendStrength = Math.abs(slope) / avgPrice * 100;

        let direction = 'Sideways';
        let description = 'Relatively stable with minimal trend';

        if (slope > 0) {
            direction = 'Uptrend';
            description = `Strong upward trend with ${trendStrength.toFixed(2)}% growth rate`;
        } else if (slope < 0) {
            direction = 'Downtrend';
            description = `Declining trend with ${trendStrength.toFixed(2)}% decline rate`;
        }

        return {
            direction,
            strength: trendStrength.toFixed(2),
            description
        };
    }

    /**
     * Get contextual events for date range
     * @param {string} startDate - Start date
     * @param {string} endDate - End date
     * @param {Array} eventsConfig - Events configuration
     * @returns {Array} Array of events in range
     */
    static getContextualEvents(startDate, endDate, eventsConfig) {
        const start = new Date(startDate);
        const end = new Date(endDate);
        
        return eventsConfig.filter(event => {
            const eventDate = new Date(event.date);
            return eventDate >= start && eventDate <= end;
        });
    }

    /**
     * Generate insights based on analysis
     * @param {number} totalReturn - Total return percentage
     * @param {number} volatility - Volatility percentage
     * @param {Object} trend - Trend analysis
     * @param {Array} events - Contextual events
     * @returns {Array<string>} Array of insights
     */
    static generateInsights(totalReturn, volatility, trend, events) {
        const insights = [];

        // Performance insights
        if (totalReturn > 10) {
            insights.push('📈 Strong positive performance during this period');
        } else if (totalReturn > 5) {
            insights.push('📊 Moderate positive performance');
        } else if (totalReturn > 0) {
            insights.push('📉 Slight positive performance');
        } else if (totalReturn > -5) {
            insights.push('📉 Minor decline in performance');
        } else if (totalReturn > -10) {
            insights.push('📉 Moderate decline in performance');
        } else {
            insights.push('📉 Significant decline in performance');
        }

        // Volatility insights
        if (volatility > 30) {
            insights.push('⚡ High volatility period - significant price swings');
        } else if (volatility > 20) {
            insights.push('📊 Moderate volatility - some price fluctuations');
        } else {
            insights.push('📈 Low volatility - relatively stable period');
        }

        // Event insights
        const highImpactEvents = events.filter(e => e.impact === 'High');
        if (highImpactEvents.length > 0) {
            insights.push(`🎯 ${highImpactEvents.length} high-impact economic events occurred`);
            insights.push('💡 Performance likely influenced by major economic developments');
        }

        // Trend insights
        insights.push(`📊 ${trend.direction}: ${trend.description}`);

        return insights;
    }

    /**
     * Calculate moving average
     * @param {Array<number>} prices - Array of prices
     * @param {number} period - Period for moving average
     * @returns {Array<number>} Moving averages
     */
    static calculateMovingAverage(prices, period) {
        const result = [];
        
        for (let i = 0; i < prices.length; i++) {
            if (i < period - 1) {
                result.push(null);
            } else {
                const sum = prices.slice(i - period + 1, i + 1).reduce((a, b) => a + b, 0);
                result.push(sum / period);
            }
        }

        return result;
    }

    /**
     * Find significant price movements
     * @param {Array<number>} prices - Array of prices
     * @param {number} threshold - Threshold percentage for significance
     * @returns {Array<Object>} Significant movements
     */
    static findSignificantMovements(prices, threshold = 5) {
        const movements = [];

        for (let i = 1; i < prices.length; i++) {
            const change = ((prices[i] - prices[i-1]) / prices[i-1]) * 100;
            
            if (Math.abs(change) >= threshold) {
                movements.push({
                    index: i,
                    fromPrice: prices[i-1],
                    toPrice: prices[i],
                    change: change.toFixed(2),
                    direction: change > 0 ? 'up' : 'down'
                });
            }
        }

        return movements;
    }

    /**
     * Compare two periods
     * @param {Array<number>} period1 - First period prices
     * @param {Array<number>} period2 - Second period prices
     * @returns {Object} Comparison results
     */
    static comparePeriods(period1, period2) {
        const stats1 = this.calculateStats(period1);
        const stats2 = this.calculateStats(period2);

        if (!stats1 || !stats2) return null;

        return {
            period1: stats1,
            period2: stats2,
            returnDiff: (stats2.returnValue - stats1.returnValue).toFixed(2),
            avgDiff: (parseFloat(stats2.avg) - parseFloat(stats1.avg)).toFixed(4)
        };
    }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = AnalysisUtils;
}

