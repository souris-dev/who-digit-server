# views.py

from flask import render_template
from flask import send_file
from app import app

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/reference')
def reference():
    return render_template('reference.html')

@app.route('/download')
def download():
    return send_file('static/NotYetMade.apk')