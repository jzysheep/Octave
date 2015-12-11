from domain import *
import webapp2
from google.appengine.api import users
from google.appengine.ext import blobstore

            
class Playlist(webapp2.RequestHandler):
    def get(self):
        user=users.get_current_user()
        if user:

            url = users.create_logout_url('/')
            url_linktext = 'Logout'

            values={
               'url_log':url_linktext,
               'url':url
                }


            template = JINJA_ENVIRONMENT.get_template('playlist.html')
            self.response.write(template.render(values))



            
class Create(webapp2.RequestHandler):
    def get(self):
        user=users.get_current_user()
        if user:

            url = users.create_logout_url('/')
            url_linktext = 'Logout'

            values={
               'url_log':url_linktext,
               'url':url
                }


            template = JINJA_ENVIRONMENT.get_template('create.html')
            self.response.write(template.render(values))
