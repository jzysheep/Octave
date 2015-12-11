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
        user = users.get_current_user()
        if user is not None:
            url = users.create_logout_url('/')
            url_linktext = 'Logout'
            global upload_key
            upload_key=""

            user_query = User.gql("WHERE email =:1", user.email())
            user_fetch = user_query.get()
            replies = []
            posts = []

            if user_fetch:
                posts = Post.query(ancestor=user_fetch.key).order(-Post.date).fetch()
                for count in range(0 , posts.__len__()):
                    temp = Reply.query(ancestor=posts[count].key).order(Reply.date).fetch()
                    replies.insert(count,temp)

                if not user_fetch.signature:
                    user_signature = ""
                else:
                    user_signature = user_fetch.signature

            for post in posts:
                print "BLOB_KEY_MEDIA: " + str(post.blob_key_media)

            values = {
                'url_log': url_linktext,
                'url': url,
                'posts': posts,
                'replies': replies,
                'user_name': user_fetch.name,
                'user_role': user_fetch.role,
                'user_signature': user_signature
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
            blob_key_media=media_fetch.key_media
            )
            media_fetch.upload_check=False;
            media_fetch.put()
        else:
            post.populate(
            date_created=date_created,
            text=post_text,
            user_key=user_fetch.key
            )


        post.put()
        self.redirect('/MyMusic')

        #define a post method for the reply

        #post_query = Post.query(
        # ancestor=).order(-Stream_sub.date).fetch(2)
        # reply_text = self.request.get('reply_text')
        # date_reply_created = strftime("%Y-%m-%d %H:%M")
        # user_key = user_fetch.key
        # post_key = post.key       #which post

class Reply_Handler(webapp2.RequestHandler):
    def post(self):
        print "ENTERED"
        post_nbr=self.request.get('post_nbr')

        print "NBR= " + post_nbr
        date_reply = strftime("%Y-%m-%d %H:%M")

        user = users.get_current_user()
        user_query = User.gql("WHERE email =:1 ", user.email())
        user_fetch = user_query.get()

        posts = Post.query(ancestor=user_fetch.key).order(-Post.date).fetch()

        post_key=posts[int(post_nbr)].key
        reply_text=self.request.get("reply_text_" + post_nbr)

        reply = Reply(parent=post_key)

        reply.populate(
        user_key=user_fetch.key,
        reply=reply_text,
        date_reply = date_reply,
        post_key = post_key
        )

        reply.put()
        self.redirect('/MyMusic')


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

        posts = Post.query(ancestor=user_fetch.key).order(-Post.date).fetch()
        print "post_nbr: " + post_nbr
        post_key=posts[int(post_nbr)].key

        reply_text = self.request.get("reply_text_" + post_nbr)

        reply = Reply(parent=post_key)

        reply.populate(
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


class ViewMediaHandler(blobstore_handlers.BlobstoreDownloadHandler):
    def get(self, media_key):
        if not blobstore.get(media_key):
            self.error(404)
        else:
            self.send_blob(media_key)


class Image(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user is not None:
            user_query = User.gql("WHERE email =:1", user.email())
            user_fetch = user_query.get()


        if(user_fetch.profile_image):
            self.response.headers['Content-Type'] = 'image/png'
            self.response.out.write(user_fetch.profile_image)
        else:
            self.response.out.write('No image')
