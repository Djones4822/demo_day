import requests
import json

ex_address = '1600 Pennsylvania Ave NW, Washington, DC 20500'

GOOGLE_API_KEY = 'AIzaSyDt69MaVC9IlGIfht0L4Ho8vdLsvDlwsh8'
GOOGLE_GEOCODE_API = 'https://maps.googleapis.com/maps/api/geocode/json?address='
YELP_API = 'https://api.yelp.com/v2/search?term=Takeout&limit=20&offset=20%ll='
YELP_API_KEY = None
#GOOGLE_PLACES_API = None
GOOGLE_DISTANCE_API = 'https://maps.googleapis.com/maps/api/distancematrix/json?origins={}&destinations={}&mode={}&key={}'

# get 
def get_geolocate_link(input_address):
    new_address = input_address.replace(' ','+')
    link = '{}{}&key={}'.format(GOOGLE_GEOCODE_API,new_address,GOOGLE_API_KEY)
    return link


def get_lat_lon(address):
    address_request = requests.get(get_geolocate_link(address))
    if address_request.status_code != 200:
        print ('GeoCode Response Error. Expected 200, got {}'.format(address_request.status_code))
        return None
    
    address_json = json.loads(address_request.text)
    if address_json['status'] != 'OK':
        print ('Geocode Error. {}'.format(address_json['status']))
        return None

    lat_lon_dict = address_json['results'][0]['geometry']['location']
    return lat_lon_dict['lat'], lat_lon_dict['lng']
    
    
def get_yelp_link(lat,lon):
    return '{}{},{}&key={}'.format(YELP_API,lat,lon,YELP_API_KEY)
    

def get_yelp_results(link):
    yelp_results = requests.get(link)
    if yelp_results.status_code != 200:
        print('Status Code Error. Expected 200, got {}'.format(yelp_results.status_code))
        return None
    else:
        print('Yelp Query Successful!')
    
    results_json = json.loads(yelp_results.text)
    return_total = results_json['total']
    ratings_dict = {}
    ratings_dict['TOTAL'] = return_total
    for business in results_json['businesses']:
        if business['is_closed'] == False:
            continue
        name = business['name']
        review_count = business['review_count']
        rating = business['raiting']
        lat = business['location']['coordinate']['latitude']
        lon = business['location']['coordinate']['longitude']
        deals = business.get('deals',None)
        ratings_dict[name] = {'name':name, 'review_count':review_count, 'rating':rating, 'lat':lat, 'lon':lon, 'deals':deals}
        return ratings_dict
        

def get_distances_link(home, ratings_dict):
    search_string= '|'.join(['{},{}'.format(info['latitude'], info['longitude']) for info in ratings_dict.values()])
    walk_link = GOOGLE_DISTANCE_API.format(home,search_string,'walking',GOOGLE_API_KEY)
    drive_link = GOOGLE_DISTANCE_API.format(home,search_string,'driving',GOOGLE_API_KEY) + '&departure_time=&traffic_model=pessimistic'
    return walk_link, drive_link

def get_next_weekday_6pm():
    pass


def get_distances(link):
    distance_matrix_request = requests.get(link)
    if distance_matrix_request.status_code != 200:
        print('Status Code Error. Expected 200, got {}'.format(distance_matrix_request.status_code))
        return None
    else:
        print('Distance Query Successful!')

    distance_matrix = json.loads(distance_matrix_request.text)
    
    if distance_matrix['status'] != 'OK':
        print ('Error. {}'.format(distance_matrix['status']))
        return None

    results = distance_matrix['rows'][0]['elements']
    
    distances = []
    pessimistic_distances = []
    for business in results:
        if business['status'] != 'OK':
            distances.append(None)
            continue
        time = business['duration']['value']
        try:
            traffic_time = business['duration_in_traffic']['value']
        except:
            traffic_time = None
        distances.append(time)
        pessimistic_distances.append(traffic_time)
    
    if all(distance == None for distance in pessimistic_distances):
        return distances,None
    else:
        return distances,pessimistic_distances


        
            

