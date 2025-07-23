import axios from "axios";

import serverConfig from "../config/serverConfig";

class QualiPredictorService {
    constructor() {
        // Nothing to add here right now
    }

    async getQualiPredictions(circuitName: string, driverName: string, temperature: number, humidity: number, rain_chance: number): Promise<any> {
        // constructing the payload for the prediction request
        const payload: object = {
            circuit: circuitName,
            driver: driverName,
            weather: {
                temperature: temperature,
                humidity: humidity,
                rain_chance: rain_chance
            }
        }

        // making the API call to the ML model service for the qualifying predictions
        try {
            const response = await axios.post(`${serverConfig.ML_MODEL_API_URL}/quali-prediction`, payload)
            if (response.status === 200) {
                return response.data;
            }
            throw new Error(`Unexpected response status: ${response.status}`);
        } catch (error: any) {
            console.error("Error fetching predictions from ML model API:", error.message);
            throw new Error("Failed to fetch predictions from ML model API");
        }
    }
}

export default QualiPredictorService;