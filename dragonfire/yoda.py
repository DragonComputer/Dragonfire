import json
import urllib.request, urllib.parse, urllib.error
import urllib.request, urllib.error, urllib.parse
import time
import sys
import contextlib
import io
from random import randint

class YodaQA():

	@staticmethod
	def answer(address, query, user_prefix):
		url = address + '/q'
		#url = 'http://localhost:4567/q'
		post_params = {
			'text' : query
		}

		params = urllib.parse.urlencode(post_params)
		response = urllib.request.urlopen(url, params)
		json_response = json.loads(response.read())

		#print json_response['id']

		# setup toolbar
		toolbar_width = 180 / 3
		sys.stdout.write("|%s|" % (" " * toolbar_width))
		sys.stdout.flush()
		sys.stdout.write("\b" * (toolbar_width+1)) # return to start of line, after '['

		seconds = 0
		while seconds < 180:
			time.sleep(3)
			seconds = seconds + 3

			url2 = url + '/' + json_response['id']

			#print url2
			response2 = urllib.request.urlopen(url2)
			data = json.load(response2)
			#print data
			#print data['answers']
			sys.stdout.write(chr(0x2588))
			sys.stdout.flush()
			if data['answers']:
				if float(data['answers'][0]['confidence']) > 0.5:
					sys.stdout.write("\n\n")
					return data['answers'][0]['text']
		sys.stdout.write("\n\n")
		return noanswer(user_prefix)




def noanswer(user_prefix):
	words_dragonfire = {
	0 : "I'm not that smart, " + user_prefix + ".",
	1 : "Please, be simple.",
	2 : "Excuse me? I have an average IQ."
	}
	return words_dragonfire[randint(0,2)]

@contextlib.contextmanager
def nostdout():
	save_stdout = sys.stdout
	sys.stdout = io.StringIO()
	yield
	sys.stdout = save_stdout

@contextlib.contextmanager
def nostderr():
	save_stderr = sys.stderr
	sys.stderr = io.StringIO()
	yield
	sys.stderr = save_stderr

if __name__ == "__main__":
	print(YodaQA.answer("http://localhost:4567", "When was Albert Einstein born", "sir"))
