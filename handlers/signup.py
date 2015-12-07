import webapp2

from domain import *
from google.appengine.api import users
import time


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


        user=User()
        user.populate(email=user_curr.email(),city=city,name=name,role=role,signature=signature)
        user.put()
        time.sleep(0.1)
        self.redirect('/MyMusic')
    
