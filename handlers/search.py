import webapp2
import re
import json

from domain import *
from google.appengine.api import users, search

class SearchUser(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if not user:
            self.redirect(users.create_login_url(self.request.uri))
        else:
            url = users.create_logout_url('/')
            url_linktext = 'Logout'
            search_str = self.request.get("search_str").strip()
            user_query = User.query(User.name == search_str)
            user_fetch = user_query.get()
            replies = []
            posts = []

            if user_fetch:
                if user.email() == user_fetch.email:
                    is_self = True
                else:
                    is_self = False
                posts = Post.query(ancestor=user_fetch.key).order(-Post.date).fetch()
                for count in range(len(posts)):
                    replies.append(Reply.query(ancestor=posts[count].key).order(Reply.date).fetch())

                if not user_fetch.signature:
                    user_signature = ""
                else:
                    user_signature = user_fetch.signature

                if user.email() in user_fetch.followers:
                    follow_button = "Unfollow"
                else:
                    follow_button = "Follow"

                values = {
                    'url_log': url_linktext,
                    'url': url,
                    'posts': posts,
                    'replies': replies,
                    'user_key': user_fetch.key,
                    'user_name': user_fetch.name,
                    'user_role': user_fetch.role,
                    'user_signature': user_signature,
                    'is_self': is_self,
                    'follow_button': follow_button
                }

                template = JINJA_ENVIRONMENT.get_template('mymusic.html')
                self.response.write(template.render(values))

            else:
                self.redirect('/MyMusic')

class SearchAutoComplete(webapp2.RequestHandler):
    def get(self):
        search_str = self.request.get("term")
        print search_str
        resp = dict()
        resp['user_names'] = []

        user_list = User.query()
        for user in user_list:
            if user.name.startswith(search_str):
                resp['user_names'].append(user.name)

        self.response.out.write(json.dumps(resp))