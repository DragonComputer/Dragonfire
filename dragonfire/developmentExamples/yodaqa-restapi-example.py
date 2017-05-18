import json
import urllib.request, urllib.parse, urllib.error
import urllib.request, urllib.error, urllib.parse
import time

url = 'http://qa.ailao.eu/q'
#url = 'http://localhost:4567/q'
post_params = {
	'text' : 'When was Albet Einstein born'
}

params = urllib.parse.urlencode(post_params)
response = urllib.request.urlopen(url, params)
json_response = json.loads(response.read())

print(json_response['id'])

time.sleep(20)

url2 = url + '/' + json_response['id']

print(url2)
response2 = urllib.request.urlopen(url2)
data = json.load(response2)
#print data
print(data['answers'])
print(data['answers'][0])
