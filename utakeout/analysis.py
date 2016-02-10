from numpy import median

from get_box_plot import get_box_plot
from grading_functions import grader, grade
from database_functions import get_closest_police, get_lum
from api_functions import get_address_info, get_yelp_results, get_business_distances
from link_functions import get_distances_link
from config import ERROR_MESSAGE


def analysis(address):
    """Performs a detailed analysis of takeout information off a given address.

    Returns: Dictionary of information for website display.
    """
    address_dict = get_address_info(address)
    if address_dict is None:
        return ERROR_MESSAGE
    yelp_dict = get_yelp_results(address_dict['lat'],address_dict['lng'])
    if not yelp_dict:
        return ERROR_MESSAGE
    walk_link, bad_drive_link, good_drive_link = get_distances_link(address_dict['lat'],
                                                                    address_dict['lng'],
                                                                    yelp_dict)
    if any(not x for x in [walk_link, bad_drive_link, good_drive_link]):
        return ERROR_MESSAGE

    #Get distance list
    walk_distance = get_business_distances(walk_link)
    good_drive_dist = get_business_distances(good_drive_link)
    bad_drive_dist = get_business_distances(bad_drive_link)
    if any(not x for x in [walk_distance, good_drive_dist, bad_drive_dist]):
        return ERROR_MESSAGE

    #Get Box Plots
    walk_img = get_box_plot(walk_distance, str(address_dict['postal_code']))
    gd_img = get_box_plot(good_drive_dist, str(address_dict['postal_code']))
    bd_img = get_box_plot(bad_drive_dist, str(address_dict['postal_code']))

    if any((not x) for x in [bd_img, gd_img, walk_img]):
        return ERROR_MESSAGE

    pol_info = get_closest_police(str(address_dict['state']),
                                      address_dict['lat'],
                                      address_dict['lng'])
    lum = get_lum(address_dict['postal_code'])

    if not pol_info or not lum:
        return ERROR_MESSAGE

    ratings = [(business_dict['rating'],business_dict['review_count'],
                                        business_dict['distance']) for
                                        business_dict in yelp_dict.values()
                                        if business_dict['rating']]

    total_rev = sum([x[1] for x in ratings])
    avg_review = sum([rating[0] for rating in ratings])/len(ratings)
    median_review = median([rating[0] for rating in ratings])
    bus_dists = [bus[2] for bus in ratings]
    num_walkable = len([x for x in bus_dists if x <=1])

    avg_walk = sum(walk_distance)/len(walk_distance)
    median_walk = median(walk_distance)
    avg_good_dr = sum(good_drive_dist)/len(good_drive_dist)
    median_good = median(good_drive_dist)
    avg_bad_dr = sum(bad_drive_dist)/len(bad_drive_dist)
    median_bad = median(bad_drive_dist)

    final_result = {
                    'address':address_dict,
                    'average_review': avg_review,
                    'median_review': median_review,
                    'total_reviews':total_rev,
                    'lum':lum,
                    'median_walk': median_walk,
                    'median_bad': median_bad,
                    'median_good': median_good,
                    'police_name':pol_info[5],
                    'pol_distance':pol_info[0],
                    'pop_served':pol_info[6],
                    'violent_crime_pc':pol_info[2],
                    'violent_rank':pol_info[1],
                    'property_crime_pc':pol_info[4],
                    'property_rank':pol_info[3],
                    'avg_walk':avg_walk,
                    'avg_good_dr':avg_good_dr,
                    'avg_bad_dr':avg_bad_dr,
                    'yelp_results':yelp_dict,
                    'avg_yelp_rating':avg_review,
                    'gd_img':gd_img,
                    'bd_img':bd_img,
                    'walk_img':walk_img,
                    'num_walkable':num_walkable
                    }

    walk_grade, drive_grade = grade(final_result)
    rest_grade = grader(((avg_review)/5)*100)
    final_result['walk_grade'] = walk_grade
    final_result['drive_grade'] = drive_grade
    final_result['rest_grade'] = rest_grade

    return final_result