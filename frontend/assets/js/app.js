/**
 * CAL Fund Analyzer - Main Application
 * Simple version without ES6 modules
 */

class CALFundAnalyzer {
    constructor() {
        this.apiService = apiService;
        this.storageService = storageService;
        
        this.state = {
            currentFund: null,
            availableFunds: [],
            priceData: {},
            chart: null
        };
        
        this.init();
    }

    async init() {
        try {
            console.log('Initializing CAL Fund Analyzer...');
            this.setupEventListeners();
            this.setDefaultDates();
            await this.loadAvailableFunds();
            this.updateStorageInfo();
            this.setStatus('Ready. Select a fund and fetch data to begin.', 'success');
        } catch (error) {
            console.error('Initialization error:', error);
            this.setStatus('Failed to initialize application', 'error');
        }
    }

    setDefaultDates() {
        // Set default end date to today
        const endDateInput = document.getElementById('endDate');
        if (endDateInput) {
            endDateInput.value = new Date().toISOString().split('T')[0];
        }
        
        // Set default start date to 2 years ago
        const startDateInput = document.getElementById('startDate');
        if (startDateInput) {
            const twoYearsAgo = new Date();
            twoYearsAgo.setFullYear(twoYearsAgo.getFullYear() - 2);
            startDateInput.value = twoYearsAgo.toISOString().split('T')[0];
        }
    }

    setupEventListeners() {
        const fetchBtn = document.getElementById('fetchDataBtn');
        if (fetchBtn) {
            fetchBtn.addEventListener('click', () => this.fetchFundData());
        }

        const refreshBtn = document.getElementById('refreshDataBtn');
        if (refreshBtn) {
            refreshBtn.addEventListener('click', () => this.refreshCurrentFund());
        }

        const clearBtn = document.getElementById('clearCacheBtn');
        if (clearBtn) {
            clearBtn.addEventListener('click', () => this.clearCache());
        }

        const exportBtn = document.getElementById('exportDataBtn');
        if (exportBtn) {
            exportBtn.addEventListener('click', () => this.exportToCSV());
        }

        const exportPngBtn = document.getElementById('exportPngBtn');
        if (exportPngBtn) {
            exportPngBtn.addEventListener('click', () => this.exportChartToPNG());
        }

        const updateGraphBtn = document.getElementById('updateGraphBtn');
        if (updateGraphBtn) {
            updateGraphBtn.addEventListener('click', () => this.updateGraphRange());
        }

        // Analysis buttons
        const analyzeCurrentBtn = document.getElementById('analyzeCurrentBtn');
        if (analyzeCurrentBtn) {
            analyzeCurrentBtn.addEventListener('click', () => this.analyzeCurrentView());
        }

        const analyzeCrisisBtn = document.getElementById('analyzeCrisisBtn');
        if (analyzeCrisisBtn) {
            analyzeCrisisBtn.addEventListener('click', () => this.analyzeCrisis());
        }

        const analyzeRecoveryBtn = document.getElementById('analyzeRecoveryBtn');
        if (analyzeRecoveryBtn) {
            analyzeRecoveryBtn.addEventListener('click', () => this.analyzeRecovery());
        }

        const analyzeRecentBtn = document.getElementById('analyzeRecentBtn');
        if (analyzeRecentBtn) {
            analyzeRecentBtn.addEventListener('click', () => this.analyzeRecent());
        }

        const fundSelect = document.getElementById('fundSelect');
        if (fundSelect) {
            fundSelect.addEventListener('change', (e) => this.onFundChange(e));
        }
    }

    async loadAvailableFunds() {
        try {
            this.setStatus('Loading available funds...', 'loading');
            this.showLoading();
            
            let funds = this.storageService.loadAvailableFunds();
            
            if (!funds || funds.length === 0) {
                console.log('Fetching funds from API...');
                funds = await this.apiService.getAvailableFunds();
                
                if (funds && funds.length > 0) {
                    this.storageService.saveAvailableFunds(funds);
                }
            }
            
            this.state.availableFunds = funds;
            this.populateFundSelect();
            
            this.hideLoading();
            this.setStatus(`Loaded ${funds.length} funds`, 'success');
            
        } catch (error) {
            console.error('Error loading funds:', error);
            this.hideLoading();
            this.setStatus('Failed to load funds. Check console for details.', 'error');
        }
    }

