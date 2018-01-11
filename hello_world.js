express = require('express')

var message = 'Hello World!';
var port = 80;

var server_app = express();
server_app.get('/', function(req, res){
    res.end(message);
});

server_app.listen(port);
console.log("Hello World app listening on port " + String(port));
