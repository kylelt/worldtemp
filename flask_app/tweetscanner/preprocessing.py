import re
import queue
from fileio import writeCSVFile
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from multiprocessing import Process, Queue
import asyncio
import time
import sys
from dataIO import *

# File contains helper functions for the processing of tweet text
class TweetProcessor(Process):
    """
    :param in_queue the queue in which the tweets will appear
    :param control_queue the queue in which any sentinal messages will come through
    :param sleep_time how long should i sleep between iterations
    """
    def __init__(self, in_queue: Queue, sleep_time: int, sent):
        super().__init__()
        print("thread init")
        self.in_queue = in_queue
        self.sleep_time = sleep_time
        self.analyzer = SentimentIntensityAnalyzer()
        self.sent = sent
    
    def run(self):
        while self.sent.is_running():
                val = self.in_queue.get(timeout=30)
                self.processTweetText(val)
                time.sleep(self.sleep_time)     

    def processTweetText(self, tweet):

        """ Processes the tweet """
        try:
            # Dump any tweets that don't have the fields we want because we cannot
            # classify those tweets

            if tweet['text']:
                retweeted = tweet['retweeted']
                
                if(tweet['user'] != None and retweeted == False):
                    tweet_location = tweet['place']['country']
                    
                    # Some locations are wierd unicode ... lets drop them
                    tweet_location = tweet_location.encode('ascii', 'ignore').decode('utf-8')
                    if(len(self.removeNoise(tweet_location)) == 0):
                        return

                    tweet_text = tweet['text'].encode('ascii', 'ignore').decode('utf-8')
	                # Removes reply, email, hashtags and newline segments
                    filtered = self.removeNoise(tweet_text) 
                    # Correct Spacing
                    correctedSpacing = self.correctSpacing(filtered)
                    # Convert all letters to lower case
                    lowerCase = correctedSpacing.lower()
	                # Sentiment Analysis
                    vs = self.analyzer.polarity_scores(lowerCase)['compound']
                    self.update_kv_store(tweet_location, vs)
        except (KeyError, TypeError) as e:
            pass
        except:
            raise
            self.join()

    def update_kv_store(self, country, sentiment_value):
        setCountryStats(country, sentiment_value)
    
    def removeNoise(self, tweet_text):
        """ Removes reply, weblinks, hashtags and newline segments
        """
	   # Remove twitter weblinks
        sub_weblinks = re.sub(r'https?:\/\/\S+', '', tweet_text)

	# Replacing '\n' symbols with single spaces
        sub_newline = re.sub(r'\n', ' ', sub_weblinks)

	# Remove 'RT'
        sub_RT = re.sub(r'RT', '', sub_newline)

	# Remove '@someuser'
        sub_replies = re.sub(r'@\w+', '', sub_RT)

	# Remove '#' from hashtags converting it to words
        sub_hashtag = re.sub(r'#', '', sub_replies)

	# Remove alphanumeric characters
        sub_non_an = re.sub(r'[^a-zA-Z0-9]+', ' ', sub_hashtag);

	# Remove excessive whitespace at the start and end
        final_string = sub_non_an.strip()

        return final_string


    def correctSpacing(self, tweet_text):
        """ Removes multiple spaces and replaces it with a single space
        """
        words = [word.strip() for word in tweet_text.split()]
        return ' '.join(words)

    def textToTokens(self, tweet_text):
        """ Converts a tweet to a list of words seperated by a single space
        """
        tokens = [token.strip() for token in tweet_text.split()]
        return tokens

