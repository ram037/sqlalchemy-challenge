import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite?check_same_thread=False")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    return (
        f"Welcome to my sqlalchemy Challenge API page<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    """Convert the query results to a Dictionary using date as the key and prcp as the value.
    Return the JSON representation of your dictionary"""
    # Run the query required
    results = session.query(Measurement.date, Measurement.prcp, Measurement.station).all()
    
    # Create a dictionary from the data
    prcp_dict = {}
    for result in results:
        date = result[0]
        prcp = result[1]
        station = result[2]
        prcp_dict[station + "-" + date] = prcp
    return jsonify(prcp_dict)

@app.route("/api/v1.0/stations")
def stations():
    """Return a JSON list of stations from the dataset"""
    # Run the query required
    results = session.query(Station.station, Station.name).all()
    
    # Create a dictionary from the data
    station_dict = {}
    for result in results:
        station = result[0]
        name = result[1]
        station_dict[station] = name
    return jsonify(station_dict)


@app.route("/api/v1.0/tobs")
def tobs():
    """query for the dates and temperature observations from a year from the last data point.
    Return a JSON list of Temperature Observations (tobs) for the previous year."""
    # Run the query required
    year_ago_date = dt.date(2017,8,23) - dt.timedelta(days=365)
    results = session.query(Measurement.station, Measurement.date, Measurement.tobs).filter(Measurement.date >= year_ago_date).all()
    
    # Create a dictionary from the data
    tobs_dict = {}
    for result in results:
        station = result[0]
        date = result[1]
        tobs = result[2]
        tobs_dict [station + "-" + date] = tobs
    return jsonify(tobs_dict)
        
@app.route("/api/v1.0/temp/<start_date>")
@app.route("/api/v1.0/temp/<start_date>/<end_date>")
def stats(start_date, end_date=None):
    if not end_date: 
        results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start_date).all()
        return jsonify(results)
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
