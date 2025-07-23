import express from "express";

import strategySuggestorController from "../../controllers/strategySuggestorController";

const strategySuggestorRouter = express.Router();

strategySuggestorRouter.post("/strategy-suggestion", strategySuggestorController.strategySuggestion);

export default strategySuggestorRouter;