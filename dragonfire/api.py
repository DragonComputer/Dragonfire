from __future__ import print_function
import collections  # Imported to support ordered dictionaries in Python
import hug
from hug_middleware_cors import CORSMiddleware
import waitress
from threading import Thread
import json

nlp = None

@hug.get('/tag')
def tagger(text):
    data = collections.OrderedDict()
    doc = nlp(text)
    for token in doc:
        parse = {
            'lemma': token.lemma_,
            'pos': token.pos_,
            'tag': token.tag_,
            'dep': token.dep_,
            'shape': token.shape_,
            'is_alpha': token.is_alpha,
            'is_stop': token.is_stop
            }
        data[token.text] = parse
    return json.dumps(data)


class Run():
    def __init__(self, nlpRef):
        global nlp
        nlp = nlpRef  # Load en_core_web_sm, English, 50 MB, default model
        app = hug.API(__name__)
        app.http.output_format = hug.output_format.text
        app.http.add_middleware(CORSMiddleware(app))
        t = Thread(target=waitress.serve, args=(__hug_wsgi__, ), kwargs={"port": 3301})
        t.start()
        t.join()


if __name__ == '__main__':
    app = hug.API(__name__)
    app.http.output_format = hug.output_format.text
    app.http.add_middleware(CORSMiddleware(app))
    waitress.serve(__hug_wsgi__, port=8000)
