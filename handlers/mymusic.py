from domain import *
from time import strftime
from google.appengine.api import users
import webapp2

class MyMusic(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user is not None:
            url = users.create_logout_url('/')
            url_linktext = 'Logout'
            
            user_query = User.gql("WHERE email =:1", user.email())
            user_fetch = user_query.get()
            replies = []
            posts = []

            if user_fetch:
                posts = Post.query(ancestor=user_fetch.key).order(-Post.date).fetch()
                for count in range(0 , posts.__len__()):
                    temp = Reply.query(ancestor=posts[count].key).order(Reply.date).fetch()
                    #if temp == []:
                        #replies.insert(count,None)
                    #else:
                    replies.insert(count,temp)


            values = {
               'url_log': url_linktext,
               'url': url,
               'posts': posts,
               'replies': replies
                }

            template = JINJA_ENVIRONMENT.get_template('mymusic.html')
            self.response.write(template.render(values))

    def post(self):
        post_text = self.request.get('post_text')
        date_created = strftime("%Y-%m-%d %H:%M")

        user = users.get_current_user()
        user_query = User.gql("WHERE email =:1 ", user.email())
        user_fetch = user_query.get()

        post = Post(parent=user_fetch.key)

        post.populate(
        date_created=date_created,
        text=post_text,
        user_key=user_fetch.key
        )

        post.put()

        self.redirect('/MyMusic')


        #define a post method for the reply

        #post_query = Post.query(
        #    ancestor=).order(-Stream_sub.date).fetch(2)
        #
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

