from flask import render_template, flash, redirect, session, url_for, request, g
from utakeout import app
# from forms import AddressForm


@app.route('/', methods=['POST','GET'])
def index():
    if request.method == 'POST':
        address = request.form['address']
        return render_template('results.html', address=address)
    return render_template('index.html')