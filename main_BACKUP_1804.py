from handlers import *
import webapp2

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/MyMusic', MyMusic),
    ('/signup',SignUp),
    ('/reply', Reply_Handler),
    ('/_ah/upload', MediaUploadHandler),
    ('/media_url', MediaUploadFormHandler),
    ('/reply', Reply_Handler),
    ('/ajax_reply', ReplyHandlerAjax),
    ('/view_media/([^/]+)?', ViewMediaHandler),
<<<<<<< HEAD
    ('/search', SearchUser),
    ('/follow', FollowUser)
=======
    ('/profile_img',Image),
    ('/playlist', Playlist),
    ('/manage',Manage)
>>>>>>> a9cf6a4215ada9a4138b1c1219de45c324f0efb0
    ], debug=True)

