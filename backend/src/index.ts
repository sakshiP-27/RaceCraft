import express, { Express, Request, Response } from "express";
import bodyParser from "body-parser";

import serverConfig from "./config/serverConfig";
import apiRouter from "./routes";

const app: Express = express();

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true}));
app.use(bodyParser.text());

app.use("/api", apiRouter);

app.listen(serverConfig.PORT, () => {
    console.log(`Server is running on the PORT ${serverConfig.PORT}`)
});