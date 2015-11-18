import os
import urllib
from google.appengine.api import users
from google.appengine.ext import ndb
import webapp2
import jinja2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)



class MainPage(webapp2.RequestHandler):
    def get(self):
        user=users.get_current_user()
        if user:
            self.redirect(self.request.uri+'manage')

        else:
            url = users.create_login_url(self.request.uri+'manage')
            url_linktext = 'Login'
            values={
               'url_log':url_linktext,
               'url':url,
               }


            template = JINJA_ENVIRONMENT.get_template('index.html')
            self.response.write(template.render(values))



