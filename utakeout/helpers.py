from __future__ import print_function
import requests
import json
import psycopg2
from time import sleep
from math import sin, cos, sqrt, atan2, radians, log1p
from pprint import pprint
import yelpapi

GOOGLE_API_KEY = 'AIzaSyDt69MaVC9IlGIfht0L4Ho8vdLsvDlwsh8'
YELP_CONSUMER_KEY = 'pXB7Yb4GG5XmWT48uU9y4A'
YELP_CONSUMER_SECRET = '5vKOEu3dSsSialqsHk4r8xLDfnE'
YELP_TOKEN = 'nmvFHGmyK4z_z6hTYzjnohEVHENsnJpw'
YELP_TOKEN_SECRET = 'FqMg_7EDcM2CJqEyxUHW3mZC7MU'
GOOGLE_GEOCODE_API = 'https://maps.googleapis.com/maps/api/geocode/json?address='
GOOGLE_DISTANCE_API = 'https://maps.googleapis.com/maps/api/distancematrix/json?origins={}&destinations={}&mode={}&key={}'
DBNAME = 'd957m8v93iupnq'
DBUSER ='qkzwpeovygmsup' 
DBHOST='ec2-54-225-197-143.compute-1.amazonaws.com' 
DBPW ='50qIXvnDz100e54cqAoV6lpEpg'
R = 6373.0 # approximate radius of earth in km
 
def get_geolocate_link(input_address):
    new_address = input_address.replace(' ','+')
    link = '{}{}&key={}'.format(GOOGLE_GEOCODE_API,new_address,GOOGLE_API_KEY)
    return link


def get_address_info(address):
    address_request = requests.get(get_geolocate_link(address))
    if address_request.status_code != 200:
        print ('GeoCode Response Error. Expected 200, got {}'.format(address_request.status_code))
        return None
    
    address_json = json.loads(address_request.text)
    if address_json['status'] != 'OK':
        print ('Geocode Error. {}'.format(address_json['status']))
        return None

    address_dict = {'street_number' : None,
                    'route' : None,
                    'locality': None,
                    'administrative_area_level_2': None,
                    'administrative_area_level_1': None,
                    'postal_code': None
                    }
    for key in address_dict.keys():
        for dict in address_json['results'][0]['address_components']:
            if key in dict['types']:
                address_dict[key] = dict['short_name']
    address_dict['state'] = address_dict['administrative_area_level_1']
    address_dict['county'] = address_dict['administrative_area_level_2']
    address_dict['lat'] = address_json['results'][0]['geometry']['location']['lat']
    address_dict['lng'] = address_json['results'][0]['geometry']['location']['lng']
    
    return address_dict
    
    
def get_yelp_results(lat, lon):
    yelp_api = yelpapi.YelpAPI(YELP_CONSUMER_KEY, YELP_CONSUMER_SECRET, YELP_TOKEN, YELP_TOKEN_SECRET)
    results_json1 = yelp_api.search_query(sort=1, term='takeout', ll='{},{}'.format(lat,lon))
    results_json2 = yelp_api.search_query(sort=1, offset=20, limit=20, term='takeout', ll='{},{}'.format(lat,lon))
    results_json = results_json1['businesses'] + results_json2['businesses']

    ratings_dict = {}
    #pprint(results_json)
    for business in results_json:
        if business['is_closed'] == True:
            continue
        name = business['name']
        review_count = business['review_count']
        rating = business['rating']
        lat = business['location']['coordinate']['latitude']
        lon = business['location']['coordinate']['longitude']
        distance = business['distance']
        deals = business.get('deals',None)
        ratings_dict[name] = {'name':name, 'review_count':review_count, 'rating':rating, 'lat':lat, 'lon':lon, 'deals':deals, 'distance':distance}
    #pprint(ratings_dict)
    return ratings_dict, results_json
        

def get_distances_link(lat, lon, ratings_dict):
    home = '{},{}'.format(lat,lon)
    search_string= '|'.join(['{},{}'.format(business['lat'], business['lon']) for business in ratings_dict.values()])
    walk_link = GOOGLE_DISTANCE_API.format(home,search_string,'walking',GOOGLE_API_KEY)
    bad_drive_link = GOOGLE_DISTANCE_API.format(home,search_string,'driving',GOOGLE_API_KEY) + '&departure_time={}&traffic_model=pessimistic'.format(get_next_weekday_6pm())
    good_drive_link = GOOGLE_DISTANCE_API.format(home,search_string,'driving',GOOGLE_API_KEY)
    return walk_link, bad_drive_link, good_drive_link


