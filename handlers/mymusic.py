from domain import *
from time import strftime
from google.appengine.api import users
import webapp2
import json
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
import time
import heapq
from google.appengine.ext import blobstore
from google.appengine.ext.db import GqlQuery
import re


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

            if logged_user_fetch:
                if logged_user_fetch.role == 'Artist':
                    is_artist = True
                else:
                    is_artist = False

                post_user_reply = []

                posts = Post.query(Post.user_key == logged_user_fetch.key).fetch()

                for post_key in logged_user_fetch.shared_posts:
                    posts.append(post_key.get())

                for post_key in logged_user_fetch.promoted_others_posts:
                    if post_key.get() not in posts:
                        posts.append(post_key.get())

                posts.sort(key=lambda x: x.date, reverse=True)

                media_types=[]
                links=[]
                for post in posts:
                    media_query = Media.gql("WHERE key_media = :1", post.blob_key_media)
                    if post.links:
                        links.append(post.links[0])
                        print "LINKS SAVED: "
                        print post.links[0]

                    entity=media_query.get()
                    if entity!=None:
                        media_types.append(entity.media_type)



                for post in posts:
                    post_user = post.user_key.get()
                    post_replies = Reply.query(Reply.post_key == post.key).order(Reply.date).fetch()
                    user_reply = []


                    if post.key in logged_user_fetch.shared_posts:
                        is_share = True
                        share_status = "Shared from " + post_user.name
                    else:
                        is_share = False
                        share_status = ""

                    if post.key in logged_user_fetch.promoted_own_posts:
                        is_promoted_own = True
                        promoted_own_status = "Promoted"
                    else:
                        is_promoted_own = False
                        promoted_own_status = "Promote"

                    if post.key in logged_user_fetch.promoted_others_posts:
                        is_promoted_others = True
                        promoted_others_status = "Promoted from " + post_user.name
                    else:
                        is_promoted_others = False
                        promoted_others_status = ""

                    for reply in post_replies:
                        user_reply.append(reply.user_key.get())
                    post_user_reply.append((post, post_user, post_replies, user_reply, is_share, share_status, is_promoted_own, promoted_own_status, is_promoted_others, promoted_others_status))




                # You might like section:
                all_users = User.query(User.email != logged_user_fetch.email).fetch()
                 # choose top k uses which has the most shared posts
                top_k_users = heapq.nlargest(8, all_users, key=lambda x: x.num_shared_posts)


                values = {
                    'url_log': url_linktext,
                    'url': url,
                    'logged_user': logged_user_fetch,
                    'post_user_reply': post_user_reply,
                    'is_self': True,
                    'is_artist': is_artist,
                    'top_k_users': top_k_users,
                    'media_types': media_types,
                    'links':links
                }

                template = JINJA_ENVIRONMENT.get_template('mymusic.html')
                self.response.write(template.render(values))
            else:
                self.redirect('/signup')

    def post(self):
        post_text = self.request.get('post_text')
        date_created = strftime("%Y-%m-%d %H:%M")

        grp = re.search("(?P<url>https?://[^\s]+)", post_text)\

        if grp:
            link=grp.group("url")
        else:
            link=""

        print "link: " + link

        user = users.get_current_user()
        user_query = User.gql("WHERE email =:1 ", user.email())
        user_fetch = user_query.get()

        media_query = Media.gql("WHERE upload_check = :1", True)

        post = Post(parent=user_fetch.key)

        youtube_regex = (
            r'(https?://)?(www\.)?'
            '(youtube|youtu|youtube-nocookie)\.(com|be)/'
            '(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')

        if link!="":
            youtube_regex_match = re.match(youtube_regex, link)
            if youtube_regex_match:
                id= youtube_regex_match.group(6)
            else:
                id= youtube_regex_match

            link = "https://www.youtube.com/embed/" + id


        media_fetch=media_query.get()
        if media_fetch!=None:
            post.populate(
            date_created=date_created,
            text=post_text,
            user_key=user_fetch.key,
            blob_key_media=media_fetch.key_media,
            likes=0,
            )
            media_fetch.upload_check=False;
            media_fetch.put()
        else:
            post.populate(
            date_created=date_created,
            text=post_text,
            user_key=user_fetch.key,
            likes=0,
            )

        media_link = Media(link=link)
        media_link.put()

        post.links.append(link)
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
        blob_info = blobstore.BlobInfo.get(upload.key())
        filename=blob_info.filename
        if '.mp3' in filename:
            type='audio'
        else:
            type='video'

        user_media = Media(key_media=upload.key(),upload_check=True,views=0, date_created=now_string,media_type=type)
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
