from MainPage import *
from domain.models import *
from time import strftime

from google.appengine.ext import ndb

class MyMusic(webapp2.RequestHandler):
    def get(self):
        user=users.get_current_user()
        if user:
            url = users.create_logout_url('/')
            url_linktext = 'Logout'


            values={
               'url_log':url_linktext,
               'url':url
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




        #define a post method for the reply

        #post_query = Post.query(
        #    ancestor=).order(-Stream_sub.date).fetch(2)
        #
        # reply_text = self.request.get('reply_text')
        # date_reply_created = strftime("%Y-%m-%d %H:%M")
        # user_key = user_fetch.key
        # post_key = post.key       #which post
        self.redirect('/music')