import express from "express";

import qualiPredictorController from "../../controllers/qualiPredictorController";

const qualiPredictorRouter = express.Router();

qualiPredictorRouter.post("/qualifier-prediction", qualiPredictorController.qualifierPrediction);

export default qualiPredictorRouter;
