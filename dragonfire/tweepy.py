try:
    import thread  # Low-level threading API
except ImportError:
    import _thread as thread  # Low-level threading API
import json  # JSON encoder and decoder
import re  # Regular expression operations
from tweepy.streaming import StreamListener
from dragonfire import VirtualAssistant


class MentionListener(StreamListener):
    """ A listener handles tweets that are received from the stream.
    This is a basic listener that just prints received tweets to stdout.

    """

    def __init__(self, args, userin):
        self.args = args
        self.userin = userin

    def on_data(self, data):
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
        print(status)
