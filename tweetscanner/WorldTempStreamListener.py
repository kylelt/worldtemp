# Import essential library
from tweepy import StreamListener
from coordinator import TweetCoordinator
import json


# Stream listener for receiving data
class WorldTempStreamListener(StreamListener):
    """ A listener handles tweets that are received from the stream.
"""

    def __init__(self, controller=None):
        self.controller = TweetCoordinator()

    def on_status(self, status):
        print(status.text)

    def on_error(self, status_code):
        if status_code == 420:
        # returning false in on_data disconnects the stream
            if(self.controller.working):
                self.controller.stop_work()
            return False

    def on_data(self, data):
        """ 
        Decodes the received data and prints it out in a desired format
        """
        self.controller.put_tweet(data)
        if not self.controller.working:
            self.controller.start_work()

