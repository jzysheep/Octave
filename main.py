from handlers import *
import webapp2

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/MyMusic', MyMusic),
    ('/signup',SignUp),
    ('/reply', Reply_Handler),
    ('/ajax_reply', ReplyHandlerAjax)
    ], debug=True)

