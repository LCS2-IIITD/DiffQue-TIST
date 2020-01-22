var express = require('express');
var router = express.Router();
var localStorage = require('localStorage')
var PythonShell = require('python-shell');

router.post('/', function(req, res) {
    var id1 = req.body.id1;
    var id2 = req.body.id2;

    console.log("Computing for "  + id1 + " " + id2);
    callModel(id1, id2, function(answer){
    	console.log("Answer received " + answer);
	    res.status(200);
	    res.end(""+answer);
    });
    
});

function callModel(id1, id2, next){
	var options = {
	  args: [id1, id2]
	};
	var pyshell = new PythonShell('model/interface.py', options);
	pyshell.on('message', function (message) {
	  console.log(message);
	  next(message);
	});
}

module.exports = router;