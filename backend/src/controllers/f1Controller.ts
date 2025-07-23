import { Request, Response, NextFunction } from "express";
import { StatusCodes } from "http-status-codes";

import F1Service from "../services/f1Service";

const f1Service = new F1Service();

async function getCircuits(req: Request, res: Response, next: NextFunction) {
    try {
        const circuits = await f1Service.getCircuits();
        return res.status(StatusCodes.OK).json(circuits);
    } catch (error) {
        next(error);
        console.error("Error in getCircuits service", error);
        return res.status(StatusCodes.INTERNAL_SERVER_ERROR).json({
            message: "Failed to fetch circuits due to some internal issue"
        });
    }
};

async function getDrivers(req: Request, res: Response, next: NextFunction) {
    try {
        const drivers = await f1Service.getDrivers();
        return res.status(StatusCodes.OK).json(drivers);
    } catch (error) {
        next(error);
        console.error("Error in getDrivers service", error);
        return res.status(StatusCodes.INTERNAL_SERVER_ERROR).json({
            message: "Failed to fetch drivers due to some internal issue"
        });
    }
}

export default {
    getCircuits,
    getDrivers
};