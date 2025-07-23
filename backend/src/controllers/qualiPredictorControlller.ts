import { Request, Response, NextFunction } from "express";
import { StatusCodes } from "http-status-codes";

async function qualifierPrediction(req: Request, res: Response, next: NextFunction) {
    return res.status(StatusCodes.OK).json({
        message: "Qualifier prediction endpoint build complete"
    });
};

export default {
    qualifierPrediction
};