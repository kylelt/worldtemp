# Import essential library
from tweepy import StreamListener
from preprocessing import processTweetText
from coordinator import TweetCoordinator
import json


# Stream listener for receiving data
class WorldTempStreamListener(StreamListener):
    """ A listener handles tweets that are received from the stream.
"""
    def init_controller(self, controller):
        if controller is None:
            self.controller = TweetCoordinator()
        else:
            self.controller = controller

    def __init__(self, controller=None):
        self.controller = WorldTempStreamListener.get_controller
            
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
        if self.controller.working:
            self.controller.start_work()

