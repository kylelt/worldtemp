# Import helper class
from WorldTempStreamListener import WorldTempStreamListener
from tweepy import Stream
from authenticate import get_authenticated_api
from coordinator import TweetCoordinator
api = get_authenticated_api()
controller = TweetCoordinator()
controller.start_work()
worldTempStream = Stream(api.auth, WorldTempStreamListener(controller))

# Tracks the tweets from all over the world
worldTempStream.filter(locations=[-180,-90,180,90], languages = ['en'])

