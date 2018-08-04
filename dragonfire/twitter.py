#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: twitter
    :platform: Unix
    :synopsis: the top-level submodule of Dragonfire that contains the classes to provide Twitter chatbot functionality to Dragonfire.

.. moduleauthor:: Mehmet Mert Yıldıran <mert.yildiran@bil.omu.edu.tr>
"""

try:
    import thread  # Low-level threading API
except ImportError:
    import _thread as thread  # Low-level threading API
import json  # JSON encoder and decoder
import re  # Regular expression operations
from tweepy.streaming import StreamListener  # An easy-to-use Python library for accessing the Twitter API
from dragonfire import VirtualAssistant  # The class to create a virtual assistant


class MentionListener(StreamListener):
    """ A listener handles tweets that are received from the stream.
    """

    def __init__(self, args, userin):
        """Initialization method of :class:`dragonfire.twitter.MentionListener` class.

        Args:
            args:       Command-line arguments.
            userin:     :class:`dragonfire.utilities.TextToAction` instance.
        """

        self.args = args
        self.userin = userin

    def on_data(self, data):
        """Method that called whenever someone tweeted Dragonfire with a mention.

        Args:
            data (str):  String that contains data of the tweet.
        """

        mention = json.loads(data)
        # print(json.dumps(mention, indent=4, sort_keys=True))
        if 'retweeted_status' not in mention:
            tw_text = mention['text']
            tw_user = mention['user']['screen_name']
            if tw_user == "DragonfireAI":
                return True
            user_full_name = mention['user']['name']
            user_prefix = mention['user']['name'].split()[0]
            print("\n@" + tw_user + " said:")
            print(tw_text)
            tw_text = tw_text.replace("@DragonfireAI", "")
            tw_text = re.sub(r'([^\s\w\?]|_)+', '', tw_text).strip()
            her = VirtualAssistant(self.args, self.userin, user_full_name, user_prefix, tw_user)
            thread.start_new_thread(her.command, (tw_text,))
        return True

    def on_error(self, status):
        """Method that called when an error occurred.

        Args:
            status (str):  String that holds information about the error.
        """

        print(status)
