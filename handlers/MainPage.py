from domain import *
from google.appengine.api import users
import webapp2




class MainPage(webapp2.RequestHandler):
    def get(self):
        user=users.get_current_user()

        if user is not None:
            user_query = User.gql("WHERE email =:1 ",user.email())
            user_fetch=user_query.fetch()

            if user_fetch:
                self.redirect(self.request.uri+'MyMusic')
            else:
                self.redirect(self.request.uri+'signup')

        else:
            url = users.create_login_url(self.request.uri)

            url_linktext = 'Login'
            values={
               'url_log':url_linktext,
               'url':url,
               }

            template = JINJA_ENVIRONMENT.get_template('index.html')
            self.response.write(template.render(values))
