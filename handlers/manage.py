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

            values={
               'url_log':url_linktext,
               'url':url
                }

            template = JINJA_ENVIRONMENT.get_template('manage.html')
            self.response.write(template.render(values))



class PlaylistUploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        s_time = time.strftime("%Y/%m/%d")
        now_string = s_time.replace('/','-')
        upload = self.get_uploads()[0]
        playlist = Playlist( date_created=now_string)
        playlist.key_media.append(upload.key())
        playlist.put()


