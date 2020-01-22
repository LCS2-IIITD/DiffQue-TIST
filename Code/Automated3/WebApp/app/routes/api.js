var express = require('express');
var apiRouter  = express.Router();

var questionsRouter = require('./questions');

apiRouter.use('/questions',questionsRouter);

module.exports = apiRouter;