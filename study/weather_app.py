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
    <li>/api/v1.0/temp/start/end</li>
    </ul>
    ''')
    
@weather_app.route("/weather_app/v1.0/precipitation")
def precipitation():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    precipitation = session.query(Measurement.date, Measurement.prcp).\
      filter(Measurement.date >= prev_year).all()
    precip = {date: prcp for date, prcp in precipitation}
    # return jsonify(precip)
    return precip

@weather_app.route("/weather_app/v1.0/stations")
def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    print(f"results\n{results}")
    print(f"np.ravel(results)\n{np.ravel(results)}")
    return jsonify(stations=stations)

