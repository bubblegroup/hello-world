/*
	A simple hello world server used for testing purposes. 
	Listens on a prespecified port and ends any incoming get request with Hello World
*/

math = require('mathjs')
express = require('express')
var message = "Hello World!\n";
var port = 8080;

var server_app = express();
exports.server = server_app;

server_app.get('/', function(req, res){
	res.end(message);
});

server_app.get('/matrix/multiply', function(req, res){
	const c = math.matrix([[2, 0, 7], [-1, 3, 1], [5, 5, 2]])   
	const d = math.matrix([[7, 1, 2], [-2, 3, 1], [5, 6, 2]])  
	const e = math.multiply(c, d)
	res.end(String(e))
})

server_app.get('/monitor', function(req, res){
	res.statusCode = 200
	res.end('Okay!')
})

if (require.main === module){
	server_app.listen(port);
	console.log("Hello World app listening on port " + String(port));	
}

