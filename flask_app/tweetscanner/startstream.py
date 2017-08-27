# Import helper class
from WorldTempStreamListener import WorldTempStreamListener
from tweepy import Stream
from authenticate import get_authenticated_api

api = get_authenticated_api()
worldTempStream = Stream(api.auth, WorldTempStreamListener())

# Tracks the tweets from all over the world
worldTempStream.filter(locations=[-180,-90,180,90], languages = ['en'])

