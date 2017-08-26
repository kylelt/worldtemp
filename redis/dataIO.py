import redis

POOL = redis.ConnectionPool(host='localhost', port=6379, db=0)

def getCountryStats(countryName):
    redis_db = redis.Redis(connection_pool=POOL)

    # Get current data
    countryData = redis_db.hgetall(countryName)

    if countryData == {}:
        raise KeyError('Country named \'' + countryName + '\' does not exist')
    else:
        # Convert from byte literal to unicode
        response = {k.decode('utf-8'): v.decode('utf-8') \
                for k, v in countryData.items()}
        return response;
    

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
        newCountryData = {k.decode('utf-8'): v.decode('utf-8') \
                for k, v in countryData.items()}

        # Increment the tweet count
        newCountryData['count'] = int(newCountryData['count']) + 1

        # Average the sentiment
        newCountryData['sentiment'] = (float(newCountryData['sentiment']) \
         + sentiment) / 2
        
    # Set the new value
    redis_db.hmset(countryName, newCountryData);

# setCountryStats("United States", -0.6)
print(getCountryStats("Unisted States"))