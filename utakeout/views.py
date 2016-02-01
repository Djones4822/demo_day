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
    return render_template('score.html', address=score_data)