    populateFundSelect() {
        const select = document.getElementById('fundSelect');
        if (!select) return;

        select.innerHTML = '<option value="">-- Select a Fund --</option>';
        
        this.state.availableFunds.forEach((fund, index) => {
            const option = document.createElement('option');
            option.value = index;
            option.textContent = fund.name;
            select.appendChild(option);
        });
    }

    onFundChange(event) {
        const fundIndex = event.target.value;
        
        if (fundIndex === '') {
            this.state.currentFund = null;
            return;
        }

        this.state.currentFund = this.state.availableFunds[fundIndex].name;
        this.loadFundData();
        this.updateFundInfo();
    }

    loadFundData() {
        if (!this.state.currentFund) return;

        console.log(`Loading data for fund: ${this.state.currentFund}`);
        
        const stored = this.storageService.loadFundData(this.state.currentFund);
        const startDateInput = document.getElementById('startDate');
        const endDateInput = document.getElementById('endDate');
        
        const today = new Date().toISOString().split('T')[0];
        
        // Always set end date to today
        if (endDateInput) {
            endDateInput.value = today;
            console.log(`Set end date to: ${today}`);
        }
        
        if (stored && stored.data && Object.keys(stored.data).length > 0) {
            this.state.priceData = stored.data;
            
            // Set start date to earliest cached date
            const dates = Object.keys(this.state.priceData).sort();
            const earliestDate = dates[0];
            const latestDate = dates[dates.length - 1];
            
            if (startDateInput) {
                startDateInput.value = earliestDate;
                console.log(`Set start date to earliest cached: ${earliestDate}`);
            }
            
            this.updateChart();
            this.setStatus(`✓ Loaded ${dates.length} cached points. Range: ${earliestDate} to ${latestDate}`, 'success');
            
            // Visual feedback: briefly highlight the date inputs
            this.highlightDateInputs();
        } else {
            this.state.priceData = {};
            
            // No cached data, set start date to 2 years ago
            const twoYearsAgo = new Date();
            twoYearsAgo.setFullYear(twoYearsAgo.getFullYear() - 2);
            const startDate = twoYearsAgo.toISOString().split('T')[0];
            
            if (startDateInput) {
                startDateInput.value = startDate;
                console.log(`No cache. Set start date to 2 years ago: ${startDate}`);
            }
            
            this.setStatus('No cached data. Dates set to default (2 years). Click "Fetch New Data" to load.', 'info');
            
            // Visual feedback
            this.highlightDateInputs();
        }
    }

    highlightDateInputs() {
        // Briefly highlight date inputs to show they changed
        const startDateInput = document.getElementById('startDate');
        const endDateInput = document.getElementById('endDate');
        
        [startDateInput, endDateInput].forEach(input => {
            if (input) {
                input.style.transition = 'background-color 0.3s';
                input.style.backgroundColor = '#fef3c7';
                setTimeout(() => {
                    input.style.backgroundColor = '';
                }, 800);
            }
        });
    }

    showConfirmDialog(title, message, icon = '❓') {
        return new Promise((resolve) => {
            const modal = document.getElementById('confirmModal');
            const titleEl = document.getElementById('confirmTitle');
            const messageEl = document.getElementById('confirmMessage');
            const iconEl = document.getElementById('confirmIcon');
            const okBtn = document.getElementById('confirmOkBtn');
            const cancelBtn = document.getElementById('confirmCancelBtn');

            // Set content
            if (titleEl) titleEl.textContent = title;
            if (messageEl) messageEl.innerHTML = message;
            if (iconEl) iconEl.textContent = icon;

            // Show modal
            if (modal) {
                modal.style.display = 'flex';
                modal.classList.add('show');
            }

            // Handle OK button
            const handleOk = () => {
                if (modal) {
                    modal.style.display = 'none';
                    modal.classList.remove('show');
                }
                cleanup();
                resolve(true);
            };

            // Handle Cancel button
            const handleCancel = () => {
                if (modal) {
                    modal.style.display = 'none';
                    modal.classList.remove('show');
                }
                cleanup();
                resolve(false);
            };

            // Handle clicking outside modal
            const handleClickOutside = (e) => {
                if (e.target === modal) {
                    handleCancel();
                }
            };

            // Add event listeners
            okBtn.addEventListener('click', handleOk);
            cancelBtn.addEventListener('click', handleCancel);
            modal.addEventListener('click', handleClickOutside);

            // Cleanup function
            function cleanup() {
                okBtn.removeEventListener('click', handleOk);
                cancelBtn.removeEventListener('click', handleCancel);
                modal.removeEventListener('click', handleClickOutside);
            }
        });
    }

