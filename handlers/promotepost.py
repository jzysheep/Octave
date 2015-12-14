import webapp2
import time
import json
from time import strftime
from domain import *
from google.appengine.api import users, search
import heapq

class PromotePost(webapp2.RequestHandler):
    def post(self):
        logged_user = users.get_current_user()
        if not logged_user:
            self.redirect(users.create_login_url(self.request.uri))
        else:
            post_key = ndb.Key(urlsafe=self.request.get("post_key"))
            city = self.request.get("city")
            num_users = self.request.get("num_users")
            logged_user_query = User.gql("WHERE email =:1 ", logged_user.email())
            logged_user_fetch = logged_user_query.get()
            resp = {}

            # find top k active users:
            city_users = User.query(User.city == city).fetch()
            top_k_users = heapq.nlargest(int(num_users), city_users, key=lambda x: x.num_shared_posts)

            for user in top_k_users:
                if str(user.email) != str(logged_user_fetch.email):
                    user.promoted_others_posts.append(post_key)
                    user.put()

            if post_key not in logged_user_fetch.promoted_own_posts:
                logged_user_fetch.promoted_own_posts.append(post_key)
                logged_user_fetch.put()
            resp['promote_status'] = "Promoted"

            time.sleep(0.1)
            self.response.headers['Content-Type'] = 'application/json'
            self.response.out.write(json.dumps(resp))