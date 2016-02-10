from flask import render_template, flash, redirect, session, url_for, request, g
from utakeout import app
from helpers import analysis, nth
import json
import os
# from forms import AddressForm


@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        address = request.form['address']
        result = analysis(address)
        if isinstance(result,str):
        	return render_template('index.html',message=result)
        return redirect(url_for('score', address=address))
    return render_template('index.html',message='')

@app.route('/score/<address>')
def score(address):
    score_data = analysis(address)
    yelp_list = sorted(score_data['yelp_results'].values(), key=lambda k: k['distance'])
    yelp_markers = [[restaurant['name'], restaurant['lat'], restaurant['lon']] for restaurant in yelp_list]
    num_places = len(yelp_list)
    sum_reviews = sum([restaurant['review_count'] for restaurant in yelp_list])
    violent_rank = nth(str(int(score_data['violent_rank'] * 100)))
    property_rank = nth(str(int(score_data['property_rank'] * 100)))
    return render_template('score.html',
    						number=score_data['address']['street_number'],
    						street=score_data['address']['route'],
    						town=score_data['address']['locality'],
    						state=score_data['address']['state'],
    						zip=score_data['address']['postal_code'],
    						lum=score_data['lum'],
    						rep_agency=score_data['police_name'],
    						rep_agency_dist=score_data['pol_distance'],
    						pop_served=score_data['pop_served'],
    						violent_crime_pc=score_data['violent_crime_pc'],
    						violent_rank=violent_rank,
    						property_crime_pc=score_data['property_crime_pc'],
    						property_rank=property_rank,
    						restaurants=yelp_list,
    						address_lat=score_data['address']['lat'],
    						address_lng=score_data['address']['lng'],
    						yelp_markers=json.dumps(yelp_markers),
    						num_places=num_places,
    						sum_reviews=sum_reviews,
    						avg_yelp_rating=score_data['avg_yelp_rating'],
    						num_walkable=score_data['num_walkable'],
    						avg_walk=score_data['avg_walk'],
    						avg_good_dr=score_data['avg_good_dr'],
    						avg_bad_dr=score_data['avg_bad_dr'],
    						walk_grade=score_data['walk_grade'],
    						drive_grade=score_data['drive_grade'],
    						rest_grade=score_data['rest_grade'],
    						walk_img=score_data['walk_img'],
    						gd_img=score_data['gd_img'],
    						bd_img=score_data['bd_img']
    						)

@app.route('/about')
def about():
	return render_template('about.html')