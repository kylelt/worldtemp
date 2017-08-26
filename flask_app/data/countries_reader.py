from csv import DictReader
from csv import DictWriter

#
# Converts our TSV of countries, cities and degrees minute seconds lat, lon to 
# a CSV with decimal rather than dms notation
#
#

degrees = lambda x: float(x[0: x.index("°")])
minutes = lambda x: float(x[x.index("°")+1: x.index("'")])
mult = lambda x: -1 if x[-1] in ['S', 'W'] else 1

with open('./countries.csv', 'r') as rh, open('countries_decimal_degrees.csv', 'w') as wh:
    dr = DictReader(rh, delimiter='\t')
    wh = DictWriter(wh, ["Country", "Capital", "Latitude", "Longitude"]) 
    wh.writeheader()
    for i in dr:
        lat_dms = i['Latitude']
        lon_dms = i['Longitude']
        lat_d = (degrees(lat_dms) + minutes(lat_dms)/60) * mult(lat_dms)
        lon_d = (degrees(lon_dms) + minutes(lon_dms)/60) * mult(lon_dms)
        print(("ldms: {0}, ldeg: {1}, lodms: {2}, lodeg: {3} ".format(lat_dms, lat_d, lon_dms, lon_d)))
        
        j=i
        j['Latitude'] = lat_d
        j['Longitude'] = lon_d

        wh.writerow(j)
