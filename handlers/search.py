import webapp2
import re
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
                posts = Post.query(ancestor=searched_user.key).order(-Post.date).fetch()
                for post in posts:
                    post_user = post.user_key.get()
                    post_replies = Reply.query(ancestor=post.key).order(Reply.date).fetch()
                    for reply in post_replies:
                        user_reply.append(reply.user_key.get())
                    post_user_reply.append((post, post_user, post_replies, user_reply))

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
        user = users.get_current_user()
        if not user:
            self.redirect(users.create_login_url(self.request.uri))
        else:
            post_nbr = self.request.get('post_nbr')
            searched_user_email = self.request.get("searched_user_email")
            print searched_user_email
            searched_user = User.gql("WHERE email =:1", searched_user_email).get()
            print "NBR= " + post_nbr
            date_reply = strftime("%Y-%m-%d %H:%M:%S")



            logged_user = users.get_current_user()
            logged_user_query = User.gql("WHERE email =:1 ", logged_user.email())
            logged_user_fetch = logged_user_query.get()

            posts = Post.query(ancestor=searched_user.key).order(-Post.date).fetch()
            print "post_nbr: " + post_nbr
            post_key=posts[int(post_nbr)].key
            reply_text = self.request.get("reply_text_" + post_nbr)

            reply = Reply(parent=post_key)

            reply.populate(
            user_key=logged_user_fetch.key,
            reply=reply_text,
            date_reply = date_reply,
            post_key = post_key
            )

            reply.put()
            resp = {}

            resp['reply_text'] = reply_text
            resp['date_reply'] = date_reply
            resp['post_nbr'] = post_nbr
            resp['user_name'] = logged_user_fetch.name

            print "resp=" + resp['reply_text']

            self.response.headers['Content-Type'] = 'application/json'
            self.response.out.write(json.dumps(resp))
