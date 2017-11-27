from flask import render_template
from app import app, db, models
import sys


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')


@app.route('/contact')
def contact():
    return render_template('contact.html', title='Contact')


@app.route('/faq')
def faq():
    return render_template('faq.html', title='FAQ')


@app.route('/map')
def map():
    # unique_locations = models.UniqueLocation.query.all()
    victims = models.UniqueVictims.query.all()
    # timeframe_data = {
    #     'tcp': [t.tcp_count for t in timeframes],
    #     'udp': [t.udp_count for t in timeframes],
    #     'icmp': [t.icmp_count for t in timeframes],
    #     'ip': [t.ip_count for t in timeframes]
    # }

    return render_template('map.html', title='DDoS Attack Map', victims=victims)

# @app.route('/map')
# def map():
#     return render_template('map.html', title='DDoS Attack Map',
#                            model=models.Victims.query.filter_by(ip='149.67.91.179').first())
