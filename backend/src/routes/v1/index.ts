import express from "express";

import qualiPredictorRouter from "./qualiPredictorRouter";
import strategySuggestorRouter from "./strategySuggestorRouter";
import f1Router from "./f1Router";

const v1Router = express.Router();

v1Router.use("/f1", f1Router);
v1Router.use("/quali-predictor", qualiPredictorRouter);
v1Router.use("/strategy-suggestor", strategySuggestorRouter);

export default v1Router;