from domain import *
from time import strftime
from google.appengine.api import users
import webapp2
import json
from datetime import datetime, tzinfo,timedelta
from google.appengine.ext.webapp import blobstore_handlers
import time
from google.appengine.ext import blobstore
from google.appengine.ext.db import GqlQuery

class BuddyMusic(webapp2.RequestHandler):
    def get(self):
        # user = users.get_current_user()
        # if not user:
        #     self.redirect(users.create_login_url(self.request.uri))
        # else:
        #     url = users.create_logout_url('/')
        #     url_linktext = 'Logout'
        #     user_query = User.query(User.followers == user.email())
        #     user_fetch = user_query.get()
        #     posts = []
        #     replies = []
        #
        #     if user_fetch:
        #         is_self = False
        #         for user_item in user_fetch:
        #             posts.extend(Post.query(ancestor=user_item.key).order(-Post.date).fetch())
        #         for count in range(len(posts)):
        #             replies.append(Reply.query(ancestor=posts[count].key).order(Reply.date).fetch())
        #
        #         if not user_fetch.signature:
        #             user_signature = ""
        #         else:
        #             user_signature = user_fetch.signature
        #
        #         if user.email() in user_fetch.followers:
        #             follow_button = "Unfollow"
        #         else:
        #             follow_button = "Follow"
        #
        #         values = {
        #             'url_log': url_linktext,
        #             'url': url,
        #             'posts': posts,
        #             'replies': replies,
        #             'user_key': user_fetch.key,
        #             'user_name': user_fetch.name,
        #             'user_role': user_fetch.role,
        #             'user_signature': user_signature,
        #             'is_self': is_self,
        #         }
        #
        #         template = JINJA_ENVIRONMENT.get_template('mymusic.html')
        #         self.response.write(template.render(values))
        #
        #     else:
        #         self.redirect('/MyMusic')
        pass