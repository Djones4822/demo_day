import psycopg2

from config import DBNAME, DBUSER, DBHOST, DBPW
from helper_functions import measure_distances


def get_closest_police(state, lat, lng):
    """Makes a query against the database for Police Information.Distance

    Returns list of information regarding the nearest police agency to the
    given coordinates.

    Resulting List elments (in order):
        Distance (miles), Percentile Rank of Violent Crimes per 100k Residents,
        number of violent crimes per 100k residents, percentile rank of Property
        Crimes per 100k residents, number of Property Crimes per 100k residents,
        Agency Name, Population Served by Agency.
    """
    try:
        conn = psycopg2.connect("dbname='{}' user='{}' host='{}' password='{}'" \
                                .format(DBNAME, DBUSER, DBHOST, DBPW))
    except:
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
            pop_served = agency[7]
            agency_name = agency[0]
            pol_info = [closest_dist, violent_rank, violent_pc, property_rank,
                        property_pc, agency_name, pop_served]
    return pol_info


def get_lum(zipcode):
    """Searches database for corresponding LUM value to the given zipcode.

    Returns: Floating Point Number"""
    try:
        conn = psycopg2.connect("dbname='{}' user='{}' host='{}' password='{}'" \
                                .format(DBNAME, DBUSER, DBHOST, DBPW))
    except:
        return None

    cursor = conn.cursor()
    statement = 'SELECT * FROM lumbyzcta WHERE zip = %s'
    data = [zipcode]
    cursor.execute(statement, data)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    if data:
        return data[0][-1]
    return None