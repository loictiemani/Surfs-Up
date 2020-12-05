#1. Import Flask
from flask import Flask, jsonify
from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

import numpy as np
import pandas as pd
import datetime as dt
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)
#2. Create an app
app = Flask(__name__)

#3.Define Static routes
@app.route("/")
def welcome():
    return (
        f"Available Routes:<br/>"
        f"Precipitation:/api/v1.0/precipitation<br/>"
        f"List of Stations:/api/v1.0/stations<br/>"
        f"Temperature:/api/v1.0/tobs<br/>"
        f"Temperature from the start date:/api/v1.0/<start><br/>"
        f"Temperature from start to end date:/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
 

    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    one_year = dt.timedelta(365)
    one_year_date = dt.datetime.strptime(last_date[0],"%Y-%m-%d") - one_year
    precipitation_data = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date>one_year_date).order_by(Measurement.date).all()

    print(precipitation_data)



#@app.route("/jsonify")    
