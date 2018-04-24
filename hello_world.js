/*
	A simple hello world server used for testing purposes. 
	Listens on a prespecified port and ends any incoming get request with Hello World
*/

express = require('express')
var message = 'Hello World!\n';
var port = 8080;

var server_app = express();
server_app.get('/', function(req, res){
	var obj = {
		"headers": req.headers,
		"body": req.body
	}
	var msg = "Received at " + String(Date.now()) + "\n" + JSON.stringify(obj, null, 4);
	console.log(msg);
	res.end(message);
});

server_app.get('/monitor', function(req, res){
	res.statusCode = 200
	res.end('Okay!')
})

server_app.listen(port);
console.log("Hello World app listening on port " + String(port));
