const axios = require('axios');

const hotelApiConfig = {
    headers: {
        "x-rapidapi-host": "hotels4.p.rapidapi.com",
        "x-rapidapi-key": "409d60d423msh8a522df17b8208dp193db0jsn60b1dcc49c9e"
    }
};

axios.defaults.headers.get["x-rapidapi-host"] = "hotels4.p.rapidapi.com";
axios.defaults.headers.get["x-rapidapi-key"] = "409d60d423msh8a522df17b8208dp193db0jsn60b1dcc49c9e";

const hotelDescr = `Situated 700 m from Louvre Museum in Paris, the hotel offers free access to its indoor pool and hot tub. 
The hotel also features a spa centre, Le Spa Pont-Neuf by Cinq Mondes, accessible at an extra cost. 
Guests can enjoy a meal at the restaurant. Every room at this hotel is air conditioned and has a coffee machine and a 
flat-screen TV with cable channels. All rooms comes with a touchpad, which is at guest's disposal. Each room is fitted 
with a private bathroom, free toiletries and a hairdryer. Guests will find japanese toilet in the bathroom.
A continental buffet breakfast including pastries, cheese and salmon is available daily. Fruit juice, cold meats and jam 
are also provided and eggs are prepared on request and at an extra cost. Guests can also enjoy lunch and dinner made with 
seasonal produce at the hotel's restaurant. There is a 24-hour front desk at the property.
Pompidou Centre is 10 minutes away by walk from the hotel, while Notre Dame Cathedral is 15 minutes away. 
The nearest airport is Paris - Orly Airport, 23 km from the property.
The hotel is located in the 1st arr. which is a great choice for travellers interested in shopping, art and museums.
This is our guests' favourite part of Paris, according to independent reviews. This area is also great for shopping, 
with popular brands nearby: H&M, Zara, Chanel.
Couples particularly like the location — they rated it 9.4 for a two-person trip.
We speak your language!
Among the most popular facilities, there are: swimming pool, non-smocking rooms, spa, fitness centre, room service, indoor pool,
bar, free wi-fi. Has great rating for comfy beds, and very good coffee.`;

const googleSearch = (query) => {
    return axios.get("https://www.googleapis.com/customsearch/v1", {
        params: {
            cx: "000241170284453365987:9dru2oeetju",
            q: query,
            key: "AIzaSyCizOsDnVSqSK21pxe2owf5gh7o1ofmZsU"
        }
    }).then(({ data }) => data.items[1].link);
};

export const qa = (doc, question) => {
    return axios.post("http://192.168.43.50:8000/predict", {
        document: doc,
        question: question
    }).then(({ data }) => data.result.answer);
};

const locationSearch = (location) => {
    return axios.get("https://hotels4.p.rapidapi.com/locations/search", {
        params: {
            locale: "en_US",
            query: location
        }
    }, hotelApiConfig).then(({ data }) => data.suggestions[0].entities[0]);
};


const propertySearch = (destId, destType, date, price) => {
    return axios.get("https://hotels4.p.rapidapi.com/properties/list", {
        params: {
            currency: "USD",
            checkIn: "2020-01-08",
            locale: "en_US",
            sortOrder: "PRICE",
            destinationId: destId,
            type: destType,
            pageNumber: 1,
            pageSize: 25,
            adults1: 1,
            priceMax: 350
        }
    }, hotelApiConfig).then(({ data }) => data.data.body.searchResults.results[0]);
};

const getHotelDesctiption = (hotelId) => {
    return Promise.resolve(hotelDescr);
};

const hotelFind = ([location, date, price]) => {
    return locationSearch(location)
        .then(gpe => {
            return propertySearch(gpe.destinationId, gpe.type, date, price)
                .then(hotel => {
                    return getHotelDesctiption(hotel.id)
                        .then(descr => {
                            return {
                                name: hotel.name,
                                description: descr, 
                                url: hotel.thumbnailUrl
                            };
                        });
                });
        });
};

export default hotelFind;