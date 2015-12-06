import time
from mainpage import *
import datetime
from google.appengine.ext.db import GqlQuery
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers

# A custom datastore model for associating users with uploaded files.


class Media_Show(webapp2.RequestHandler):
    def get(self):
        user=users.get_current_user()
        if user:
            url = users.create_logout_url('/')
            url_linktext = 'Logout'
            global stream_id
            stream_id=self.request.get('stream_id')
            #stream_key_id= ndb.Key('Stream',stream_id,parent=stream_key(users.get_current_user().nickname()))
            stream_query = Stream.gql("WHERE name = :1", stream_id) # note that stream name is unique, I used this because when clicking from view on the stream the current user is not the parent of that stream


            stream = stream_query.get()  #constructing the entity
            stream_sub_query = Stream_sub.gql("WHERE name = :1 AND email=:2", stream_id,user.email())
            stream_sub=stream_sub_query.get()
            if(stream!=None):
                if(stream.email!=user.email()):
                    stream.views=stream.views+1
                    stream.put()

                if(stream_sub!=None):
                    stream_sub.views=stream_sub.views+1
                    stream_sub.put()

            Photo_query=UserPhoto.gql("WHERE stream_name = :1", stream_id)
            Photo=Photo_query.order(UserPhoto.date).fetch()
            links=[]
            if(Photo):
                num=0
                for photo in Photo:
                    links.insert(num,photo.blob_key)
                    num=num+1                    
                
                if(stream.img_nbr<num):
                    stream.date_image.insert(0,datetime.date.today())

                stream.img_nbr=num

                if stream.img_nbr>=3:
                    img_id=range(num-1,num-4,-1)

                else:
                    img_id=range(num-1,-1,-1)

                
                stream.put()
            else:
                img_id=[]

            values={
               'url_log':url_linktext,
               'url':url,
               'stream':stream,
               'stream_name': stream_id, 
               'img_id':img_id,
               'email': user.email(),
               'links':links
               } 
            template = JINJA_ENVIRONMENT.get_template('stream.html')
            self.response.write(template.render(values))

    def post(self):
        user=users.get_current_user()
        if user:
            url = users.create_logout_url('/')
            url_linktext = 'Logout'
            global stream_id
            stream_id=self.request.get('stream_id')
            #stream_key_id= ndb.Key('Stream',stream_id,parent=stream_key(users.get_current_user().nickname()))
            stream_query = Stream.gql("WHERE name = :1", stream_id) # note that stream name is unique, I used this because when clicking from view on the stream the current user is not the parent of that stream


            stream = stream_query.get()  #constructing the entity
            stream_sub_query = Stream_sub.gql("WHERE name = :1 AND email=:2", stream_id,user.email())
            stream_sub=stream_sub_query.get()
            if(stream!=None):
                if(stream.email!=user.email()):
                    stream.views=stream.views+1
                    stream.put()

                if(stream_sub!=None):
                    stream_sub.views=stream_sub.views+1
                    stream_sub.put()

            Photo_query=UserPhoto.gql("WHERE stream_name = :1", stream_id)
            Photo=Photo_query.order(UserPhoto.date).fetch()
            links=[]
            if(Photo):
                num=0
                for photo in Photo:
                    links.insert(num,photo.blob_key)
                    num=num+1

                if(stream.img_nbr<num):
                    stream.date_image.insert(0,datetime.date.today())

                stream.img_nbr=num

                img_id=range(num-1,-1,-1)

                stream.put()
            else:
                img_id=[]

            values={
               'url_log':url_linktext,
               'url':url,
               'stream':stream,
               'stream_name': stream_id,
               'img_id':img_id,
               'email': user.email(),
               'links':links
               }
            template = JINJA_ENVIRONMENT.get_template('stream.html')
            self.response.write(template.render(values))





