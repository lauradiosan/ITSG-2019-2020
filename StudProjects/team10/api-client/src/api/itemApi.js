import {api} from './api';

class ItemService {
    async getPrediction(json) {
        console.debug("ItemService.getPrediction():");
        console.debug(json);
        return fetch(api.getPrediction(), {
            method: "POST",
            mode: "no-cors",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(json)
        })
            .then(response => {
                console.log(response);
                if (!response.ok) {
                    this.handleResponseError(response);
                }
                return response.json();
            })
            .catch(error => {
                this.handleError(error);
            });
    }

    handleResponseError(response) {
        throw new Error("HTTP error, status = " + response.status);
    }
    handleError(error) {
        console.debug(error.message);
    }
}
export default ItemService;