from domain import *
import webapp2
from google.appengine.api import users
from time import strftime
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext import blobstore
import re
import time
class MyPlaylist(webapp2.RequestHandler):
    def get(self):
        user=users.get_current_user()
        if user:

            url = users.create_logout_url('/')
            url_linktext = 'Logout'


            user_query = User.gql("WHERE email =:1", user.email())
            user_fetch = user_query.get()
            playlist=Playlist.query(ancestor=user_fetch.key).order(-Playlist.date).fetch()
            links=[]
            playlist_keys=[]



            for play in playlist:
                playlist_keys.append(str(play.user_key))
                if play.key_media:
                    links.append(play.key_media[0])
                else:
                    links.append("")

            links_front=[]
            for i in range(0,links.__len__()):
                if links[i]!="":
                    links_front.insert(i,'/view_media/' + str(links[i]))
                else:
                    links_front.insert(i,"")


            values={
               'url_log':url_linktext,
               'url':url,
               'playlist':playlist,
               'user_email':user.email(),
               'links':links_front,
                'is_self': True,
                'button_manage': "manage",
                'email':user.email()
                }

            template = JINJA_ENVIRONMENT.get_template('playlist.html')
            self.response.write(template.render(values))


class ViewPlaylist(webapp2.RequestHandler):
    def get(self):
        logged_user = users.get_current_user()
        if not logged_user:
            self.redirect(users.create_login_url(self.request.uri))
        else:
            url = users.create_logout_url('/')
            url_linktext = 'Logout'
            search_str = self.request.get("search_str").strip()
            searched_user_query = User.query(User.name == search_str)
            searched_user = searched_user_query.get()
            playlist=Playlist.query(ancestor=searched_user.key).order(-Playlist.date).fetch()
            links=[]

            for play in playlist:
                if play.key_media:
                    links.append(play.key_media[0])
                else:
                    links.append("")

            links_front=[]
            for i in range(0,links.__len__()):
                if links[i]!="":
                    links_front.insert(i,'/view_media/' + str(links[i]))
                else:
                    links_front.insert(i,"")

            values={
               'url_log':url_linktext,
               'url':url,
               'playlist':playlist,
               'user_email':searched_user.email,
               'links':links_front,
                'is_self': False,
                'button_manage': "View"

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

        music_links=[]
        music_links = self.request.get_all('music_links',"")


        user = users.get_current_user()
        user_query = User.gql("WHERE email =:1", user.email())
        user_fetch = user_query.get()


        playlist=Playlist(parent=user_fetch.key)


        media_query = Media.gql("WHERE upload_check = :1", True)


        media_fetch = media_query.fetch()


        for media in media_fetch:
            if media!=None:
                print "media names inside playlist: " +  media.name
                media.upload_check=False;
                playlist.key_media.append(media.key_media)
                playlist.media_name.append(media.name)
                media.put()

        if music_links.__len__()!=0:
            playlist.links = music_links

        playlist.populate(
            name=name,
            user_key=user_fetch.key,
            privacy=privacy,
            date_created=date_created,
            cover_url=cover_url,
        )

        playlist.put()
        self.redirect('/playlist')

class PlaylistUploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        s_time = strftime("%Y/%m/%d")
        now_string = s_time.replace('/','-')
        media_name=self.request.get('media_name')
        upload = self.get_uploads()[0]
        # media = Media.query(ancestor=user_fetch.key).order(-Media.date).get()
        #
        # media_all = Media.query(ancestor=user_fetch.key).order(-Media.date).fetch(media.media_nbr)
        #
        # for iterator in range(0,media.media_nbr):
        #     print "ENTERING "
        #     if media_all[iterator].uploaded==True:
        #         continue
        #     else:

        blob_info = blobstore.BlobInfo.get(upload.key())
        filename=blob_info.filename
        if '.mp3' in filename:
            type='audio'
        else:
            type='video'

        media=Media(name=filename,key_media=upload.key(),upload_check=True,date_created=now_string,media_type=type)
        media.put()


