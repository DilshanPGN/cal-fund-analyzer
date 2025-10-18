/**
 * Date Utilities
 * Helper functions for date manipulation and formatting
 */

class DateUtils {
    /**
     * Format date to YYYY-MM-DD
     * @param {Date|string} date - Date to format
     * @returns {string} Formatted date string
     */
    static formatDate(date) {
        const d = new Date(date);
        const year = d.getFullYear();
        const month = String(d.getMonth() + 1).padStart(2, '0');
        const day = String(d.getDate()).padStart(2, '0');
        return `${year}-${month}-${day}`;
    }

    /**
     * Parse date string to Date object
     * @param {string} dateStr - Date string (YYYY-MM-DD)
     * @returns {Date} Date object
     */
    static parseDate(dateStr) {
        return new Date(dateStr);
    }

    /**
     * Get date N days ago
     * @param {number} days - Number of days
     * @returns {string} Date string
     */
    static getDaysAgo(days) {
        const date = new Date();
        date.setDate(date.getDate() - days);
        return this.formatDate(date);
    }

    /**
     * Get date N months ago
     * @param {number} months - Number of months
     * @returns {string} Date string
     */
    static getMonthsAgo(months) {
        const date = new Date();
        date.setMonth(date.getMonth() - months);
        return this.formatDate(date);
    }

    /**
     * Get date N years ago
     * @param {number} years - Number of years
     * @returns {string} Date string
     */
    static getYearsAgo(years) {
        const date = new Date();
        date.setFullYear(date.getFullYear() - years);
        return this.formatDate(date);
    }

    /**
     * Get today's date
     * @returns {string} Date string
     */
    static getToday() {
        return this.formatDate(new Date());
    }

    /**
     * Get yesterday's date
     * @returns {string} Date string
     */
    static getYesterday() {
        return this.getDaysAgo(1);
    }

    /**
     * Generate date range (1st and 15th of each month)
     * @param {string} startDate - Start date (YYYY-MM-DD)
     * @param {string} endDate - End date (YYYY-MM-DD)
     * @returns {Array<string>} Array of date strings
     */
    static generateDateRange(startDate, endDate) {
        const dates = [];
        const start = new Date(startDate);
        const end = new Date(endDate);
        const current = new Date(start);

        while (current <= end) {
            // Add 1st of month
            const firstDay = new Date(current.getFullYear(), current.getMonth(), 1);
            if (firstDay >= start && firstDay <= end) {
                dates.push(this.formatDate(firstDay));
            }

            // Add 15th of month
            const fifteenthDay = new Date(current.getFullYear(), current.getMonth(), 15);
            if (fifteenthDay >= start && fifteenthDay <= end) {
                dates.push(this.formatDate(fifteenthDay));
            }

            // Move to next month
            current.setMonth(current.getMonth() + 1);
        }

        // Add end date if not already included
        const endDateStr = this.formatDate(end);
        if (!dates.includes(endDateStr)) {
            dates.push(endDateStr);
        }

        return dates;
    }

    /**
     * Validate date string format
     * @param {string} dateStr - Date string to validate
     * @returns {boolean} True if valid
     */
    static isValidDate(dateStr) {
        const regex = /^\d{4}-\d{2}-\d{2}$/;
        if (!regex.test(dateStr)) return false;

        const date = new Date(dateStr);
        return date instanceof Date && !isNaN(date);
    }

    /**
     * Check if date is in range
     * @param {string} date - Date to check
     * @param {string} startDate - Start date
     * @param {string} endDate - End date
     * @returns {boolean} True if in range
     */
    static isDateInRange(date, startDate, endDate) {
        const d = new Date(date);
        const start = new Date(startDate);
        const end = new Date(endDate);
        return d >= start && d <= end;
    }

    /**
     * Get number of days between dates
     * @param {string} date1 - First date
     * @param {string} date2 - Second date
     * @returns {number} Number of days
     */
    static daysBetween(date1, date2) {
        const d1 = new Date(date1);
        const d2 = new Date(date2);
        const diffTime = Math.abs(d2 - d1);
        return Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    }

    /**
     * Format date for display
     * @param {string} dateStr - Date string
     * @returns {string} Formatted display string
     */
    static formatForDisplay(dateStr) {
        const date = new Date(dateStr);
        const options = { year: 'numeric', month: 'short', day: 'numeric' };
        return date.toLocaleDateString('en-US', options);
    }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = DateUtils;
}

