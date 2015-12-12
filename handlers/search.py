import webapp2
import time
import json
from time import strftime
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
            searched_user = user_query.get()
            post_user_reply = []
            user_reply = []

            if searched_user:
                if user.email() == searched_user.email:
                    is_self = True
                else:
                    is_self = False
                posts = Post.query(Post.user_key == searched_user.key).order(-Post.date).fetch()
                for post in posts:
                    post_user = post.user_key.get()
                    post_replies = Reply.query(Reply.post_key == post.key).order(Reply.date).fetch()
                    for reply in post_replies:
                        user_reply.append(reply.user_key.get())
                        # print "reply" + reply.reply
                        # print "user" + reply.user_key.get().name
                    post_user_reply.append((post, post_user, post_replies, user_reply))

                # for i in range(len(post_user_reply)):
                #     for j in range(len(post_user_reply[i][2])):
                #         print "reply " + post_user_reply[i][2][j].reply
                #         print "user " + post_user_reply[i][3][j].name
                if not searched_user.signature:
                    user_signature = ""
                else:
                    user_signature = searched_user.signature

                if user.email() in searched_user.followers:
                    follow_button = "Unfollow"
                else:
                    follow_button = "Follow"


                values = {
                    'url_log': url_linktext,
                    'url': url,
                    'post_user_reply': post_user_reply,
                    'searched_user': searched_user,
                    'logged_user': User.gql("WHERE email =:1", user.email()).get(),
                    'is_self': is_self,
                    'follow_button': follow_button
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
            date_reply = strftime("%Y-%m-%d %H:%M:%S")

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
