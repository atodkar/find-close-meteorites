import requests
import geopy
import os, math

from geopy.geocoders import Nominatim

# Set proxy

# my current location
my_loc = (40.3666, -74.6408)
# get meteor data

def get_meteor_data():
    meteor_resp = requests.get("https://data.nasa.gov/resource/y77d-th95.json")
    return meteor_resp.json()

def get_geo_location(lat, long):
    geolocator = Nominatim(user_agent="Chrone App", timeout=5)
    location = geolocator.reverse(str(lat) + ", " + str(long))
    if location.address is None:
        return ""
    else:
        return location.address

def calc_dist(lat1, lon1, lat2, lon2):
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    h = math.sin( (lat2 - lat1) / 2 ) ** 2 + \
      math.cos(lat1) * \
      math.cos(lat2) * \
      math.sin( (lon2 - lon1) / 2 ) ** 2

    return 6372.8 * 2 * math.asin(math.sqrt(h))

def get_dist(meteor):
    return meteor.get("distance", math.inf)

if __name__ == "__main__":

    # os.environ["HTTP_PROXY"] = "http://194.138.0.9:9400"
    # os.environ["HTTPS_PROXY"] = "http://194.138.0.9:9400"

    meteor_data = get_meteor_data()

    for meteor in meteor_data:
        #print(meteor)
        if "reclat" in meteor and "reclong" in meteor and "India" in get_geo_location(meteor['reclat'], meteor['reclong']):
            meteor["distance"] = calc_dist(float(meteor.get('reclat', 0)),\
            float(meteor.get('reclong', 0)), my_loc[0], my_loc[1])

    meteor_sorted = [m for m in meteor_data if "distance" in m]
    meteor_sorted.sort(key = get_dist)

    print("Nearest location: {0}".format(get_geo_location(meteor_sorted[0]["reclat"], \
    meteor_sorted[0]["reclong"])))
    
    print("Farthest location: {0}".format(get_geo_location(meteor_sorted[len(meteor_sorted) -1]["reclat"], \
    meteor_sorted[len(meteor_sorted) -1]["reclong"])))
    