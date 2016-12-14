
import tweepy

class TwitterAPI(object):

    consumer_key = ''
    consumer_secret = ''

    key = ''
    secret = ''

    # per tweepy, Twitter never expires the keys above, but if we need to regenerate
    # them, read http://tweepy.readthedocs.io/en/v3.5.0/auth_tutorial.html#oauth-authentication
    
    def __init__(self):
        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.key, self.secret)
        self.api = tweepy.API(auth)

    def followers(self, twitter_handle):
        user = self.api.get_user(twitter_handle)
        return user.followers_count
    
