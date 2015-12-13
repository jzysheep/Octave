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

class MyMusic(webapp2.RequestHandler):
    def get(self):
        logged_user = users.get_current_user()
        if not logged_user:
            self.redirect(users.create_login_url(self.request.uri))
        else:
            url = users.create_logout_url('/')
            url_linktext = 'Logout'


            logged_user_query = User.gql("WHERE email =:1 ", logged_user.email())
            logged_user_fetch = logged_user_query.get()

            post_user_reply = []

            posts = Post.query(Post.user_key == logged_user_fetch.key).fetch()

            for post_key in logged_user_fetch.shared_posts:
                posts.append(post_key.get())

            posts.sort(key=lambda x: x.date, reverse=True)

            for post in posts:
                post_user = post.user_key.get()
                post_replies = Reply.query(Reply.post_key == post.key).order(Reply.date).fetch()
                user_reply = []
                for reply in post_replies:
                    user_reply.append(reply.user_key.get())
                post_user_reply.append((post, post_user, post_replies, user_reply))


            values = {
                'url_log': url_linktext,
                'url': url,
                'logged_user': logged_user_fetch,
                'post_user_reply': post_user_reply,
                'is_self': True
            }

            template = JINJA_ENVIRONMENT.get_template('mymusic.html')
            self.response.write(template.render(values))


    def post(self):
        post_text = self.request.get('post_text')
        date_created = strftime("%Y-%m-%d %H:%M")

        user = users.get_current_user()
        user_query = User.gql("WHERE email =:1 ", user.email())
        user_fetch = user_query.get()

        media_query = Media.gql("WHERE upload_check = :1", True)

        post = Post(parent=user_fetch.key)

        media_fetch=media_query.get()
        if media_fetch!=None:
            post.populate(
            date_created=date_created,
            text=post_text,
            user_key=user_fetch.key,
            blob_key_media=media_fetch.key_media,
            likes=0
            )
            media_fetch.upload_check=False;
            media_fetch.put()
        else:
            post.populate(
            date_created=date_created,
            text=post_text,
            user_key=user_fetch.key,
            likes=0
            )

        post.put()
        time.sleep(0.1)
        self.redirect('/MyMusic')

        #define a post method for the reply

        #post_query = Post.query(
        # ancestor=).order(-Stream_sub.date).fetch(2)
        # reply_text = self.request.get('reply_text')
        # date_reply_created = strftime("%Y-%m-%d %H:%M")
        # user_key = user_fetch.key
        # post_key = post.key       #which post



class ReplyHandlerAjax(webapp2.RequestHandler):
    def post(self):

        post_nbr = self.request.get('post_nbr')

        print "NBR= " + post_nbr
        date_reply = strftime("%Y-%m-%d %H:%M:%S")
    #   date_reply = datetime.now()
    #  date_reply = date_reply.replace(tzinfo=UTC())



        user = users.get_current_user()
        user_query = User.gql("WHERE email =:1 ", user.email())
        user_fetch = user_query.get()

        posts = Post.query(Post.user_key == user_fetch.key).order(-Post.date).fetch()
        print "post_nbr: " + post_nbr
        post_key=posts[int(post_nbr)].key
        reply_text = self.request.get("reply_text_" + post_nbr)

        reply = Reply(
            user_key=user_fetch.key,
            reply=reply_text,
            date_reply = date_reply,
            post_key = post_key
        )
        reply.put()
        resp = {}

        resp['reply_text'] = reply_text
        resp['date_reply'] = date_reply
        resp['post_nbr'] = post_nbr
        resp['user_name'] = user_fetch.name

        print "resp=" + resp['reply_text']

        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(resp))

class MediaUploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        s_time = time.strftime("%Y/%m/%d")
        now_string = s_time.replace('/','-')
        upload = self.get_uploads()[0]
        user_media = Media(key_media=upload.key(),upload_check=True,views=0, date_created=now_string)
        user_media.put()
        time.sleep(0.1)

class ViewMediaHandler(blobstore_handlers.BlobstoreDownloadHandler):
    def get(self, media_key):
        if not blobstore.get(media_key):
            self.error(404)
        else:
            self.send_blob(media_key)


class Image(webapp2.RequestHandler):
    def get(self):
        user_query = User.gql("WHERE email =:1", self.request.get('email'))
        user_fetch = user_query.get()

        if(user_fetch.profile_image):
            self.response.headers['Content-Type'] = 'image/png'
            self.response.out.write(user_fetch.profile_image)
        else:
            self.response.out.write('No image')
