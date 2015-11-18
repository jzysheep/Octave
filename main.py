import MainPage
from MainPage import * 
import domain.models
from domain.models import *

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ], debug=True)

