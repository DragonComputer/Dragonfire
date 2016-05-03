import json
import urllib
import urllib2
import time
import sys
import contextlib
import cStringIO
from random import randint
import uuid

class Teachable():

	@staticmethod
	def respond(address, convo_id, query):
		url = address + '/chatbot/conversation_start.php'
		#url = 'http://localhost:4567/q'
		post_params = {
			'say' : query,
			'convo_id' : convo_id
		}

		params = urllib.urlencode(post_params)
		response = urllib2.urlopen(url, params)
		json_response = json.loads(response.read())

		return json_response['botsay']


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
	sys.stdout = cStringIO.StringIO()
	yield
	sys.stdout = save_stdout

@contextlib.contextmanager
def nostderr():
	save_stderr = sys.stderr
	sys.stderr = cStringIO.StringIO()
	yield
	sys.stderr = save_stderr

if __name__ == "__main__":
	convo_id = uuid.uuid4()
	print Teachable.respond("http://teach.dragon.computer/", convo_id, "Learn the sun is hot")
	print Teachable.respond("http://teach.dragon.computer/", convo_id, "What is the sun")
