from helper_functions import get_next_weekday_6pm
from config import GOOGLE_GEOCODE_API, GOOGLE_API_KEY, GOOGLE_DISTANCE_API


def get_geocode_link(input_address):
    """Generates Google Maps Geocoding API request url from address"""
    new_address = input_address.replace(' ','+')
    link = '{}{}&key={}'.format(GOOGLE_GEOCODE_API, new_address, GOOGLE_API_KEY)
    return link


def get_distances_link(lat, lon, ratings_dict):
    """Constructs a tuple of 3 Google Distance Matrix API links as strings.

    Based on the given lat/lon of a home address and a dictionary constructed
    from the get_yelp_results() function above, returns 3 links that each yield a
    JSON object.

    Returns:
        First:
            walk_link: a Google Distance Matrix API link with parameter "mode=walking"

        Second:
            bad_drive_link: a Google Distance Matrix API link with parameters "mode=driving",
                            "departure_time=1482793200" and "trafic_model=pessimistic"

        Third:
            good_drive_link: a Google Distance Matrix API link with parameters "mode="driving"
                             (this effectively ignores the possibility of traffic)

    """
    home = '{},{}'.format(lat,lon)
    search_string= '|'.join(['{},{}'.format(business['lat'], business['lon'])
                        for business in ratings_dict.values()])
    walk_link = GOOGLE_DISTANCE_API.format(home, search_string, 'walking', GOOGLE_API_KEY)
    bad_drive_link = GOOGLE_DISTANCE_API.format(home, search_string, 'driving', GOOGLE_API_KEY) + \
                    '&departure_time={}&traffic_model=pessimistic'.format(get_next_weekday_6pm())
    good_drive_link = GOOGLE_DISTANCE_API.format(home, search_string, 'driving', GOOGLE_API_KEY)
    return walk_link, bad_drive_link, good_drive_link