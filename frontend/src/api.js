import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:8002';

const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

export const predictWaitTime = async (data) => {
    try {
        const response = await api.post('/predict', data);
        return response.data;
    } catch (error) {
        console.error('Error predicting wait time:', error);
        throw error;
    }
};

export const getMetrics = async () => {
    try {
        const response = await api.get('/mlops/metrics');
        return response.data;
    } catch (error) {
        console.error('Error getting metrics:', error);
        throw error;
    }
};

export const retrainModel = async () => {
    try {
        const response = await api.post('/mlops/retrain');
        return response.data;
    } catch (error) {
        console.error('Error retraining model:', error);
        throw error;
    }
};

export default api;
