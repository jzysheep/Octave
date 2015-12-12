import webapp2
import time
import json
from time import strftime
from domain import *
from google.appengine.api import users, search

class LikePost(webapp2.RequestHandler):
    def post(self):
        logged_user = users.get_current_user()
        if not logged_user:
            self.redirect(users.create_login_url(self.request.uri))
        else:
            print "post_key" + self.request.get("post_key")
            post_key = ndb.Key(urlsafe=self.request.get("post_key"))



            liked_post = post_key.get()
            logged_user_query = User.gql("WHERE email =:1 ", logged_user.email())
            logged_user_fetch = logged_user_query.get()
            like_get = Like.query(ndb.AND(Like.user_key == logged_user_fetch.key, Like.post_key == post_key)).get()
            if like_get is None:
                print "None"
                liked_post.likes += 1
                like = Like(user_key=logged_user_fetch.key, post_key=post_key)
                like.put()
            else:
                print "exists"
                liked_post.likes -= 1
                like_get.key.delete()
            liked_post.put()
            time.sleep(0.1)
            resp = {}
            resp['like_nbr'] = liked_post.likes
            self.response.headers['Content-Type'] = 'application/json'
            self.response.out.write(json.dumps(resp))


