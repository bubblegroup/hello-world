/*
	A simple hello world server used for testing purposes. 
	Listens on a prespecified port and ends any incoming get request with Hello World
*/

request = require('request')
express = require('express')
var message = "Hello World!\n";
var port = 8080;

var server_app = express();
exports.server = server_app;

var id = ''
server_app.use(function(req, res, next) {
	res.setHeader("x-hello-world-id", id)
	next()
})

server_app.get('/', function(req, res){
	res.end(message);
});

server_app.get('/monitor', function(req, res){
	res.statusCode = 200
	res.end('Okay!')
})

if (require.main === module){
	request.get("http://169.254.169.254/latest/meta-data/instance-id", function(err, response, body){
		if (err) {
			throw err
		} else {
			id = body.toString()
			server_app.listen(port)
			console.log("Hello World app listening on port " + String(port))
		}
	})
}

