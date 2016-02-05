from flask import render_template, flash, redirect, session, url_for, request, g
from utakeout import app
from helpers import analysis
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
    return render_template('score.html',
    						number=score_data['address']['street_number'],
    						street=score_data['address']['route'],
    						town=score_data['address']['locality'],
    						state=score_data['address']['state'],
    						zip=score_data['address']['postal_code'],
    						lum=score_data['lum'],
    						rep_agency=score_data['police_name'],
    						rep_agency_dist=score_data['pol_distance'],
    						)
