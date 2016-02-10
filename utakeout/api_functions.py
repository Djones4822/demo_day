import json
from time import sleep
import requests
import yelpapi
from config import YELP_CONSUMER_KEY, YELP_CONSUMER_SECRET, YELP_TOKEN, YELP_TOKEN_SECRET
from link_functions import get_geocode_link


def get_address_info(address):
    """Makes a request to Google and returns dictionary of address details"""
    address_request = requests.get(get_geocode_link(address))
    if address_request.status_code != 200:
        return None

    address_json = json.loads(address_request.text)
    if address_json['status'] != 'OK':
        return None


    address_dict = {'street_number' : None,
                    'route' : None,
                    'locality': None,
                    'administrative_area_level_2': None,
                    'administrative_area_level_1': None,
                    'postal_code': None
                    }

    for key in address_dict.keys():
        for bus_dict in address_json['results'][0]['address_components']:
            # return error if address isn't in US
            if 'country' in bus_dict['types']:
                if 'US' not in bus_dict['short_name']:
                    return None
            # return error if address is outside of contiguous US
            if 'administrative_area_level_1' in bus_dict['types']:
                if any(x in bus_dict['short_name'] for x in ['AK','HI','PR','GU','AS']):
                    return None
        
            if key in bus_dict['types']:
                address_dict[key] = bus_dict['short_name']
    address_dict['state'] = address_dict['administrative_area_level_1']
    address_dict['county'] = address_dict['administrative_area_level_2']
    address_dict['lat'] = address_json['results'][0]['geometry']['location']['lat']
    address_dict['lng'] = address_json['results'][0]['geometry']['location']['lng']

    return address_dict


def get_yelp_results(lat, lon):
    """Makes a request to Yelp for local restaurant information

    Requests 40 Yelp results based on distance to the coordinate location
    as determined by Yelp. Additionally, the request includes a search term
    of 'takeout' to find restaurants that provide such service.

    Returns:
        A dictionary of dictionaries
    """
    yelp_api = yelpapi.YelpAPI(YELP_CONSUMER_KEY, YELP_CONSUMER_SECRET, 
                               YELP_TOKEN, YELP_TOKEN_SECRET)
    results_json1 = yelp_api.search_query(sort=1, term='takeout', ll='{},{}'.format(lat,lon))
    results_json2 = yelp_api.search_query(sort=1, offset=20, limit=20,
                                          term='takeout', ll='{},{}'.format(lat,lon))
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
        categories = business.get('categories', None)
        if categories is not None:
            return_cat = ', '.join([cat[0] for cat in categories])
        ratings_dict[name] = {'name':name, 'review_count':review_count, 'rating':rating,
                            'lat':lat, 'lon':lon, 'deals':deals, 'distance':distance, 
                            'url':url, 'categories':return_cat}

    return ratings_dict


def get_business_distances(link):
    """Makes a request to Google Distances Matrix API.

    Returns a list of travel times resulting from the JSON response of the
    given link to Google Distance Matrix API.

    Automatically detects whether the parameter for traffic is included and 
    returns the appropriate travel times.
    """

    distance_matrix_request = requests.get(link)
    if distance_matrix_request.status_code != 200:
        return None

    distance_matrix = json.loads(distance_matrix_request.text)

    if distance_matrix['status'] != 'OK':
        return None

    results = distance_matrix['rows'][0]['elements']

    distances = []
    pessimistic_distances = []
    for business in results:
        if business['status'] != 'OK':
            distances.append(None)
            continue
        time = round(business['duration']['value']/60.0,2)
        try:
            traffic_time = round(business['duration_in_traffic']['value']/60.0,2)
        except:
            traffic_time = None
        distances.append(time)
        pessimistic_distances.append(traffic_time)

    sleep(.5)

    if all(distance == None for distance in pessimistic_distances):
        return distances
    else:
        return pessimistic_distances