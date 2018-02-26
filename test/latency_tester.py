import requests
import pprint 

pp = pprint.PrettyPrinter(indent=4)

from datetime import datetime 

URLS = ['google.com', 'facebook.com', 'netflix.com', 'nytimes.com', 'homedepot.com', 'squarespace.com', 'wix.com', 'bubble.is', 'x.ai']

for url in URLS:

	# prepend http:// if necessary
	if not ('http://' in url):
		_url = 'http://' + url 
	else:
		_url = url 

	# measure latency
	before = datetime.now()
	response = requests.get(_url)
	after = datetime.now()

	pp.pprint(response.headers)
	print "Latency for {}: {}".format(_url, (after - before).total_seconds() * 1000.0)