    async fetchFundData() {
        if (!this.state.currentFund) {
            alert('Please select a fund first');
            return;
        }

        // Prevent multiple clicks
        const fetchBtn = document.getElementById('fetchDataBtn');
        const refreshBtn = document.getElementById('refreshDataBtn');
        if (fetchBtn) fetchBtn.disabled = true;
        if (refreshBtn) refreshBtn.disabled = true;

        try {
            const startDateInput = document.getElementById('startDate');
            const endDateInput = document.getElementById('endDate');
            const intervalInput = document.getElementById('dataInterval');
            
            let startDate = startDateInput?.value;
            let endDate = endDateInput?.value;
            let interval = parseInt(intervalInput?.value || CONFIG.DEFAULT_DATA_INTERVAL);
            
            if (!startDate || !endDate) {
                const today = new Date();
                endDate = today.toISOString().split('T')[0];
                const twoYearsAgo = new Date(today);
                twoYearsAgo.setFullYear(today.getFullYear() - 2);
                startDate = twoYearsAgo.toISOString().split('T')[0];
            }

            const dates = this.generateDateRange(startDate, endDate, interval);
            const missingDates = dates.filter(d => !this.state.priceData[d]);
            
            if (missingDates.length === 0) {
                alert('All data already cached');
                return;
            }

            const intervalLabel = interval === 1 ? 'daily' : `every ${interval} days`;
            this.setStatus(`Preparing to fetch ${missingDates.length} data points (${intervalLabel})...`, 'loading');
            this.showLoading(`Starting data fetch...`);
            
            let fetchedCount = 0;
            let errorCount = 0;
            
            for (let i = 0; i < missingDates.length; i++) {
                const date = missingDates[i];
                const progress = Math.round((i / missingDates.length) * 100);
                
                // Update progress - make it very visible
                this.showLoading(`⏳ Fetching data: ${i + 1}/${missingDates.length} (${progress}%)<br>${date} - ${intervalLabel}`);
                this.setStatus(`Fetching: ${i + 1}/${missingDates.length} (${progress}%)`, 'loading');
                
                try {
                    const data = await this.apiService.fetchFundData(date);
                    
                    if (data && data.UTMS_FUND) {
                        const fundData = data.UTMS_FUND.find(f => f.FUND_NAME === this.state.currentFund);
                        if (fundData && fundData.OLD_PRICE) {
                            this.state.priceData[date] = parseFloat(fundData.OLD_PRICE);
                            fetchedCount++;
                        }
                    }
                } catch (error) {
                    console.error(`Error fetching date ${date}:`, error);
                    errorCount++;
                }
            }

            this.storageService.saveFundData(this.state.currentFund, this.state.priceData);
            
            this.hideLoading();
            this.updateChart();
            this.updateStorageInfo();
            
            const total = Object.keys(this.state.priceData).length;
            this.setStatus(`✓ Completed! Fetched ${fetchedCount} new points (${intervalLabel}). Total: ${total}`, 'success');
            
            if (errorCount > 0) {
                alert(`Fetch complete with ${errorCount} errors. Check console for details.`);
            }
            
        } catch (error) {
            console.error('Error fetching fund data:', error);
            this.hideLoading();
            this.setStatus('Error fetching data', 'error');
            alert('Error fetching data. Check console for details.');
        } finally {
            // Re-enable buttons
            if (fetchBtn) fetchBtn.disabled = false;
            if (refreshBtn) refreshBtn.disabled = false;
        }
    }

