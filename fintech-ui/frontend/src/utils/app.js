import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

export const fetchPortfolio = async () => {
    const response = await axios.get(`${API_BASE_URL}/dashboard/portfolio`);
    return response.data.portfolio;
};

export const fetchMarketSentiment = async () => {
    const response = await axios.get(`${API_BASE_URL}/dashboard/market-sentiment`);
    return response.data.sentiment;
};

export const executeTrade = async (symbol, quantity) => {
    const response = await axios.post(`${API_BASE_URL}/trade/execute`, { symbol, quantity });
    return response.data;
};

export const fetchComplianceLogs = async () => {
    const response = await axios.get(`${API_BASE_URL}/compliance/logs`);
    return response.data.logs;
};