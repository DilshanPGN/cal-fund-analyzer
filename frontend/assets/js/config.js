// Configuration
const CONFIG = {
    API_BASE_URL: window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
        ? 'http://localhost:5000/api/funds'
        : '/api/funds',
    API_DELAY_MS: 500,
    CACHE_PREFIX: 'cal_fund_data_',
    DEFAULT_FUND: 'Capital Alliance Quantitative Equity Fund',
    DEFAULT_START_DATE: '2013-01-01',
    DEFAULT_DATA_INTERVAL: 15, // Default: fetch data every 15 days
    DATA_INTERVAL_OPTIONS: [
        { value: 1, label: 'Every Day (Most Data)' },
        { value: 7, label: 'Every Week' },
        { value: 15, label: 'Every 15 Days (Default)' },
        { value: 30, label: 'Every Month' },
        { value: 90, label: 'Every Quarter' }
    ],
    analysis: {
        periods: {
            crisis: { start: '2022-01-01', end: '2022-12-31' },
            recovery: { start: '2023-01-01', end: '2023-12-31' },
            recentMonths: 6
        }
    }
};
