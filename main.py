import MainPage
from MainPage import * 
import domain.models
from domain.models import *
from home import *
from mymusic import *
from signup import *

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/music', Music),
    ('/MyMusic', MyMusic),
    ('/signup',SignUp),

    ], debug=True)

