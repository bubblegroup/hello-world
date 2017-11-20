express = require 'express'

class HelloWorld
    constructor: () ->
        @message = 'Hello World!'

        @server_app = express()
        @server_app.get '/', (req, res) =>
            res.end(@message)

        @server_app.listen(8080)
        console.log "Hello World app listening on port 8080"

server = new HelloWorld()

