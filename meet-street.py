# all the imports
from __future__ import with_statement
from sqlite3 import dbapi2 as sqlite3
from contextlib import closing
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
import string, random, socket, logging

# create our little application :)
app = Flask(__name__)
app.config.from_object('development_config')
app.config.from_envvar('MEET_STREET_CONFIG')
if not app.config['DEBUG']:
  file_handler = logging.FileHandler(filename="logs/production.log")
  app.logger.setLevel(logging.WARNING)
  app.logger.addHandler(file_handler)


@app.route('/')
def index():
  return render_template('index.html')

if __name__ == '__main__':
  app.run()
