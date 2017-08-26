from csv import DictReader
import json
class CountryMapper():

    def __init__(self):
        self.csv_data = self.get_dict_list()
    
    def get_dict_list(self):
        with open('./data/countries_decimal_degrees.csv', 'r') as fh:
            return list(DictReader(fh))
    
    def get_latlon(self, cityname):
        """ 
        :return { hasCountry: <t/f>, 
            lat: xxx.yyy, lon xxx.yyy,
            country: country }
        """
        matches = filter(lambda x: x['Capital'] == cityname, self.csv_data)
        matches = list(matches)
        if(len(matches) > 0):
            return json.dumps(
                {
                    "hasCountry": True,
                    "lat": matches[0]['Latitude'], 
                    "lon": matches[0]['Longitude'],
                    "country":matches[0]['Country']
                })
        else:
            return json.dumps({"hasCountry":False})

    
