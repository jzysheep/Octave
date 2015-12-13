from domain import *
import webapp2
from google.appengine.api import users
from google.appengine.ext.webapp import blobstore_handlers
import time
from google.appengine.ext import blobstore

            
class Manage(webapp2.RequestHandler):
    def get(self):
        user=users.get_current_user()
        if user:

            url = users.create_logout_url('/')
            url_linktext = 'Logout'

            user_query = User.gql("WHERE email =:1", user.email())
            user_fetch = user_query.get()

            playlist_name=self.request.get('playlist')
            playlist_query=Playlist.gql("WHERE name =:1", playlist_name)
            playlist = playlist_query.get()

            media_query = Media.gql("WHERE upload_check = :1", True)
            media_fetch = media_query.fetch()


            for media in media_fetch:
                if media!=None:
                    media.upload_check=False;
                    playlist.key_media.append(media.key_media)
                    playlist.media_name.append(media.name)
                    media.put()


            playlist.put()



            links_uploaded=[]

            for key in playlist.key_media:
                links_uploaded.append(key)

            values={
               'url_log':url_linktext,
               'url':url,
               'links_uploaded':links_uploaded,
               'playlist_name':playlist.name,
               'playlist_cover':playlist.cover_url,
               'media_name':playlist.media_name
                }



            template = JINJA_ENVIRONMENT.get_template('manage.html')
            self.response.write(template.render(values))








