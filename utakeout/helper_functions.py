from math import radians, sin, cos, atan2, sqrt

from config import R


def get_next_weekday_6pm():
    """Currently returns a string of the time since epoch of December 26th, 2016 at 6:00pm"""
    #IMPLEMENT THIS
    return '1482793200' #Last monday in December 2016


def measure_distances(latitude1, lng1, latitude2, lng2):
    """Returns the distance in miles between 2 global coordinates"""
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


def nth(percentile):
    """Constructs Percentile Label

    Returns a string
    """
    last_digit = percentile[-1]
    if percentile in ['11','12','13','14','15','16','17','18','19']:
        return '{}th'.format(percentile)
    elif last_digit in ['0','4','5','6','7','8','9']:
        return '{}th'.format(percentile)
    elif last_digit == '2':
        return '{}nd'.format(percentile)
    else:
        return '{}rd'.format(percentile)
