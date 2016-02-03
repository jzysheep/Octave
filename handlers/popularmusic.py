from domain import *
from time import strftime
from google.appengine.api import users
import webapp2
import heapq

class PopularMusic(webapp2.RequestHandler):
    def get(self):
        logged_user = users.get_current_user()
        if not logged_user:
            self.redirect(users.create_login_url(self.request.uri))
        else:
            logged_user_query = User.gql("WHERE email =:1 ", logged_user.email())
            logged_user_fetch = logged_user_query.get()
            url = users.create_logout_url('/')
            url_linktext = 'Logout'
            unordered_posts = Post.query().fetch()
            post_user_reply = []
            ######################ADD THIS#########

            links=[]
            media_types=[]
            ######################End ADD#########

            if unordered_posts:
                unordered_posts.sort(key=lambda x: x.likes, reverse=True)
                for post in unordered_posts:
                    if post.key in logged_user_fetch.shared_posts:
                        posts_share = "Shared"
                    else:
                        posts_share = "Share"
                    post_user = post.user_key.get()
                    post_replies = Reply.query(Reply.post_key == post.key).order(Reply.date).fetch()
                    user_reply = []
                    for reply in post_replies:
                        user_reply.append(reply.user_key.get())
                    post_user_reply.append((post, post_user, post_replies, user_reply, posts_share))

######################End ADD#########

                    media_query = Media.gql("WHERE key_media = :1", post.blob_key_media)
                    if post.link!=None:
                        links.append(post.link)
                        print "LINKS SAVED: "
                        print post.link

                    entity=media_query.get()
                    if entity!=None:
                        media_types.append(entity.media_type)
######################End ADD#########

                # You might like section:
                all_users = User.query().fetch()
                 # choose top k uses which has the most shared posts
                top_k_users = heapq.nlargest(8, all_users, key=lambda x: x.num_shared_posts)

                values = {
                    'url_log': url_linktext,
                    'url': url,
                    'post_user_reply': post_user_reply,
                    'logged_user': logged_user_fetch,
                    'top_k_users': top_k_users,
                    'media_types': media_types,
                    'links':links

                }

                template = JINJA_ENVIRONMENT.get_template('popularmusic.html')
                self.response.write(template.render(values))

            else:
                self.redirect('/MyMusic')
