import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

// Function to get the JWT token from local storage
const getToken = () => {
    if (typeof window !== "undefined") { // Check if running in the browser
        return localStorage.getItem('token');
    }
    return null;
};


// Axios instance with default headers
const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${getToken()}`, // Include the JWT token
    },
});

export const fetchPortfolio = async () => {
    try {
        const response = await api.get('/dashboard/portfolio');
        return response.data.portfolio;
    } catch (error) {
        console.error("Error fetching portfolio:", error);
        return []; // Return an empty array as fallback
    }
};

export const fetchMarketSentiment = async () => {
    try {
        const response = await api.get('/dashboard/market-sentiment');
        return response.data.sentiment;
    } catch (error) {
        console.error("Error fetching market sentiment:", error);
        return {
            chartData: {
                labels: ["2023-10-01", "2023-10-02", "2023-10-03", "2023-10-04", "2023-10-05", "2023-10-06", "2023-10-07"],
                prices: [100, 105, 110, 115, 120, 125, 130],
            },
        };
    }
};

export const executeTrade = async (assetType, symbol, quantity) => {
    try {
        const response = await api.post('/trade/execute', { asset_type: assetType, symbol, quantity });
        return response.data;
    } catch (error) {
        console.error("Error executing trade:", error);
        return { status: "Trade execution failed" };
    }
};


export const fetchComplianceLogs = async () => {
    try {
        const response = await api.get('/compliance/logs');
        return response.data.logs;
    } catch (error) {
        console.error("Error fetching compliance logs:", error);
        return [];
    }
};