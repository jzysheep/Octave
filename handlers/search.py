import webapp2
import time
import json
from time import strftime
from domain import *
from google.appengine.api import users, search

class SearchUser(webapp2.RequestHandler):
    def get(self):
        logged_user = users.get_current_user()
        if not logged_user:
            self.redirect(users.create_login_url(self.request.uri))
        else:
            url = users.create_logout_url('/')
            url_linktext = 'Logout'
            search_str = self.request.get("search_str").strip()
            user_query = User.query(User.name == search_str)
            logged_user_query = User.gql("WHERE email =:1 ", logged_user.email())
            logged_user_fetch = logged_user_query.get()
            searched_user = user_query.get()
            post_user_reply = []
            ######################End ADD#########

            links=[]
            media_types=[]

            ######################End ADD#########

            if searched_user:
                if logged_user.email() == searched_user.email:
                    is_self = True
                    self.redirect('/MyMusic')
                else:
                    is_self = False
                posts = Post.query(Post.user_key == searched_user.key).fetch()

                for post_key in searched_user.shared_posts:
                    posts.append(post_key.get())

                posts.sort(key=lambda x: x.date, reverse=True)

                logged_user_posts = Post.query(Post.user_key == logged_user_fetch.key).fetch()

                for post in posts:
                    if post in logged_user_posts:
                        posts_ownedby_logged_user = True
                    else:
                        posts_ownedby_logged_user = False
                    if post.key in logged_user_fetch.shared_posts:
                        posts_share = "Shared"
                    else:
                        posts_share = "Share"
                    post_user = post.user_key.get()
                    post_replies = Reply.query(Reply.post_key == post.key).order(Reply.date).fetch()
                    user_reply = []
                    for reply in post_replies:
                        user_reply.append(reply.user_key.get())
                    post_user_reply.append((post, post_user, post_replies, user_reply, posts_share, posts_ownedby_logged_user))
######################End ADD#########

                    media_query = Media.gql("WHERE key_media = :1", post.blob_key_media)
                    if post.link!=None:
                        links.append(post.link)
                        print "LINKS SAVED: "
                        print post.link

                    entity=media_query.get()
                    if entity!=None:
                        media_types.append(entity.media_type)
######################End ADD#########

                if logged_user.email() in searched_user.followers:
                    follow_button = "Unfollow"
                else:
                    follow_button = "Follow"


                values = {
                    'url_log': url_linktext,
                    'url': url,
                    'post_user_reply': post_user_reply,
                    'searched_user': searched_user,
                    'logged_user': User.gql("WHERE email =:1", logged_user.email()).get(),
                    'is_self': is_self,
                    'follow_button': follow_button,
                    'media_types': media_types,
                    'links':links

                }

                template = JINJA_ENVIRONMENT.get_template('search.html')
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

class SearchReplyHandlerAjax(webapp2.RequestHandler):
    def post(self):
        logged_user = users.get_current_user()
        if not logged_user:
            self.redirect(users.create_login_url(self.request.uri))
        else:
            post_key = ndb.Key(urlsafe=self.request.get("post_key"))
            # date_reply = strftime("%Y-%m-%d %H:%M:%S")
            date = self.request.get('date_reply')

            # print date
            date_reply = date[:-15]

            logged_user_query = User.gql("WHERE email =:1 ", logged_user.email())
            logged_user_fetch = logged_user_query.get()

            reply_text = self.request.get("reply_text")
            print "reply_text" + reply_text
            print "post_key" + self.request.get("post_key")
            print logged_user_fetch.name
            print logged_user_fetch.key




            reply = Reply(
                user_key=logged_user_fetch.key,
                reply=reply_text,
                date_reply=date_reply,
                post_key=post_key
            )

            reply.put()
            time.sleep(0.1)
            resp = {}

            resp['reply_text'] = reply_text
            resp['date_reply'] = date_reply
            resp['user_name'] = logged_user_fetch.name

            print "resp=" + resp['reply_text']

            self.response.headers['Content-Type'] = 'application/json'
            self.response.out.write(json.dumps(resp))
