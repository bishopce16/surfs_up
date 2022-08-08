# Set Up the Flask Weather App 
# Import Dependency
import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# Import the Flask Dependency
from flask import Flask, jsonify
# Set Up the Database
# The create_engine() function allows us to access and 
# query our SQLite database file
engine = create_engine("sqlite:///hawaii.sqlite")
# eflect the database into our classes.
Base = automap_base()
Base.prepare(engine, reflect=True)
# create a variable for each of the classes so 
# that we can reference them later
Measurement = Base.classes.measurement
Station = Base.classes.station
# create a session link from Python to our database
session = Session(engine)
# Set Up Flask
# create a Flask application called "app."
app = Flask(__name__)
# define the welcome route
@app.route("/")

# create a function welcome() with a return statement
def welcome():
    return(
    '''
    Welcome to the Climate Analysis API!<br/>
    Available Routes:<br/>
    /api/v1.0/precipitation<br/>
    /api/v1.0/stations<br/>
    /api/v1.0/tobs<br/>
    /api/v1.0/temp/start/end<br/>
    ''')
# Precipitation Route
@app.route("/api/v1.0/precipitation")
# create the precipitation() function and write a query to get 
# the date and precipitation for the previous year.
def precipitation():
   prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
   precipitation = session.query(Measurement.date, Measurement.prcp).\
      filter(Measurement.date >= prev_year).all()
   precip = {date: prcp for date, prcp in precipitation}
   return jsonify(precip)
# Stations route
@app.route("/api/v1.0/stations")
# create a new function called stations(), with 
# a query that will allow us to get all of the stations in our database
# convert the results to a list and jsonify the list and return it as JSON
def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)
# Monthly Temperature Route
@app.route("/api/v1.0/tobs")
# create a function called temp_monthly(), calculate 
# the date one year ago from the last date in the database and 
# query the primary station for all the temperature observations from the previous year.
# # convert the results to a list and jsonify the list and return it as JSON.
def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
      filter(Measurement.station == 'USC00519281').\
      filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)
# Statistics Route, create a route to report on the minimum, average, 
# and maximum temperatures
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
# create a function called stats()
#  add parameters to our stats()function: 
# a start parameter and an end parameter
# create a query to select the minimum, average, 
# and maximum temperatures from our SQLite database
def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    # the asterisk is used to indicate there will be multiple results for our query: 
    # minimum, average, and maximum temperatures.
    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps)

