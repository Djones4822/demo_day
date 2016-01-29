from flask import render_template, flash, redirect, session, url_for, request, g
from utakeout import app
from helpers import get_lat_lon
# from forms import AddressForm


@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        address = request.form['address']
        return redirect(url_for('score', address=address))
    return render_template('index.html')

@app.route('/score/<address>')
def score(address):
    coords = get_lat_lon(address)
    return render_template('score.html', address=coords)
