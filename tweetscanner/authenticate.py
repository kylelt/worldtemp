# Import essential tweepy libraries
from tweepy import OAuthHandler
from tweepy import API

# Import credentials
from credentials import *

def get_authenticated_api():
	"""Returns a authenticated twitter API. 

    """
	auth = OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)

	# Construct the API instance
	api = API(auth)

	return api