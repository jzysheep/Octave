from domain import *
import webapp2
from google.appengine.api import users
from time import strftime
from google.appengine.ext.webapp import blobstore_handlers

class MyPlaylist(webapp2.RequestHandler):
    def get(self):
        user=users.get_current_user()
        if user:

            url = users.create_logout_url('/')
            url_linktext = 'Logout'


            user_query = User.gql("WHERE email =:1", user.email())
            user_fetch = user_query.get()
            playlist=Playlist.query(ancestor=user_fetch.key).order(-Playlist.date).fetch()


            values={
               'url_log':url_linktext,
               'url':url,
                'playlist':playlist
                }

            template = JINJA_ENVIRONMENT.get_template('playlist.html')
            self.response.write(template.render(values))



            
class Create(webapp2.RequestHandler):
    def get(self):
        user=users.get_current_user()
        if user:

            url = users.create_logout_url('/')
            url_linktext = 'Logout'

            values={
               'url_log':url_linktext,
               'url':url
                }

            template = JINJA_ENVIRONMENT.get_template('create.html')
            self.response.write(template.render(values))

    def post(self):
        date_created = strftime("%Y-%m-%d %H:%M")
        name=self.request.get('stream_name')
        if self.request.get('image_url'):
            cover_url=self.request.get('image_url')

        else:
            cover_url="http://www.geekersmagazine.com/wp-content/uploads/2012/07/find-songs-music1.jpg"
        privacy=self.request.get('privacy')

        user = users.get_current_user()
        user_query = User.gql("WHERE email =:1", user.email())
        user_fetch = user_query.get()

        playlist=Playlist(parent=user_fetch.key)

        media_query = Media.gql("WHERE upload_check = :1", True)


        media_fetch=media_query.fetch()

        for media in media_fetch:
            if media!=None:
                playlist.populate(
                    name=name,
                    user_key=user_fetch.key,
                    privacy=privacy,
                    date_created=date_created,
                    cover_url=cover_url,
                )
                media.upload_check=False;
                playlist.key_media.append(media.key_media)
                media.put()
            else:
                playlist.populate(
                name=name,
                user_key=user_fetch.key,
                privacy=privacy,
                )

        playlist.put()
        self.redirect('/create_playlist')


class PlaylistUploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        s_time =strftime("%Y/%m/%d")
        now_string = s_time.replace('/','-')
        upload = self.get_uploads()[0]
        media = Media(key_media=upload.key(),upload_check=True, date_created = now_string)
        media.put()
