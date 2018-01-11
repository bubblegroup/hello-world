express = require('express')

var message = 'Hello World!';

var server_app = express();
server_app.get('/', function(req, res){
    res.end(message);
});

port = 80
server_app.listen(port);
console.log("Hello World app listening on port #{port}");
