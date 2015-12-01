from domain import *
from google.appengine.api import users
import webapp2

class Music(webapp2.RequestHandler):
    def get(self):
        user=users.get_current_user()
        if user:
            url = users.create_logout_url('/')
            url_linktext = 'Logout'
            

            # streams = Stream.query(
            # ancestor=stream_key(users.get_current_user().email())).order(-Stream.date).fetch(2)
            #
            # streams_sub = Stream_sub.query(
            # ancestor=stream_sub_key(users.get_current_user().email())).order(-Stream_sub.date).fetch(2)
            #
            # streams_from_sub=[]
            # count=0
            # for stream_sub in streams_sub:
            #     stream_query = Stream.gql("WHERE name = :1", stream_sub.name)
            #     stream = stream_query.get()  #constructing the entity
            #     streams_from_sub.insert(count,stream)
            #     count=count+1

            values={
               'url_log':url_linktext,
               'url':url
               #'streams':streams,
               #'streams_sub':streams_sub,
               #'streams_from_sub':streams_from_sub,
                }

            template = JINJA_ENVIRONMENT.get_template('music.html')
            self.response.write(template.render(values))

    def post(self):
    #     streams = Stream.query(
    #         ancestor=stream_key(users.get_current_user().email())).order(-Stream.date).fetch(2)
    #
    #     streams_sub = Stream_sub.query(
    #         ancestor=stream_sub_key(users.get_current_user().email())).order(-Stream_sub.date).fetch(2)
    #
    #
    #     if(self.request.get('delete1')):
    #             streams[0].key.delete()
    #             name1=self.request.get('delete1')
    #             stream_query0 = Stream_sub.gql("WHERE name = :1",name1) # note that stream name is unique
    #             if(stream_query0.get()!=None):
    #                 for stream in stream_query0:
    #                     stream.key.delete()
    #             #stream0_get=stream_query0.get()
    #             #if(stream0_get!=None):
    #             #    stream0_get.key.delete()
    #
    #     if(self.request.get('delete2')):
    #             name2=self.request.get('delete2')
    #             streams[1].key.delete()
    #             stream_query1 = Stream_sub.gql("WHERE name = :1",name2)
    #             if(stream_query1.get()!=None):
    #                 for stream in stream_query1:
    #                     stream.key.delete()
    #             #stream1_get=stream_query1.get()
    #             #if(stream1_get!=None):
    #             #    stream1_get.key.delete()
    #
    #
    #     if(self.request.get('unsub1')):
    #         name1=self.request.get('unsub1')
    #         stream_query1 = Stream.gql("WHERE name = :1",name1)
    #         stream1_get=stream_query1.get()
    #         if(stream1_get!=None):
    #             stream1_get.views=stream1_get.views-streams_sub[0].views
    #             streams_sub[0].key.delete()
    #             stream1_get.put()
    #
    #
    #     if(self.request.get('unsub2')):
    #         name2=self.request.get('unsub2')
    #         stream_query2 = Stream.gql("WHERE name = :1",name2)
    #         stream2_get=stream_query2.get()
    #         if(stream2_get!=None):
    #             stream2_get.views=stream2_get.views-streams_sub[1].views
    #             streams_sub[1].key.delete()
    #             stream2_get.put()
    #
    #
    #
        self.redirect('/MyMusic')
