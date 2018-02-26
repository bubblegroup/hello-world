var request = require('request');

var URLS = [

	// tech giants
	'google.com', 
	'facebook.com', 
	'netflix.com', 
	'youtube.com',
	'quora.com',
	'airbnb.com',

	// news sites
	'nytimes.com', 
	'newyorker.com',
	'theatlantic.com',

	// non-tech enterprises
	'homedepot.com',
	''

	// non-profits 
	'wikipedia.com',

	// competitors
	'squarespace.com', 
	'wix.com', 

	// us
	'bubble.is', 

	// 'hot' tech startups
	'x.ai', 
	'betterment.com', 
	'clarifai.com', 
];

function cb(before){
	return function (err, response, body){


		// print error or compute latency and log
		if (err) {
			console.log("Error hitting " + response.req._headers.host + " " + String(err))
		} else if (response) {

			var latency = Date.now() - before;
			
			var msg = "Latency for " + response.req._headers.host + " " + String(latency) + " ";
			if (typeof(response.headers['server']) != 'undefined' &&  response.headers['server'] != null){
				msg += response.headers['server'] + " "
			}

			if (typeof(response.headers['x-powered-by']) != 'undefined' &&  response.headers['x-powered-by'] != null){
				msg += response.headers['x-powered-by']
			}
			
			console.log(msg)

		}

	}
}

function testLatency() {
	for(i=0; i < URLS.length; i++){
		
		url = URLS[i];
		if (url.indexOf("http://") === -1){
			url = "http://" + url
		}

		before = Date.now()
		request.get(url, cb(before))
	}
};

setInterval(testLatency, 5 * 1000)

