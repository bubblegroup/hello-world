/*
	Echo repeats back the headers and body of whatever response it receives. 
*/

express = require('express')
var port = 8080;

var echo = express();
echo.post('/', function(req, res){
	var obj = {
		"method": req.method,
		"headers": req.headers,
		"body": req.body
	}
	var msg = "Received at " + String(Date.now()) + "\n" + JSON.stringify(obj, null, 4) + "\n"; 
	console.log(msg);
	res.end(msg);
});

echo.listen(port);
console.log("Echo app listening on port " + String(port));
