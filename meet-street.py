# all the imports
from __future__ import with_statement
from sqlite3 import dbapi2 as sqlite3
from contextlib import closing
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
import string, random, socket, logging, json
from tasks import *

# create our little application :)
app = Flask(__name__)
app.config.from_object('development_config')
app.config.from_envvar('MEET_STREET_CONFIG')
if not app.config['DEBUG']:
  file_handler = logging.FileHandler(filename="logs/production.log")
  app.logger.setLevel(logging.WARNING)
  app.logger.addHandler(file_handler)

@app.route('/', methods=['POST', 'GET'])
def index():
  if request.method == 'POST':
    addresses = request.form.getlist("address[]")
    addresses = sanitizeAddresses(addresses)
    print addresses
    coords = []
    for addr in addresses:
      if len(addr.split(',')) == 2:
        try:
          lat = float(addr.split(',')[0])
          lng = float(addr.split(',')[1])
          coords.append([lat, lng])
          continue
        except ValueError:
          pass
      coords.append(getCoordinates(addr))
    print coords  
    coords = getConvexHullPoints(coords)
    centroid = findMidpoint(coords)
    locations = getPointsOfInterest(centroid[0], centroid[1])
    # Only return top 4 results
    locations = locations[:4]
    for location in locations:
      location["details"] = getDetails(location["place_id"])
    zoom = getZoomLevel(shortestDistance(coords))
    return render_template('maps.html', coords=coords, locations=locations, centroid=centroid, zoom=zoom)
  else:
    return render_template('index.html')


@app.route('/form', methods=['POST', 'GET'])
def form():
  if request.method == 'POST':
    addresses = request.form.getlist("address[]")
    for address in addresses:
      print getCoordinates(address)
  string = "blah"
  return render_template('form.html', string=string)

if __name__ == '__main__':
  app.run()
