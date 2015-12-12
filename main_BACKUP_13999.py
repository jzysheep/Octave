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
<<<<<<< HEAD
    ('/playlist', MyPlaylist),
    ('/manage',Manage),
    ('/playlist_url',PlaylistUploadFormHandler),
    ('/PlaylistUpload',PlaylistUploadHandler),
    ('/create_playlist',Create)
    ], debug=True)
||||||| merged common ancestors
    ('/playlist', Playlist),
    ('/manage',Manage)
    ], debug=True)

=======
    ('/playlist', Playlist),
    ('/manage', Manage),
    ('/autocomplete', SearchAutoComplete)
    ], debug=True)

>>>>>>> a627ecebeaf05efeaa3769b3844d596f305a7832
