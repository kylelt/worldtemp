import re
from fileio import writeCSVFile
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# File contains helper functions for the processing of tweet text

analyzer = SentimentIntensityAnalyzer()

def processTweetText(tweet_text):
	""" Processes the tweet text

	"""
	# Removes reply, email, hashtags and newline segments
	filtered = removeNoise(tweet_text)

	# Correct Spacing
	correctedSpacing = correctSpacing(filtered)

	# Convert all letters to lower case
	lowerCase = correctedSpacing.lower()

	# Write to file for data collection to a csv
	# writeCSVFile(textToTokens(processed))

	# Sentiment Analysis
	vs = analyzer.polarity_scores(lowerCase)['compound']

	if vs > 0:
		sentiment = "Positive"
	elif vs < 0:
		sentiment = "Negative"
	else:
		sentiment = "Neutral"

	filteredSentenceWithSentiment = lowerCase + ' ' + str(sentiment)

	return filteredSentenceWithSentiment


def removeNoise(tweet_text):
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


def correctSpacing(tweet_text):
	""" Removes multiple spaces and replaces it with a single space

	"""
	words = [word.strip() for word in tweet_text.split()]
	return ' '.join(words)

def textToTokens(tweet_text):
	""" Converts a tweet to a list of words seperated by a single space

	"""
	tokens = [token.strip() for token in tweet_text.split()]
	return tokens