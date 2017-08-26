# Import essential library
from tweepy import StreamListener
from preprocessing import processTweetText
import json


# Stream listener for receiving data
class WorldTempStreamListener(StreamListener):
	""" A listener handles tweets that are received from the stream.

    """

	def on_status(self, status):
		print(status.text)

	def on_error(self, status_code):
		if status_code == 420:
			# returning false in on_data disconnects the stream
			return False

	def on_data(self, data):
		""" Decodes the received data and prints it out in a desired format

    	"""

        # Twitter returns tweets in JSON format
		decodedData = json.loads(data)
		
		try:
			if decodedData['text']:
				retweeted = decodedData['retweeted']
				
				# Tweets without location are ignored as we cannot track the user to a specific geo location
				if (decodedData['user'] != None and retweeted == False and decodedData['user']['location'] != None):
					userLocation = decodedData['user']['location']
					postPlace = decodedData['place']['country']

					# Convert UTF-8 to ASCII to ignore the bad characters sent by users
					tweet_text = decodedData['text'].encode('ascii', 'ignore').decode('utf-8')

					print('Processed: %s\nActual: %s\nLocation: %s\nTweet location: %s\n' % (processTweetText(tweet_text), tweet_text, userLocation, postPlace))

		except KeyError:
			pass
		

		return True