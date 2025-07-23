import express from "express";

import f1Controller from "../../controllers/f1Controller";

const f1Router = express.Router();

f1Router.get("/circuits", f1Controller.getCircuits);
f1Router.get("/drivers", f1Controller.getDrivers);

export default f1Router;