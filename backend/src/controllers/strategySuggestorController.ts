import { Request, Response, NextFunction } from "express";
import { StatusCodes } from "http-status-codes";

async function strategySuggestion(req: Request, res: Response, next: NextFunction) {
    return res.status(StatusCodes.OK).json({
        message: "Strategy suggestion endpoint build complete"
    });
};

export default {
    strategySuggestion
};