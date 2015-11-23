from domain.models import *
import os
from google.appengine.api import users
from google.appengine.ext import ndb
import webapp2
import jinja2
from google.appengine.ext.db import GqlQuery

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)



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
