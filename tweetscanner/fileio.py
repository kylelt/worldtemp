import csv

def writeCSVFile(data):
	with open('tweets/data.csv', 'a') as csvfile:
		tweet_writer = csv.writer(csvfile)
		tweet_writer.writerow(data)
	