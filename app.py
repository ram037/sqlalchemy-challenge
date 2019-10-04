import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

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
        f"Welcome to Omar's sqlalchemy-challenge API!<br/>"
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
    
    # Create a dictionary from the row data and append to dates
    prcp_dict = {}
    for result in results:
        date = result[0]
        prcp = result[1]
        station = result[2]
        prcp_dict[station + "-" + date] = prcp
        
    return jsonify(prcp_dict)

# @app.route("/api/v1.0/stations")
# def stations():
#     """Return a JSON list of stations from the dataset"""
#     # Run the query required
#     session = Session(engine)
#     results = session.query(Station.station, Station.name).all()
    
#     # Create a dictionary from the row data and append to stations
#     all_stations = []
#     for station in results:
#         station_dict = {}
#         station_dict["station"] = station
#         station_dict["name"] = name
#         all_stations.append(station_dict)
        
#     return jsonify(all_stations)


# @app.route("/api/v1.0/tobs")
# def tobs():
#     """query for the dates and temperature observations from a year from the last data point.
#     Return a JSON list of Temperature Observations (tobs) for the previous year."""
#     # Run the query required
#     session = Session(engine)
#     year_ago_date = dt.date(2017,8,23) - dt.timedelta(days=365)
#     results = session.query(Measurement.date, Measurement.tobs).\
#               filter(Measurement.date >= year_ago_date).all()
    
#     # Create a dictionary from the row data and append to dates
#     yr_tobs = []
#     for tobs in results:
#         tobs_dict = {}
#         tobs_dict["date"] = date
#         tobs_dict["tobs"] = tobs
#         yr_tobs.append(tobs_dict)
        
#     return jsonify(yr_tobs)

@app.route("/api/v1.0/temp/<start_date>")
@app.route("/api/v1.0/temp/<start_date>/<end_date>")
def stats(start_date, end_date=None):
    if not end_date: 
        results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start_date).all()
        return jsonify(results)
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    return jsonify(results)

# @app.route("/api/v1.0/<start>")
# def start(start_date):
#     return session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
#         filter(Measurement.date >= start_date).all()
#     """Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range. 
#     When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date. 
#     When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive."""

#     # Run the query required
#     session = Session(engine)
#     results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
#               filter(Measurement.date >= start_date).all()
            
#     return jsonify(start)


##### Uncomment out to pick up where left off    
# @app.route("/api/v1.0/<start>")
# def start(start_date, end_date):
#     return session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
#         filter(Measurement.date >= start_date).all()
#     """Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range. 
#     When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date. 
#     When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive."""

#     # Run the query required
#     session = Session(engine)
#     results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
#               filter(Measurement.date >= start_date).all()
            
#     return jsonify(start)

if __name__ == '__main__':
    app.run(debug=True)
