from __future__ import print_function
import hug
from hug_middleware_cors import CORSMiddleware
import waitress
from threading import Thread


@hug.get('/happy_birthday')
def happy_birthday(name, age:hug.types.number=1):
    """Says happy birthday to a user"""
    return "Happy {age} Birthday {name}!".format(**locals())


class Run():
    def __init__(self, nlp):
        self.nlp = nlp  # Load en_core_web_sm, English, 50 MB, default model
        app = hug.API(__name__)
        app.http.add_middleware(CORSMiddleware(app))
        t = Thread(target=waitress.serve, args=(__hug_wsgi__, ), kwargs={"port": 3301})
        t.start()
        t.join()


if __name__ == '__main__':
    app = hug.API(__name__)
    app.http.add_middleware(CORSMiddleware(app))
    waitress.serve(__hug_wsgi__, port=8000)
