import webapp2

from domain import *
from google.appengine.api import users
import json

class FollowUser(webapp2.RequestHandler):
    def post(self):
        user = users.get_current_user()
        if not user:
            self.redirect(users.create_login_url(self.request.uri))
        else:
            user_key = ndb.Key(urlsafe=self.request.get("user_key"))
            followed_user = user_key.get()
            follower_list = followed_user.followers
            resp = {}
            if user.email() not in follower_list:
                follower_list.append(user.email())
                resp['follow_button'] = 'Unfollow'

            else:
                follower_list.remove(user.email())
                resp['follow_button'] = 'Follow'

            followed_user.put()
            self.response.headers['Content-Type'] = 'application/json'
            self.response.out.write(json.dumps(resp))