    generateDateRange(startDate, endDate, interval = 1) {
        const dates = [];
        const current = new Date(startDate);
        const end = new Date(endDate);

        while (current <= end) {
            dates.push(current.toISOString().split('T')[0]);
            current.setDate(current.getDate() + interval);
        }

        return dates;
    }

    updateChart() {
        if (!this.state.priceData || Object.keys(this.state.priceData).length === 0) {
            return;
        }

        const dates = Object.keys(this.state.priceData).sort();
        const prices = dates.map(d => this.state.priceData[d]);

        const ctx = document.getElementById('priceChart');
        if (!ctx) return;

        if (this.state.chart) {
            this.state.chart.destroy();
        }

        this.state.chart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: dates,
                datasets: [{
                    label: `${this.state.currentFund} Price (LKR)`,
                    data: prices,
                    borderColor: 'rgb(75, 192, 192)',
                    tension: 0.1,
                    pointRadius: 2,
                    pointHoverRadius: 5
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: {
                        title: {
                            display: true,
                            text: 'Date'
                        }
                    },
                    y: {
                        title: {
                            display: true,
                            text: 'Price (LKR)'
                        }
                    }
                },
                plugins: {
                    title: {
                        display: true,
                        text: `${this.state.currentFund} - Price Trend`,
                        font: {
                            size: 16
                        }
                    }
                }
            }
        });
    }

    refreshCurrentFund() {
        if (!this.state.currentFund) {
            alert('Please select a fund first');
            return;
        }

        const endDate = new Date();
        endDate.setDate(endDate.getDate() - 1);
        const dates = Object.keys(this.state.priceData).sort();
        const startDate = dates.length > 0 ? dates[dates.length - 1] : 
            new Date(endDate.getTime() - 30 * 24 * 60 * 60 * 1000).toISOString().split('T')[0];

        const startInput = document.getElementById('startDate');
        const endInput = document.getElementById('endDate');
        
        if (startInput) startInput.value = startDate;
        if (endInput) endInput.value = endDate.toISOString().split('T')[0];

        this.fetchFundData();
    }

    async updateGraphRange() {
        if (!this.state.currentFund) {
            alert('Please select a fund first');
            return;
        }

        const startDateInput = document.getElementById('startDate');
        const endDateInput = document.getElementById('endDate');
        
        let startDate = startDateInput?.value;
        let endDate = endDateInput?.value;

        if (!startDate || !endDate) {
            alert('Please enter both start and end dates');
            return;
        }

        // Check if we have any data in the selected range
        let dataInRange = {};
        Object.keys(this.state.priceData).forEach(date => {
            if (date >= startDate && date <= endDate) {
                dataInRange[date] = this.state.priceData[date];
            }
        });

        const cachedPointsInRange = Object.keys(dataInRange).length;

        // If no cached data in range, offer to fetch
        if (cachedPointsInRange === 0) {
            const message = `
                No cached data found for the selected date range.
                <br><br>
                <strong>📅 Date Range: ${startDate} to ${endDate}</strong>
                <br><br>
                Would you like to fetch data for this period now?
            `;
            
            const shouldFetch = await this.showConfirmDialog(
                'Fetch Data Required',
                message,
                '📊'
            );

            if (shouldFetch) {
                // Fetch data first
                this.setStatus('Fetching data before updating graph...', 'info');
                await this.fetchFundData();
                
                // After fetching, check again if we have data
                dataInRange = {};
                Object.keys(this.state.priceData).forEach(date => {
                    if (date >= startDate && date <= endDate) {
                        dataInRange[date] = this.state.priceData[date];
                    }
                });

                if (Object.keys(dataInRange).length === 0) {
                    alert('No data was fetched for this date range. The API might not have data for these dates.');
                    return;
                }
            } else {
                // User chose not to fetch
                return;
            }
        }

        // Check if we have a chart to update
        if (!this.state.chart) {
            alert('Please load fund data first');
            return;
        }

        // Update chart with data in range
        const dates = Object.keys(dataInRange).sort();
        const prices = dates.map(d => dataInRange[d]);

        this.state.chart.data.labels = dates;
        this.state.chart.data.datasets[0].data = prices;
        this.state.chart.update();

        this.setStatus(`✓ Graph updated! Showing ${dates.length} points from ${startDate} to ${endDate}`, 'success');
    }

    async clearCache() {
        const message = `
            Are you sure you want to clear <strong>all cached data</strong>?
            <br><br>
            This will remove all downloaded fund data from your browser.
            <br><br>
            <strong>⚠️ This action cannot be undone.</strong>
        `;
        
        const shouldClear = await this.showConfirmDialog(
            'Clear All Cache',
            message,
            '🗑️'
        );
        
        if (shouldClear) {
            this.storageService.clearAll();
            this.state.priceData = {};
            if (this.state.chart) {
                this.state.chart.destroy();
                this.state.chart = null;
            }
            this.updateStorageInfo();
            this.setStatus('✓ Cache cleared successfully', 'success');
        }
    }

    exportToCSV() {
        if (Object.keys(this.state.priceData).length === 0) {
            alert('No data to export');
            return;
        }

        const dates = Object.keys(this.state.priceData).sort();
        let csv = 'Date,Price\n';
        dates.forEach(date => {
            csv += `${date},${this.state.priceData[date]}\n`;
        });

        const blob = new Blob([csv], { type: 'text/csv' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `${this.state.currentFund.replace(/[^a-z0-9]/gi, '_')}_data.csv`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
        
        this.setStatus('✓ Data exported to CSV', 'success');
    }

    exportChartToPNG() {
        if (!this.state.chart) {
            alert('Please load fund data and display a chart first');
            return;
        }

        try {
            // Get the canvas element
            const canvas = document.getElementById('priceChart');
            
            if (!canvas) {
                alert('Chart canvas not found');
                return;
            }

            // Create a temporary canvas with white background
            const tempCanvas = document.createElement('canvas');
            tempCanvas.width = canvas.width;
            tempCanvas.height = canvas.height;
            const ctx = tempCanvas.getContext('2d');
            
            // Fill with white background
            ctx.fillStyle = '#ffffff';
            ctx.fillRect(0, 0, tempCanvas.width, tempCanvas.height);
            
            // Draw the chart on top
            ctx.drawImage(canvas, 0, 0);
            
            // Convert to PNG
            tempCanvas.toBlob((blob) => {
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                
                // Create filename with fund name and date
                const today = new Date().toISOString().split('T')[0];
                const fundName = this.state.currentFund.replace(/[^a-z0-9]/gi, '_');
                a.download = `${fundName}_chart_${today}.png`;
                
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                window.URL.revokeObjectURL(url);
                
                this.setStatus('✓ Chart exported as PNG', 'success');
            }, 'image/png');
            
        } catch (error) {
            console.error('Error exporting chart:', error);
            alert('Failed to export chart. Please try again.');
        }
    }

    updateFundInfo() {
        const dates = Object.keys(this.state.priceData).sort();
        const stored = this.storageService.loadFundData(this.state.currentFund);

        const earliestEl = document.getElementById('earliestDate');
        const pointsEl = document.getElementById('dataPoints');
        const updatedEl = document.getElementById('lastUpdated');

        if (earliestEl) earliestEl.textContent = dates.length > 0 ? dates[0] : '-';
        if (pointsEl) pointsEl.textContent = dates.length;
        if (updatedEl) updatedEl.textContent = stored?.lastUpdated ? 
            new Date(stored.lastUpdated).toLocaleDateString() : '-';
    }

    updateStorageInfo() {
        const info = this.storageService.getStorageInfo();
        const storageEl = document.getElementById('storageInfo');
        if (storageEl) {
            storageEl.textContent = `Local Storage: ${info.usedMB} MB (${info.cachedFunds} funds cached)`;
        }
    }

    setStatus(message, type = 'info') {
        const statusEl = document.getElementById('statusText');
        if (statusEl) {
            statusEl.textContent = message;
            statusEl.className = `status-${type}`;
        }
    }

    showLoading(message = 'Loading...') {
        let loadingEl = document.getElementById('loadingSpinner');
        let overlayEl = document.getElementById('loadingOverlay');
        
        // Create elements if they don't exist
        if (!loadingEl) {
            loadingEl = document.createElement('div');
            loadingEl.id = 'loadingSpinner';
            loadingEl.className = 'loading-spinner';
            loadingEl.innerHTML = '<p></p>';
            document.body.appendChild(loadingEl);
        }
        
        if (!overlayEl) {
            overlayEl = document.createElement('div');
            overlayEl.id = 'loadingOverlay';
            overlayEl.className = 'loading-overlay';
            document.body.appendChild(overlayEl);
        }
        
        // Update message and show
        const messageEl = loadingEl.querySelector('p');
        if (messageEl) messageEl.innerHTML = message;
        
        loadingEl.style.display = 'block';
        overlayEl.style.display = 'block';
    }

    hideLoading() {
        const loadingEl = document.getElementById('loadingSpinner');
        const overlayEl = document.getElementById('loadingOverlay');
        
        if (loadingEl) loadingEl.style.display = 'none';
        if (overlayEl) overlayEl.style.display = 'none';
    }

    // ==================== ANALYSIS FUNCTIONS ====================

    analyzeCurrentView() {
        if (!this.state.chart || Object.keys(this.state.priceData).length === 0) {
            alert('Please load fund data first');
            return;
        }

        const dates = Object.keys(this.state.priceData).sort();
        const startDate = dates[0];
        const endDate = dates[dates.length - 1];

        this.performAnalysis(startDate, endDate, 'Current View Analysis');
    }

    analyzeCrisis() {
        const crisisPeriod = CONFIG.analysis.periods.crisis;
        this.performAnalysis(
            crisisPeriod.start,
            crisisPeriod.end,
            '🚨 Crisis Period Analysis (2022)'
        );
    }

    analyzeRecovery() {
        const recoveryPeriod = CONFIG.analysis.periods.recovery;
        this.performAnalysis(
            recoveryPeriod.start,
            recoveryPeriod.end,
            '📈 Recovery Period Analysis (2023)'
        );
    }

    analyzeRecent() {
        const endDate = new Date();
        const startDate = new Date();
        startDate.setMonth(startDate.getMonth() - CONFIG.analysis.periods.recentMonths);

        this.performAnalysis(
            startDate.toISOString().split('T')[0],
            endDate.toISOString().split('T')[0],
            '📊 Recent 6 Months Analysis'
        );
    }

    performAnalysis(startDate, endDate, title) {
        // Filter data for the specified range
        const dataInRange = {};
        Object.keys(this.state.priceData).forEach(date => {
            if (date >= startDate && date <= endDate) {
                dataInRange[date] = this.state.priceData[date];
            }
        });

        const dates = Object.keys(dataInRange).sort();
        const prices = dates.map(d => dataInRange[d]);

        if (prices.length < 2) {
            alert(`Not enough data for the period ${startDate} to ${endDate}. Please fetch data for this range first.`);
            return;
        }

        // Calculate statistics
        const stats = this.calculateStatistics(prices, dates);
        const volatility = this.calculateVolatility(prices);
        const trend = this.analyzeTrend(prices);
        const events = this.getEconomicEvents(startDate, endDate);

        // Display results
        this.displayAnalysisModal(title, {
            startDate,
            endDate,
            dataPoints: prices.length,
            ...stats,
            volatility,
            trend,
            events
        });
    }

    calculateStatistics(prices, dates) {
        const min = Math.min(...prices);
        const max = Math.max(...prices);
        const avg = prices.reduce((sum, p) => sum + p, 0) / prices.length;
        const startPrice = prices[0];
        const endPrice = prices[prices.length - 1];
        const totalReturn = ((endPrice - startPrice) / startPrice) * 100;

        return {
            min: min.toFixed(4),
            max: max.toFixed(4),
            avg: avg.toFixed(4),
            startPrice: startPrice.toFixed(4),
            endPrice: endPrice.toFixed(4),
            totalReturn: totalReturn.toFixed(2),
            totalReturnValue: totalReturn
        };
    }

    calculateVolatility(prices) {
        const returns = [];
        for (let i = 1; i < prices.length; i++) {
            returns.push((prices[i] - prices[i - 1]) / prices[i - 1]);
        }
        
        const mean = returns.reduce((sum, r) => sum + r, 0) / returns.length;
        const variance = returns.reduce((sum, r) => sum + Math.pow(r - mean, 2), 0) / returns.length;
        const stdDev = Math.sqrt(variance);
        
        // Annualized volatility
        return (stdDev * Math.sqrt(252) * 100).toFixed(2);
    }

    analyzeTrend(prices) {
        const n = prices.length;
        const x = Array.from({ length: n }, (_, i) => i);
        const y = prices;

        const sumX = x.reduce((a, b) => a + b, 0);
        const sumY = y.reduce((a, b) => a + b, 0);
        const sumXY = x.reduce((sum, xi, i) => sum + xi * y[i], 0);
        const sumX2 = x.reduce((sum, xi) => sum + xi * xi, 0);

        const slope = (n * sumXY - sumX * sumY) / (n * sumX2 - sumX * sumX);
        const avgPrice = sumY / n;
        const trendStrength = Math.abs((slope * n / 2) / avgPrice) * 100;

        let direction = 'Sideways';
        if (slope > 0.001) direction = 'Uptrend';
        else if (slope < -0.001) direction = 'Downtrend';

        let description = '';
        if (direction === 'Uptrend') {
            description = `📈 Showing a positive trend with consistent price increases.`;
        } else if (direction === 'Downtrend') {
            description = `📉 Showing a negative trend with price decreases.`;
        } else {
            description = `↔️ Relatively stable with minimal directional movement.`;
        }

        return {
            direction,
            strength: trendStrength.toFixed(2),
            description
        };
    }

    getEconomicEvents(startDate, endDate) {
        const allEvents = [
            { date: '2022-03-01', event: 'Sri Lanka economic crisis begins', impact: 'High' },
            { date: '2022-04-01', event: 'Sri Lanka defaults on foreign debt', impact: 'High' },
            { date: '2022-07-01', event: 'IMF bailout negotiations begin', impact: 'Medium' },
            { date: '2023-03-01', event: 'IMF approves $3 billion bailout package', impact: 'High' },
            { date: '2023-09-01', event: 'Central Bank policy rate adjustments', impact: 'Medium' },
            { date: '2024-01-01', event: 'Economic recovery measures implemented', impact: 'Medium' },
            { date: '2024-06-01', event: 'Tourism sector recovery', impact: 'Low' }
        ];

        return allEvents.filter(event => event.date >= startDate && event.date <= endDate);
    }

    displayAnalysisModal(title, analysis) {
        const modal = document.getElementById('analysisModal');
        const modalTitle = document.getElementById('modalTitle');
        const modalBody = document.getElementById('modalBody');
        const modalClose = document.getElementById('modalClose');

        if (!modal || !modalTitle || !modalBody) {
            alert('Modal elements not found');
            return;
        }

        modalTitle.textContent = title;

        const html = `
            <div class="analysis-section">
                <h3>📅 Period Information</h3>
                <p><strong>Date Range:</strong> ${analysis.startDate} to ${analysis.endDate}</p>
                <p><strong>Data Points:</strong> ${analysis.dataPoints}</p>
            </div>

            <div class="analysis-section">
                <h3>💰 Price Statistics</h3>
                <p><strong>Starting Price:</strong> ${analysis.startPrice} LKR</p>
                <p><strong>Ending Price:</strong> ${analysis.endPrice} LKR</p>
                <p><strong>Minimum Price:</strong> ${analysis.min} LKR</p>
                <p><strong>Maximum Price:</strong> ${analysis.max} LKR</p>
                <p><strong>Average Price:</strong> ${analysis.avg} LKR</p>
            </div>

            <div class="analysis-section">
                <h3>📈 Performance Metrics</h3>
                <p><strong>Total Return:</strong> 
                    <span class="${analysis.totalReturnValue >= 0 ? 'positive-return' : 'negative-return'}">
                        ${analysis.totalReturn}%
                    </span>
                </p>
                <p><strong>Annualized Volatility:</strong> ${analysis.volatility}%</p>
                ${this.getVolatilityLabel(analysis.volatility)}
            </div>

            <div class="analysis-section">
                <h3>📊 Trend Analysis</h3>
                <p><strong>Direction:</strong> ${analysis.trend.direction}</p>
                <p><strong>Trend Strength:</strong> ${analysis.trend.strength}%</p>
                <p>${analysis.trend.description}</p>
            </div>

            ${analysis.events.length > 0 ? `
                <div class="analysis-section">
                    <h3>🎯 Key Economic Events</h3>
                    <ul class="events-list">
                        ${analysis.events.map(event => `
                            <li class="event-item event-${event.impact.toLowerCase()}">
                                <strong>${event.date}:</strong> ${event.event}
                                <span class="impact-badge impact-${event.impact.toLowerCase()}">${event.impact} Impact</span>
                            </li>
                        `).join('')}
                    </ul>
                </div>
            ` : ''}

            <div class="analysis-section insights-section">
                <h3>💡 Key Insights</h3>
                <ul class="insights-list">
                    ${this.generateInsights(analysis).map(insight => `<li>${insight}</li>`).join('')}
                </ul>
            </div>

            <div class="analysis-footer">
                <p><em>This analysis provides historical context and statistical insights. Past performance does not guarantee future results.</em></p>
            </div>
        `;

        modalBody.innerHTML = html;
        modal.style.display = 'flex';

        // Close button handler
        const closeModal = () => {
            modal.style.display = 'none';
        };

        modalClose.onclick = closeModal;
        modal.onclick = (e) => {
            if (e.target === modal) closeModal();
        };
    }

    getVolatilityLabel(volatility) {
        const vol = parseFloat(volatility);
        if (vol > 30) {
            return '<p><em>⚡ High volatility - significant price swings observed.</em></p>';
        } else if (vol > 15) {
            return '<p><em>📊 Moderate volatility - some price fluctuations.</em></p>';
        } else {
            return '<p><em>📈 Low volatility - relatively stable period.</em></p>';
        }
    }

    generateInsights(analysis) {
        const insights = [];
        const returnVal = parseFloat(analysis.totalReturn);
        const volatility = parseFloat(analysis.volatility);

        // Return insights
        if (returnVal > 10) {
            insights.push('📈 <strong>Strong Performance:</strong> The fund showed excellent returns during this period.');
        } else if (returnVal > 0) {
            insights.push('📊 <strong>Positive Growth:</strong> The fund delivered modest positive returns.');
        } else if (returnVal < -10) {
            insights.push('📉 <strong>Significant Decline:</strong> The fund experienced substantial losses during this period.');
        } else if (returnVal < 0) {
            insights.push('↘️ <strong>Minor Decline:</strong> The fund showed slight negative returns.');
        } else {
            insights.push('↔️ <strong>Stable:</strong> The fund remained relatively flat with minimal change.');
        }

        // Volatility insights
        if (volatility > 30) {
            insights.push('⚡ <strong>High Risk Period:</strong> Significant price fluctuations indicate higher investment risk.');
        } else if (volatility < 10) {
            insights.push('🛡️ <strong>Stable Period:</strong> Low volatility suggests a safer, more predictable investment period.');
        }

        // Trend insights
        if (analysis.trend.direction === 'Uptrend') {
            insights.push('🚀 <strong>Positive Momentum:</strong> The upward trend suggests growing investor confidence.');
        } else if (analysis.trend.direction === 'Downtrend') {
            insights.push('🔻 <strong>Negative Momentum:</strong> The downward trend indicates decreasing fund value over time.');
        }

        // Event insights
        if (analysis.events.length > 0) {
            const highImpact = analysis.events.filter(e => e.impact === 'High').length;
            if (highImpact > 0) {
                insights.push(`🎯 <strong>Major Events:</strong> ${highImpact} high-impact economic events occurred during this period.`);
            }
        }

        return insights;
    }
}

// Initialize application when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    console.log('DOM loaded, initializing app...');
    window.app = new CALFundAnalyzer();
});
