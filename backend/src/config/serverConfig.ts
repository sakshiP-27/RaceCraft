import dotenv from "dotenv";
dotenv.config();

export default {
    PORT: process.env.PORT || 3000,
    ML_MODEL_API_URL: process.env.ML_MODEL_API_URL
};