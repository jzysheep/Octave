import webapp2
import time
from domain import *
from google.appengine.ext import blobstore
from google.appengine.api import users
from google.appengine.api import images

class SignUp(webapp2.RequestHandler):
    def get(self):
        user=users.get_current_user()
        if user:
            url = users.create_logout_url('/')
            url_linktext = 'Logout'


            values={
               'url_log':url_linktext,
               'url':url
                }

            template = JINJA_ENVIRONMENT.get_template('signup.html')
            self.response.write(template.render(values))

    def post(self):
        user_curr=users.get_current_user()
        name=self.request.get('name')
        city=self.request.get('city')
        role=self.request.get('role')
        signature=self.request.get('signature')

        upload_url = blobstore.create_upload_url('/_ah/upload')

        user=User()
        user.populate(email=user_curr.email(),city=city,name=name,role=role,signature=signature)
        if self.request.get('photo'):
            image= self.request.get('photo')
            image = images.resize(image, 256, 256)
            user.profile_image=image

        user.put()
        time.sleep(0.1)

        self.redirect('/MyMusic')

