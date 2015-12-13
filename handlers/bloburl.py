import json
import webapp2
from google.appengine.api import users
from google.appengine.ext import blobstore
import time
from domain import *
import urllib
class MediaUploadFormHandler(webapp2.RequestHandler):
    def post(self):
        user=users.get_current_user()
        if user:
            upload_url = blobstore.create_upload_url('/_ah/upload')

            self.response.headers["Content-Type"] = "application/json"

            res = {
                'code': 200,
                'response':upload_url
                 }
            #print upload_url
            print json.dumps(res)
            self.response.write(json.dumps(res))



class PlaylistUploadFormHandler(webapp2.RequestHandler):
    def post(self):
        user=users.get_current_user()
        if user:
            # media_name = self.request.get('media_name')
            # # files_nbr = self.request.get('nbr')
            # print "media name from front end: " +  media_name
            upload_url = blobstore.create_upload_url('/PlaylistUpload')
            # upload_url=str(upload_url) + '?media_name=' + media_name

            # upload_ur=urllib.urlencode({'media_name':media_name,'key_upload':upload_url})

            print upload_url



            # user_query = User.gql("WHERE email =:1", user.email())
            # user_fetch = user_query.get()

            # media = Media(parent=user_fetch.key)
            # media.name=media_name
            # media.media_nbr=int(files_nbr)
            # media.uploaded=False

            # print "media name: " + media.name
            # media.put()

            self.response.headers["Content-Type"] = "application/json"


            res = {
                'code': 200,
                'response' :upload_url
                 }

            self.response.write(json.dumps(res))