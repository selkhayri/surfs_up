# -*- coding: utf-8 -*-

# Adding dependencies

import datetime as dt
import numpy as np
import pandas as pd

# SQLAlchemy dependencies
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# Flask dependencies
from flask import Flask, jsonify

weather_app = Flask(__name__)

# Set Up the Database
engine = create_engine("sqlite:///hawaii.sqlite")

# Reflect the database into our classes
Base = automap_base()
Base.prepare(engine, reflect=True)

# Save our references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create a session link from Python to our database
#session = Session(engine)
def get_session():
    global session
    session = Session(engine)

@weather_app.route("/")
def welcome():
    return(
    '''
    <h1>Welcome to the Climate Analysis API!</h1>
    
    <h3>Available Routes:</h3>
    <ul>
    <li>/api/v1.0/precipitation</li>
    <li>/api/v1.0/stations</li>
    <li>/api/v1.0/tobs</li>
    <li>/api/v1.0/temp/start</li>
    <li>/api/v1.0/temp/start/end</li>
    </ul>
    ''')
    
@weather_app.route("/weather_api/v1.0/precipitation")
def precipitation():
    get_session()
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    precipitation = session.query(Measurement.date, Measurement.prcp).\
      filter(Measurement.date >= prev_year).all()
    precip = {date: prcp for date, prcp in precipitation}
    # return jsonify(precip)
    return precip
    
@weather_app.route("/weather_api/v1.0/stations")
def stations():
    get_session()
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    print(f"results\n{results}")
    print(f"np.ravel(results)\n{np.ravel(results)}")
    return jsonify(stations=stations)
    
    # return "stations"

@weather_app.route("/weather_api/v1.0/tobs")
def temp_monthly():
    get_session()
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
	
    results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= prev_year).all()
    
    temps = list(np.ravel(results))
	
    #return jsonify(temps=temps)
    return temps

@weather_app.route("/weather_api/v1.0/temp/<start>")
@weather_app.route("/weather_api/v1.0/temp/<start>/<end>")
def stats(start=None, end=None):
    get_session()
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end: 
        results = session.query(*sel).\
          filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        #return jsonify(temps)
    else:
        results = session.query(*sel).\
            filter(Measurement.date >= start).\
                filter(Measurement.date <= end).all()
        temps = list(np.ravel(results))
        
    return jsonify(temps=temps)