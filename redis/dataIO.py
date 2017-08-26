import redis

POOL = redis.ConnectionPool(host='localhost', port=6379, db=0)

def byteToUTF(dictionary):
    return {k.decode('utf-8'): v.decode('utf-8') \
                for k, v in dictionary.items()}

def getCountryStats(countryName):
    redis_db = redis.Redis(connection_pool=POOL)

    # Get current data
    countryData = redis_db.hgetall(countryName)

    if countryData == {}:
        raise KeyError('Country named \'' + countryName + \
        '\' does not exist')
    else:
        # Convert from byte literal to unicode
        response = byteToUTF(countryData)
        return response

def getCountrySentiment(countryName):
    country = getCountryStats(countryName)
    avgSentiment = float(country['sentiment']) / int(country['count'])
    return avgSentiment

    
def setCountryStats(countryName, sentiment):
    redis_db = redis.Redis(connection_pool=POOL)

    # Get current data
    countryData = redis_db.hgetall(countryName)

    if countryData == {}:
        newCountryData = {}
        newCountryData['sentiment'] = sentiment
        newCountryData['count'] = 1
    else:
        # Convert from byte literal to unicode
        newCountryData = byteToUTF(countryData)

        # Increment the tweet count
        newCountryData['count'] = int(newCountryData['count']) + 1

        # Average the sentiment
        newCountryData['sentiment'] = \
        (float(newCountryData['sentiment']) \
         + sentiment)
        
    # Set the new value
    redis_db.hmset(countryName, newCountryData);

# setCountryStats("United States", -0.6)
# print(getCountryStats("United States"))
# print(getCountrySentiment("United States"))
