from domain import *
from time import strftime
from google.appengine.api import users
import webapp2
from collections import OrderedDict
import json
from datetime import datetime, tzinfo,timedelta
from google.appengine.ext.webapp import blobstore_handlers
import time
from google.appengine.ext import blobstore
from google.appengine.ext.db import GqlQuery

class BuddyMusic(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if not user:
            self.redirect(users.create_login_url(self.request.uri))
        else:
            current_user = User.gql("WHERE email =:1", user.email()).get()
            url = users.create_logout_url('/')
            url_linktext = 'Logout'
            user_query = User.query(User.followers == user.email())
            user_fetch = user_query.fetch()
            unordered_posts = []
            ordered_posts = OrderedDict()
            replies = []

            if user_fetch:
                is_self = False
                for user_item in user_fetch:
                    unordered_posts.extend(Post.query(ancestor=user_item.key).fetch())
                unordered_posts.sort(key=lambda x: x.date, reverse=True)
                for post in unordered_posts:
                    post_user = post.user_key.get()
                    post_replies = Reply.query(ancestor=post.key).order(Reply.date).fetch()
                    ordered_posts.append((post, post_user, post_replies))

                if not current_user.signature:
                    user_signature = ""
                else:
                    user_signature = current_user.signature


                values = {
                    'url_log': url_linktext,
                    'url': url,
                    'ordered_posts': ordered_posts,
                    'user_key': current_user.key,
                    'user_name': current_user.name,
                    'user_role': current_user.role,
                    'user_signature': user_signature,
                    'is_self': is_self,
                }

                template = JINJA_ENVIRONMENT.get_template('buddymusic.html')
                self.response.write(template.render(values))

            else:
                self.redirect('/MyMusic')