def get_next_weekday_6pm():
    #IMPLEMENT THIS
    return 'now'


def get_business_distances(link):
    distance_matrix_request = requests.get(link)
    if distance_matrix_request.status_code != 200:
        print('Status Code Error. Expected 200, got {}'\
                .format(distance_matrix_request.status_code))
        return None

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
        
    sleep(.5)
    
    if all(distance == None for distance in pessimistic_distances):
        return distances
    else:
        return pessimistic_distances


def measure_distances(latitude1, lng1, latitude2, lng2):
    lat1 = radians(latitude1)
    lon1 = radians(lng1)
    lat2 = radians(latitude2)
    lon2 = radians(lng2)
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c
    return distance


def get_closest_police(state, lat, lng):
    #IMPLEMENT DATABASE AND SET EVERYTHING
    try:
        conn = psycopg2.connect("dbname='{}' user='{}' host='{}' password='{}'"\
                                          .format(DBNAME, DBUSER, DBHOST, DBPW))
    except:
        print("Database Connection Error")
        return None

    cursor = conn.cursor()
    STATEMENT = 'SELECT * FROM crime_data WHERE STATE = %s'
    data = state
    cursor.execute(STATEMENT, [data])
    agencies = cursor.fetchall()
    cursor.close()
    conn.close()
    closest_dist = None
    closest_agency = None
    for agency in agencies:
        distance = measure_distances(float(lat), float(lng), agency[28], agency[29])
        if closest_dist is None or distance < closest_dist:
            closest_dist = distance
            closest_agency = agency
    return closest_dist, closest_agency


def get_lum(zipcode):
    try:
        conn = psycopg2.connect("dbname='{}' user='{}' host='{}' password='{}'"\
                                          .format(DBNAME, DBUSER, DBHOST, DBPW))
    except:
        print("Database Connection Error")
        return None
    
    cursor = conn.cursor()
    statement = 'SELECT * FROM lumbyzcta WHERE zip = %s'
    data = [zipcode]
    cursor.execute(statement, data)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data[-1]

    
def analysis(address):
    address_dict = get_address_info(address)
    yelp_dict, yelp_results = get_yelp_results(address_dict['lat'],address_dict['lng'])
    walk_link, bad_drive_link, good_drive_link = get_distances_link(address_dict['lat'], 
                                                                    address_dict['lng'],
                                                                    yelp_dict)
    walk_distance = get_business_distances(walk_link)
    good_drive_dist = get_business_distances(good_drive_link)
    bad_drive_dist = get_business_distances(bad_drive_link)
    closest_pol_dist, closest_pol = get_closest_police(str(address_dict['state']), 
                                                        address_dict['lat'], 
                                                        address_dict['lng'])
    pol_name = closest_pol[1]
    
    lum = get_lum(address_dict['postal_code'])

    #Get avg yelp review
    ratings = []
    for business_dict in yelp_dict.values():
        ratings.append((business_dict['rating'],business_dict['review_count'], 
                                                business_dict['distance']))
    total_rev = 0.0
    for bus in ratings:
        total_rev += bus[1]
    weighted_score = 0
    for bus in ratings:
        dist_weight = 1.0/log1p(bus[2])
        rev_weight = bus[1]/total_rev
        weighted_score += dist_weight * rev_weight * bus[0]
    
    avg_walk = sum(walk_distance)/len(walk_distance)
    avg_good_dr = sum(good_drive_dist)/len(good_drive_dist)
    avg_bad_dr = sum(bad_drive_dist)/len(bad_drive_dist)
    
    final_result = {
                    'Average_review':weighted_score,
                    'total_reviews':total_rev,
                    'lum':lum,
                    'police_name':pol_name,
                    'pol_distance':closest_pol_dist,
                    'pol_row':closest_pol,
                    'avg_walk':avg_walk,
                    'avg_good_dr':avg_good_dr,
                    'avg_bad_dr':avg_bad_dr,
                    'yelp_results':yelp_results
                    }
    return final_result

    
# pprint(analysis('2042 barberrie ln, decatur, ga 30032')) 