from flask import render_template, flash, redirect, session, url_for, request, g
from utakeout import app
from helpers import analysis
import json
# from forms import AddressForm


@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        address = request.form['address']
        return redirect(url_for('score', address=address))
    return render_template('index.html')

@app.route('/score/<address>')
def score(address):
    score_data = analysis(address)
    yelp_list = sorted(score_data['yelp_results'].values(), key=lambda k: k['distance'])
    yelp_markers = [[restaurant['name'], restaurant['lat'], restaurant['lon']] for restaurant in yelp_list]
    num_places = len(yelp_list)
    sum_reviews = sum([restaurant['review_count'] for restaurant in yelp_list])
    return render_template('score.html',
    						number=score_data['address']['street_number'],
    						street=score_data['address']['route'],
    						town=score_data['address']['locality'],
    						state=score_data['address']['state'],
    						zip=score_data['address']['postal_code'],
    						lum=score_data['lum'],
    						rep_agency=score_data['police_name'],
    						rep_agency_dist=score_data['pol_distance'],
    						violent_crime_pc=score_data['violent_crime_pc'],
    						violent_rank=score_data['violent_rank'],
    						property_crime_pc=score_data['property_crime_pc'],
    						property_rank=score_data['property_rank'],
    						restaurants=yelp_list,
    						address_lat=score_data['address']['lat'],
    						address_lng=score_data['address']['lng'],
    						yelp_markers=json.dumps(yelp_markers),
    						num_places=num_places,
    						sum_reviews=sum_reviews,
    						avg_yelp_rating=score_data['avg_yelp_rating'],
    						avg_walk=score_data['avg_walk'],
    						avg_good_dr=score_data['avg_good_dr'],
    						avg_bad_dr=score_data['avg_bad_dr'],
    						walk_grade=score_data['walk_grade'],
    						drive_grade=score_data['drive_grade'],
    						rest_grade=score_data['rest_grade']
    						)
