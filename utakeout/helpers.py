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
    for business in results_json:
        if business['is_closed'] == True:
            continue
        name = business['name']
        url = business['url']
        review_count = business.get('review_count', None)
        rating = business.get('rating', None)
        lat = business['location']['coordinate']['latitude']
        lon = business['location']['coordinate']['longitude']
        distance = business['distance']*0.000621371 # meters to miles conversion
        deals = business.get('deals',None)
        ratings_dict[name] = {'name':name, 'review_count':review_count, 'rating':rating, 'lat':lat, 'lon':lon, 'deals':deals, 'distance':distance}
    #pprint(ratings_dict)
    return ratings_dict, results_json
        

def get_distances_link(lat, lon, ratings_dict):
    home = '{},{}'.format(lat,lon)
    search_string= '|'.join(['{},{}'.format(business['lat'], business['lon']) 
                        for business in ratings_dict.values()])
    walk_link = GOOGLE_DISTANCE_API.format(home,search_string,'walking',GOOGLE_API_KEY)
    bad_drive_link = GOOGLE_DISTANCE_API.format(home,search_string,'driving',GOOGLE_API_KEY) + '&departure_time={}&traffic_model=pessimistic'.format(get_next_weekday_6pm())
    good_drive_link = GOOGLE_DISTANCE_API.format(home,search_string,'driving',GOOGLE_API_KEY)
    return walk_link, bad_drive_link, good_drive_link


def get_next_weekday_6pm():
    #IMPLEMENT THIS
    return '1482793200' #Last monday in December 2016


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
    distance = R * c * 0.621371 # km to miles conversion
    return distance


def get_closest_police(state, lat, lng):
    try:
        conn = psycopg2.connect("dbname='{}' user='{}' host='{}' password='{}'"\
                                          .format(DBNAME, DBUSER, DBHOST, DBPW))
    except:
        print("Database Connection Error")
        return None

    cursor = conn.cursor()
    STATEMENT = 'SELECT * FROM crime_data_final WHERE STATE = %s'
    data = state
    cursor.execute(STATEMENT, [data])
    agencies = cursor.fetchall()
    cursor.close()
    conn.close()
    closest_dist = None
    closest_agency = None
    violent_crime_pc = None
    violent_rank = None
    property_crime_pc = None
    property_rank = None
    pol_info = []
    for agency in agencies:
        distance = measure_distances(float(lat), float(lng), agency[32], agency[33])
        if closest_dist is None or distance < closest_dist:
            closest_dist = distance
            violent_rank = agency[19]
            violent_pc = agency[18]
            property_rank = agency[26]
            property_pc = agency[25]
            closest_agency = agency
            pol_info = [closest_dist, violent_rank, violent_pc, property_rank, property_pc, closest_agency]
    return pol_info


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
    return data[0][-1]

    
def analysis(address):
    address_dict = get_address_info(address)
    yelp_dict, yelp_results = get_yelp_results(address_dict['lat'],address_dict['lng'])
    walk_link, bad_drive_link, good_drive_link = get_distances_link(address_dict['lat'], 
                                                                    address_dict['lng'],
                                                                    yelp_dict)
    walk_distance = get_business_distances(walk_link)
    good_drive_dist = get_business_distances(good_drive_link)
    bad_drive_dist = get_business_distances(bad_drive_link)
    pol_info = get_closest_police(str(address_dict['state']), 
                                      address_dict['lat'], 
                                      address_dict['lng'])

    lum = get_lum(address_dict['postal_code'])

    #############
    #Get avg yelp review grade
    ratings = [(business_dict['rating'],business_dict['review_count'], 
                                        business_dict['distance']) for 
                                        business_dict in yelp_dict.values() 
                                        if business_dict['rating']]
    print([rating[1] for rating in ratings])
    total_rev = 0.0
    weighted_score = 0.0
    avg_review = sum([rating[0] for rating in ratings])/len(ratings)
    for bus in ratings:
        total_rev += log1p(bus[1])
    #calc distance weight
    for bus in ratings:
        weight = log1p(bus[1]) / total_rev
        weighted_score += weight * bus[0]
        
    weighted_score = weighted_score/len(ratings)
    rest_grade = grader(((avg_review)/5)*100)
    #############
    
    avg_walk = sum(walk_distance)/len(walk_distance)
    avg_good_dr = sum(good_drive_dist)/len(good_drive_dist)
    avg_bad_dr = sum(bad_drive_dist)/len(bad_drive_dist)
    final_result = {
                    'address':address_dict,
                    'average_review': avg_review,
                    'weighted_review':weighted_score,
                    'total_reviews':total_rev,
                    'lum':lum,
                    'police_name':pol_info[-1][0],
                    'pol_distance':pol_info[0],
                    'violent_crime_pc':pol_info[2],
                    'violent_rank':pol_info[1],
                    'property_crime_pc':pol_info[4],
                    'property_rank':pol_info[3],
                    'pol_row':pol_info[-1],
                    'avg_walk':avg_walk,
                    'avg_good_dr':avg_good_dr,
                    'avg_bad_dr':avg_bad_dr,
                    'yelp_results':yelp_dict,
                    'avg_yelp_rating':avg_review
                    }
                    
    walk_grade, drive_grade = grade(final_result)
    
    # final_result['yelp_results'] = yelp_results
    
    final_result['walk_grade'] = walk_grade
    final_result['drive_grade'] = drive_grade
    final_result['rest_grade'] = rest_grade

    return final_result

