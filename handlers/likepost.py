import webapp2
import re
import json
from time import strftime
from domain import *
from google.appengine.api import users, search

class LikePost(webapp2.RequestHandler):
    def post(self):
        pass
