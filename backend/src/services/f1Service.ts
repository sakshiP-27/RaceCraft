import axios from "axios";

import serverConfig from "../config/serverConfig";

class F1Service {
    constructor() {
        // Nothing to add right now
    }

    async getCircuits() {
        try {
            const response = await axios.get(`${serverConfig.ML_MODEL_API_URL}/circuits`);
            if (!response.data || !Array.isArray(response.data)) {
                throw new Error ("Invalid response format for circuits");
            }

            return response.data;
        } catch (error) {
            console.error("Error fetching the circuits", error);
            throw new Error("Failed to fetch circuits");
        }
    }

    async getDrivers() {
        try {
            const response = await axios.get(`${serverConfig.ML_MODEL_API_URL}/drivers`);
            if (!response.data || !Array.isArray(response.data)) {
                throw new Error("Invalid response format for drivers");
            }

            return response.data;
        } catch (error) {
            console.error("Error fetching the drivers", error);
            throw new Error("Failed to fetch drivers");
        }
    }
}

export default F1Service;