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
        logged_user = users.get_current_user()
        if not logged_user:
            self.redirect(users.create_login_url(self.request.uri))
        else:
            ######################ADD THIS#########

            links=[]
            media_types=[]
            ######################End ADD#########

            logged_user_query = User.gql("WHERE email =:1 ", logged_user.email())
            logged_user_fetch = logged_user_query.get()
            url = users.create_logout_url('/')
            url_linktext = 'Logout'
            followed_user_query = User.query(User.followers == logged_user.email())
            followed_user_fetch = followed_user_query.fetch()
            unordered_posts = []
            post_user_reply = []

            if followed_user_fetch:
                is_self = False
                for user_item in followed_user_fetch:
                    unordered_posts.extend(Post.query(Post.user_key == user_item.key).fetch())
                    for post_key in user_item.shared_posts:
                        post = post_key.get()
                        if post not in unordered_posts:
                            unordered_posts.append(post)
                unordered_posts.sort(key=lambda x: x.date, reverse=True)
                for post in unordered_posts:
                    if post.key in logged_user_fetch.shared_posts:
                        posts_share = "Shared"
                    else:
                        posts_share = "Share"
                    post_user = post.user_key.get()
                    post_replies = Reply.query(Reply.post_key == post.key).order(Reply.date).fetch()
                    user_reply = []
                    for reply in post_replies:
                        user_reply.append(reply.user_key.get())
                    post_user_reply.append((post, post_user, post_replies, user_reply, posts_share))

######################ADD THIS#########
                    media_query = Media.gql("WHERE key_media = :1", post.blob_key_media)
                    if post.link!=None:
                        links.append(post.link)
                        print "LINKS SAVED: "
                        print post.link

                    entity=media_query.get()
                    if entity!=None:
                        media_types.append(entity.media_type)
######################End ADD#########


                values = {
                    'url_log': url_linktext,
                    'url': url,
                    'post_user_reply': post_user_reply,
                    'logged_user': logged_user_fetch,
                    'is_self': is_self,
                    'media_types': media_types,
                    'links':links

                }

                template = JINJA_ENVIRONMENT.get_template('buddymusic.html')
                self.response.write(template.render(values))

            else:
                self.redirect('/MyMusic')
