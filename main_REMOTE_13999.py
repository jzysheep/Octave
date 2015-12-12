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
    ('/search', SearchUser),
    ('/follow', FollowUser),
    ('/profile_img',Image),
    ('/playlist', Playlist),
    ('/manage', Manage),
    ('/autocomplete', SearchAutoComplete)
    ], debug=True)

