const urlProd = 'SET URL WHEN DEPLOYED TO PRODUCTION';
//const urlDev = 'http://localhost:5000/';
const urlDev = 'https://wet-owl-89.localtunnel.me/';
const production = false;

export const api = {
    getPrediction: () => `${production ? urlProd : urlDev}cnnclassifier/predict`
};