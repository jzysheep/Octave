import webapp2
import time
import json
from time import strftime
from domain import *
from google.appengine.api import users, search

class SharePost(webapp2.RequestHandler):
    def post(self):
        logged_user = users.get_current_user()
        if not logged_user:
            self.redirect(users.create_login_url(self.request.uri))
        else:
            post_key = ndb.Key(urlsafe=self.request.get("post_key"))
            logged_user_query = User.gql("WHERE email =:1 ", logged_user.email())
            logged_user_fetch = logged_user_query.get()
            resp = {}

            if post_key not in logged_user_fetch.shared_posts:
                logged_user_fetch.shared_posts.append(post_key)
                logged_user_fetch.put()
                post_user = post_key.get().user_key.get()
                post_user.num_shared_posts += 1
            resp['share_status'] = "Shared"

            time.sleep(0.1)
            self.response.headers['Content-Type'] = 'application/json'
            self.response.out.write(json.dumps(resp))