import {api} from './api';

class ItemService {
    async getPrediction(json) {
        console.debug("ItemService.getPrediction():");
        console.debug(json);
        return fetch(api.getPrediction(), {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(json)
        })
            .then(response => {
                // if (!response.ok) {
                //     console.log("GRESIT");
                //     this.handleResponseError(response);
                // }
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