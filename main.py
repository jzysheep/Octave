from handlers import *
import webapp2

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/MyMusic', MyMusic),
    ('/signup',SignUp),
    ('/_ah/upload', MediaUploadHandler),
    ('/media_url', MediaUploadFormHandler),
    ('/ajax_reply', ReplyHandlerAjax),
    ('/search_ajax_reply', SearchReplyHandlerAjax),
    ('/view_media/([^/]+)?', ViewMediaHandler),
    ('/search', SearchUser),
    ('/follow', FollowUser),
    ('/profile_img',Image),
    ('/playlist', Playlist),
    ('/manage', Manage),
    ('/autocomplete', SearchAutoComplete),
    ('/like_post', LikePost),
    ('/buddymusic', BuddyMusic),
  ('/playlist_url',PlaylistUploadFormHandler),
  ('/PlaylistUpload',PlaylistUploadHandler),
    ('/create_playlist',Create)
    ], debug=True)

