from google.appengine.ext import ndb

class Media(ndb.Model):
    views = ndb.IntegerProperty()
    link = ndb.StringProperty()
    blob_key_media = ndb.BlobKeyProperty()
    media_type = ndb.StringProperty()                      

class Tag(ndb.Model):
    name = ndb.StringProperty()
    media_names = ndb.StringProperty(repeated=True) #construct entities later from the name string

class User(ndb.Model):
    email = ndb.StringProperty()
    city = ndb.StringProperty()
    name = ndb.StringProperty()
    role = ndb.StringProperty()
    blob_key_photo=ndb.BlobKeyProperty()
    followers = ndb.StringProperty(repeated=True) #Their emails

class Post(ndb.Model):
    date = ndb.DateTimeProperty(auto_now_add=True)
    date_created = ndb.StringProperty()
    text = ndb.StringProperty()
    tags = ndb.StringProperty(repeated=True) # construct entities from the strings
    media_names = ndb.StringProperty(repeated=True) #construct entities by fetching the media based on the list of names
    user_key = ndb.KeyProperty(kind=User)

class Reply(ndb.Model):
    date = ndb.DateTimeProperty(auto_now_add=True)
    user_key = ndb.KeyProperty(kind=User)
    reply = ndb.TextProperty()
    date_reply = ndb.StringProperty()
    post_key = ndb.KeyProperty(kind=Post)

class Playlist(ndb.Model):
    name = ndb.StringProperty()
    user_key = ndb.KeyProperty()
    media = ndb.StructuredProperty(Media, repeated=True)
    privacy = ndb.StringProperty()

class Artist(ndb.Model):
    user = ndb.StructuredProperty(User,repeated=False)
    cities_ad = ndb.StringProperty(repeated=True)
    users_to_share = ndb.IntegerProperty()