def grader (z):
    """Converts a numeric value into a letter grade.

    Returns a string
    """
    if   z < 60:
        return "F"
    elif 60 <= z < 63:
        return "D-"
    elif 63 <= z < 67:
        return "D"
    elif 67 <= z < 70:
        return "D+"
    elif 70 <= z < 73:
        return "C-"
    elif 73 <= z < 77:
        return "C"
    elif 77 <= z < 80:
        return "C+"
    elif 80 <= z < 83:
        return "B-"
    elif 83 <= z < 87:
        return "B"
    elif 87 <= z < 90:
        return "B+"
    elif 90 <= z < 93:
        return "A-"
    elif 93 <= z < 97:
        return "A"
    else:
        return "A+"


def grade_walk_func(num_walkable, lum, avg_walk_time, violent_crime_rank, property_crime_rank):
    """Creates 0-100 grade based on inputs and returns that grade as a letter.

    Inputs:
        First: num_walkable - an integer that is the count of restaurants within 1 miles
        Second: lum - a floating point number between 0 and 1
        Third: Avg_walk_time - a floating point number greater than 0
        Fourth: Violent_crime_rank - a floating point number between 0 and 1
        Fifth: property_crime_rank - a floating point number between 0 and 1

    Returns: a string
    """
    walk_range = {1 : [0, 15], .8 : [15, 30], .6 : [30, 45], .4 : [45, 60], .2 : [60, 99999999]}
    for k,v in walk_range.items():
        if v[0] <= avg_walk_time < v[1]:
            walk_score = k
            break
    walkable_score = 1 if num_walkable >= 15 else num_walkable/15.0

    result = (lum*15) + (walkable_score*30) + (walk_score*30) + ((1-property_crime_rank)*15) + \
             ((1-violent_crime_rank)*10)
    return grader(result)


def grade_drive_func(avg_good_dr, avg_bad_dr, violent_crime_rank, property_crime_rank):
    """Creates 0-100 grade based on inputs and returns that grade as a letter.

    Inputs:
        First: avg_good_dr - a floating point number greater than 0
        Second: avg_bad_dr - a floating point number greater than 0
        Fourth: Violent_crime_rank - a floating point number between 0 and 1
        Fifth: property_crime_rank - a floating point number between 0 and 1

    Returns: a string
    """
    drive_variance = avg_bad_dr - avg_good_dr
    good_ranges = {1 : [0, 5], .8 : [5, 10], .6 : [10, 15], .4 : [15, 20], .2 : [25, 99999999]}
    bad_ranges = {1 : [0, 10], .8 : [10, 20], .6 : [20, 30], .4 : [30, 40], .2 : [40, 99999999]}
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

    result = (good_dr_score*35) + (bad_dr_score*30) + (variance_score*15) + \
              ((1-property_crime_rank)*10) + ((1-violent_crime_rank)*10)

    return grader(result)


def grade(factor_dict):
    """Constructs a walk_grade and a drive_grade from a dictionary of factors
    constructed in the analysis() function.

    Returns a 2 element tupple of strings
    """
    walk_grade = grade_walk_func(factor_dict['num_walkable'], factor_dict['lum'],
                                factor_dict['avg_walk'], factor_dict['violent_rank'],
                                factor_dict['property_rank'])
    drive_grade = grade_drive_func(factor_dict['avg_good_dr'], factor_dict['avg_bad_dr'],
                                   factor_dict['violent_rank'], factor_dict['property_rank'])
    return walk_grade, drive_grade