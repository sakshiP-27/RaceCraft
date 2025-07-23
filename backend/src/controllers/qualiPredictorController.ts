import { Request, Response, NextFunction } from "express";
import { StatusCodes } from "http-status-codes";

import QualiPredictorService from "../services/qualiPredictorService";

const qualiPredictorService = new QualiPredictorService();

async function qualifierPrediction(req: Request, res: Response, next: NextFunction) {
    try {
        const circuitName = req.body.circuit;
        const driverName = req.body.driver;
        const { temperature, humidity, rain_chance } = req.body.weather;

        const predictionData = await qualiPredictorService.getQualiPredictions(circuitName, driverName, temperature, humidity, rain_chance);

        if (!predictionData) {
            return res.status(StatusCodes.INTERNAL_SERVER_ERROR).json({
                message: "Error fetching predictions from ML model API"
            });
        }

        return res.status(StatusCodes.OK).json({
            message: "Qualifying predictions fetched successfully",
            data: predictionData
        });
    } catch (error: any) {
        console.error("Error in qualifierPrediction controller:", error);
        next(error);
    }
};

export default {
    qualifierPrediction
};