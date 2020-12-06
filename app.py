#1. Import Flask
from flask import Flask, jsonify
from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

# Dependencies and Setup
import numpy as np
import pandas as pd
import datetime as dt

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Reflect Existing Database Into a New Model
Base = automap_base()

# Reflect the Tables
Base.prepare(engine, reflect=True)

# Save References to Each Table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create Session (Link) From Python to the DB
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
            f"<a href='api/v1.0/2015-03-15'>Temperature from the start date (default '15-03-2015)'</a><br/>"
            f"<a href='api/v1.0/2015-01-01/2016-01-01'>Temperature from start to end date (default '2015-01-01' to '2016-01-01')</a><end>"
        )
#Convert the query results to a dictionary using date as the key and prcp as the value.
#Return the JSON representation of your dictionary.
    
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

#Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")
def stations():
    allStations = []
    Stations_all = session.query(Station.station,Station.name, Station.latitude,Station.longitude, Station.elevation).all()
    for result2 in Stations_all:
        row = {}
        row["station"] = result2[0]
        row["name"] = result2[1]
        row["latitude"] = result2[2]
        row["longitude"] = result2[3]
        row["elevation"] = result2[4]
        allStations.append(row)
    return jsonify(allStations)

#Query the dates and temperature observations of the most active station for the last year of data.
#Return a JSON list of temperature observations (TOBS) for the previous year.

@app.route("/api/v1.0/tobs")
def tobs():
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    one_year = dt.timedelta(365)
    one_year_date = dt.datetime.strptime(last_date[0],"%Y-%m-%d") - one_year 

    tobs_data = session.query(Measurement.date,Measurement.tobs).filter(Measurement.date> one_year_date)\
        .filter(Measurement.station =='USC00519281').order_by(Measurement.date).all()
 
    
    tobs = []

    for temperature in tobs_data:
        row ={}
        row["Date"] = temperature[0]
        row["tobs"] = temperature[1]

        tobs.append(row)
   
    return jsonify(tobs)

#Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
#When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
#When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.

""" @app.route("/api/v1.0/<startdate>")
def start_date(startdate):
    session = Session(engine)
    startdate_formated = dt.datetime.strptime(startdate,"%Y-%m-%d")
    stats_temp = session.query(func.max(Measurement.tobs),func.min(Measurement.tobs),func.avg(Measurement.tobs))\
    .filter(Measurement.date > startdate_formated).all() 
    return jsonify(date = startdate)"""

@app.route("/api/v1.0/<startdate>")
def start_date(startdate):
    session = Session(engine)
    startdate_formated = dt.datetime.strptime(startdate,"%Y-%m-%d")
    stats_temp = session.query(func.max(Measurement.tobs),func.min(Measurement.tobs),func.avg(Measurement.tobs))\
    .filter(Measurement.date > startdate_formated ).all()
    return jsonify(max=stats_temp[0][0], min=stats_temp[0][1], avg=stats_temp[0][2])
    #start_day_list = list(stats_temp)
        # Return JSON List of Min Temp, Avg Temp and Max Temp for a Given Start Range
    #return jsonify(start_day_list)
    #return jsonify(max=stats_temp[0][0], min=stats_temp[0][1], avg=stats_temp[0][2])
    
   

@app.route("/api/v1.0/<startdate>/<enddate>")
def start_to_end(startdate,enddate):


    return jsonify ()

# 4. Define main behavior
if __name__ == "__main__":
    app.run(debug=True) 
