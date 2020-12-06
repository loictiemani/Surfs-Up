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
        f"<a href='api/v1.0/precipitation'>Precipitation</a><br/>"
        f"<a href='api/v1.0/stations'>List of Stations</a><br/>"
        f"<a href='api/v1.0/tobs'>Temperature</a><br/>"
        f"<a href='api/v1.0/startdate'>Temperature from the start date</a><br/>"
        f"<a href='api/v1.0/start_to_end'>Temperature from start to end date</a><end>"
    )
@app.route("/api/v1.0/precipitation")
def precipitation():
    
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    one_year = dt.timedelta(365)
    one_year_date = dt.datetime.strptime(last_date[0],"%Y-%m-%d") - one_year    
    precipitation_data = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date>one_year_date).order_by(Measurement.date).all()
    prcp_totals = []
    for result in precipitation_data:
        row = {}
        row["date"] = result[0]
        row["prcp"] = result[1]
        prcp_totals.append(row)
    
    return jsonify(prcp_totals)

@app.route("/api/v1.0/stations")
def stations():
    return f"test text - stations"
@app.route("/api/v1.0/tobs")
def tobs():
    return f"test text - tobs."
@app.route("/api/v1.0/startdate")
def startdate():
    return f"test text - startdate"
@app.route("/api/v1.0/start_to_end")
def start_to_end():
    return f"test text - start_to_end"

    #print(precipitation_data)



#@app.route("/jsonify")    
# 4. Define main behavior
if __name__ == "__main__":
    app.run(debug=True) 