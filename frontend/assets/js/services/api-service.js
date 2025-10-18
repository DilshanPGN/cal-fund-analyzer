// Simple API Service without ES6 modules
class APIService {
    constructor() {
        this.baseUrl = CONFIG.API_BASE_URL;
        this.retryAttempts = 3;
        this.retryDelayMs = 1000;
    }

    async fetchFundData(date) {
        const url = `${this.baseUrl}?date=${date}`;
        let attempts = 0;

        while (attempts < this.retryAttempts) {
            try {
                const response = await fetch(url);
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                const data = await response.json();
                if (data.error) {
                    throw new Error(data.error);
                }
                await this.sleep(CONFIG.API_DELAY_MS);
                return data;
            } catch (error) {
                attempts++;
                console.warn(`API fetch attempt ${attempts} failed for date ${date}: ${error.message}`);
                if (attempts < this.retryAttempts) {
                    await this.sleep(this.retryDelayMs * attempts);
                } else {
                    throw new Error(`Failed to fetch data for ${date} after ${this.retryAttempts} attempts: ${error.message}`);
                }
            }
        }
    }

    async getAvailableFunds() {
        try {
            const sampleDate = '2024-10-01'; // Use a recent date
            const data = await this.fetchFundData(sampleDate);
            
            if (!data || !data.UTMS_FUND) {
                throw new Error('Invalid API response for fund discovery');
            }
            
            return data.UTMS_FUND.map(fund => ({
                name: fund.FUND_NAME,
                earliestDate: null
            }));
        } catch (error) {
            console.error('Error discovering funds:', error);
            throw error;
        }
    }

    sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
}

// Create global instance
const apiService = new APIService();
