const urlProd = 'SET URL WHEN DEPLOYED TO PRODUCTION';
const urlDev = 'http://localhost:5000/';
const production = false;

export const api = {
    getPrediction: () => `${production ? urlProd : urlDev}cnnclassifier/predict`
};