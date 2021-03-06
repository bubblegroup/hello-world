const assert = require('assert')
const request = require('request')

// TODO : this should probably run the hello world module as a subprocess for realism
const server = require('../hello_world').server

server.listen(8080)

describe('/', function(){

	var url = "http://localhost:8080/";

	it('returns statusCode 200', function(done){
		request.get(url, function(err, response, body){
			if (err){
				throw err
			} else {
				assert.equal(response.statusCode, 200)
			}
			done()
		})
	})

	it('returns body Hello World!', function(done){
		request.get(url, function(err, response, body){
			if (err){
				throw err
			} else {
				assert.equal(body, 'Hello World!\n')
			}
			done()
		})
	})
})

describe('/monitor', function(){

	var url = 'http://localhost:8080/monitor';

	it('returns statusCode 200', function(done){
		request.get(url, function(err, response, body){
			if (err){
				throw err
			} else {
				assert.equal(response.statusCode, 200)
			}
			done()
		})
	})

	it('returns body Okay!', function(done){
		request.get(url, function(err, response, body){
			if (err){
				throw err
			} else {
				assert.equal(body, "Okay!")
			}
			done()
		})
	})
})