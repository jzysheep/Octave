from domain import *
import webapp2
from google.appengine.api import users
from google.appengine.ext.webapp import blobstore_handlers
import time
from google.appengine.ext import blobstore
import json
from google.appengine.ext.blobstore import BlobKey
            
class Manage(webapp2.RequestHandler):
    def get(self):
        user=users.get_current_user()
        if user:

            url = users.create_logout_url('/')
            url_linktext = 'Logout'

            user_query = User.gql("WHERE email =:1", user.email())
            user_fetch = user_query.get()

            playlist_name=self.request.get('playlist')
            playlist_key=self.request.get('key')


            playlist_query=Playlist.gql("WHERE name=:1",playlist_name)


            playlist_chosen = playlist_query.fetch()

            print "PLAYLIST KEY: " + playlist_key
            print "PLAYLIST KEY: " + str(playlist_chosen[0].user_key)

            for play in playlist_chosen:
                if str(play.user_key)==playlist_key:
                    playlist = play
                    break


            media_query = Media.gql("WHERE upload_check = :1", True)
            media_fetch = media_query.fetch()


            for media in media_fetch:
                if media!=None:
                    media.upload_check=False;
                    playlist.key_media.append(media.key_media)
                    playlist.media_name.append(media.name)
                    media.put()

            if user_fetch.key==playlist.user_key:
                is_self = True
                self_delete = "true"
            else:
                is_self = False
                self_delete="false"
            playlist.put()


            links_audio=[]
            links_video=[]
            name_audio=[]
            name_video=[]
            links=[]
            names=[]
            keys=[]

            for key in playlist.key_media:
                media_query = Media.gql("WHERE key_media = :1", key)
                media = media_query.get()
                keys.append(str(key))
                print media
                if media:
                    links.append(str(key))
                    names.append(media.name)
                    if media.media_type=='audio':
                        links_audio.append(str(key))
                        name_audio.append(media.name)

                    else:
                        links_video.append(str(key))
                        name_video.append(media.name)

            # for link in playlist.links:
            #     links_video.append(link)



            for link in links_audio:
                link.decode("utf8")

            for link in links_video:
                link.decode("utf8")

            for name in name_audio:
                name.decode("utf8")

            for name in name_video:
                name.decode("utf8")

            for name in names:
                name.decode("utf8")

            for link in links:
                link.decode("utf8")



            values={
               'url_log':url_linktext,
               'url':url,
               'links_audio':json.dumps(links_audio),
               'links_video':json.dumps(links_video),
               'playlist_name':playlist.name,
               'playlist_key':playlist.user_key,
               'playlist_cover':playlist.cover_url,
               'name_audio':json.dumps(name_audio),
               'name_video':json.dumps(name_video),
               'size_audio':links_audio.__len__(),
               'size_video':links_video.__len__(),
               'is_self':is_self,
                'names':json.dumps(names),
                'links':json.dumps(links),
                'size':links.__len__(),
                'playlist_key':playlist_key,
                'keys':keys,
                'self_delete':self_delete
                }



            template = JINJA_ENVIRONMENT.get_template('jplayer.html')
            self.response.write(template.render(values))


    def post(self):
        # key_media = ndb.Key(urlsafe=self.request.get("key_media"))
        key_media=self.request.get("key_media")

        blobkey = BlobKey (key_media)

        media_query = Media.gql("WHERE key_media = :1", blobkey)
        media = media_query.get()
        blobstore.delete(key_media)

        media.key.delete()









