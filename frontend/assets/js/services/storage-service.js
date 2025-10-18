// Simple Storage Service without ES6 modules
class StorageService {
    constructor() {
        this.cachePrefix = CONFIG.CACHE_PREFIX;
    }

    getFundData(fundName) {
        const key = `${this.cachePrefix}${fundName}`;
        const data = localStorage.getItem(key);
        return data ? JSON.parse(data) : null;
    }

    setFundData(fundName, data) {
        const key = `${this.cachePrefix}${fundName}`;
        try {
            const dataToStore = {
                data: data,
                lastUpdated: new Date().toISOString()
            };
            localStorage.setItem(key, JSON.stringify(dataToStore));
            return true;
        } catch (e) {
            console.error('Error saving to localStorage:', e);
            if (e.name === 'QuotaExceededError') {
                alert('Local storage quota exceeded. Please clear some cached data or browser storage.');
            }
            return false;
        }
    }

    loadFundData(fundName) {
        return this.getFundData(fundName);
    }

    saveFundData(fundName, data) {
        return this.setFundData(fundName, data);
    }

    getAllCachedFunds() {
        const funds = [];
        for (let i = 0; i < localStorage.length; i++) {
            const key = localStorage.key(i);
            if (key.startsWith(this.cachePrefix)) {
                const fundName = key.substring(this.cachePrefix.length);
                funds.push(fundName);
            }
        }
        return funds;
    }

    clearFundData(fundName) {
        const key = `${this.cachePrefix}${fundName}`;
        localStorage.removeItem(key);
    }

    clearAll() {
        this.getAllCachedFunds().forEach(fundName => this.clearFundData(fundName));
    }

    getStorageInfo() {
        let total = 0;
        for (let i = 0; i < localStorage.length; i++) {
            const key = localStorage.key(i);
            if (key.startsWith(this.cachePrefix)) {
                total += (localStorage.getItem(key).length * 2);
            }
        }
        return {
            usedBytes: total,
            usedMB: (total / (1024 * 1024)).toFixed(2),
            cachedFunds: this.getAllCachedFunds().length
        };
    }

    loadAvailableFunds() {
        const key = 'cal_available_funds';
        const data = localStorage.getItem(key);
        return data ? JSON.parse(data) : null;
    }

    saveAvailableFunds(funds) {
        const key = 'cal_available_funds';
        try {
            localStorage.setItem(key, JSON.stringify(funds));
            return true;
        } catch (e) {
            console.error('Error saving available funds:', e);
            return false;
        }
    }
}

// Create global instance
const storageService = new StorageService();