def grader (z):
    if   z >= 0 and z < 60:
        return "F"
    elif z >= 60 and z < 63:
        return "D-"
    elif z >= 63 and z < 67:
        return "D"
    elif z >= 67 and z < 70:
        return "D+"
    elif z >= 70 and z < 73:
        return "C-"
    elif z >= 73 and z < 77:
        return "C"
    elif z >= 77 and z < 80:
        return "C+"   
    elif z >= 80 and z < 83:
        return "B-"
    elif z >= 83 and z < 87:
        return "B"
    elif z >= 87 and z < 90:
        return "B+"
    elif z >= 90 and z < 93:
        return "A-"
    else:
        return "A"
        
        
def grade_walk(lum, avg_walk_time, violent_crime_rank, property_crime_rank):
    walk_range = {1 : [0, 15], .8 : [15, 30], .6 : [30, 45], .4 : [45, 60], .2 : [60, 99999999]}
    for k,v in walk_range.items():
        if v[0] <= avg_walk_time < v[1]:
            walk_score = k
            break
    scores = [lum, walk_score, 1 - property_crime_rank, 1 - violent_crime_rank]
    result = 0
    for score in scores:
        result += score*25
        
    return grader(result)
    
    
def grade_drive(avg_good_dr, avg_bad_dr, violent_crime_rank, property_crime_rank):
    drive_variance = avg_bad_dr - avg_good_dr
    good_ranges = {1 : [0, 7], .8 : [7, 14], .6 : [14, 21], .4 : [21, 30], .2 : [30, 99999999]}
    bad_ranges = {1 : [0, 15], .8 : [15, 30], .6 : [30, 45], .4 : [45, 60], .2 : [60, 99999999]}
    var_ranges = {1 : [0, 5], .8 : [5, 10], .6 : [10, 15], .4 : [15, 20], .2 : [20, 99999999]}

    for k,v in good_ranges.items():
        if v[0] <= avg_good_dr < v[1]:
            good_dr_score = k
            break
    for k,v in bad_ranges.items():
        if v[0] <= avg_bad_dr < v[1]:
            bad_dr_score = k
            break
    for k,v in var_ranges.items():
        if v[0] <= drive_variance < v[1]:
            variance_score = k
            break
    
    scores = [good_dr_score, bad_dr_score, variance_score, 1-property_crime_rank, 1-violent_crime_rank]
    result = 0
    for score in scores:
        result += score*20
        
    return grader(result)
    
    
def grade(factor_dict):
    walk_grade = grade_walk(factor_dict['lum'], factor_dict['avg_walk'], factor_dict['violent_crime_pc'], factor_dict['violent_crime_pc'])
    drive_grade = grade_walk(factor_dict['avg_good_dr'], factor_dict['avg_bad_dr'], factor_dict['violent_crime_pc'], factor_dict['property_crime_pc'])
    return walk_grade, drive_grade