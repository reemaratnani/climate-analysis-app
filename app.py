import numpy as np

import sqlalchemy
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)
# Flask Setup
app = Flask(__name__)

# Flask Route

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    
    # Query precipitation
    year_ago = year_ago = dt.date(2017, 8, 23) - dt.timedelta(days =365)
    result = session.query(Measurement.date, Measurement.prcp).\
             filter(Measurement.date >= year_ago).all()
    
    result =dict(result)

    return jsonify(result)


@app.route("/api/v1.0/stations")
def stations():
    station_id = session.query(Station.station, Station.name).all()
    station_id = list(np.ravel(station_id))

    return jsonify(station_id)

@app.route("/api/v1.0/tobs")
def tobs():
    year_ago = year_ago = dt.date(2017, 8, 23) - dt.timedelta(days =365)
    station_tobs = session.query(Measurement.tobs).\
                  filter(Measurement.station == 'USC00519281' ).\
                  filter(Measurement.date >= year_ago).all()
    station_tobs = list(np.ravel(station_tobs))

    return jsonify(station_tobs)

@app.route("/api/v1.0/start")
def calc_temps():
    """TMIN, TAVG, and TMAX for a list of dates.
    
    Args:
        start_date (string): A date string in the format %Y-%m-%d
        
    Returns:
        TMIN, TAVE, and TMAX
    """
    start_date = "2017-04-01"
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all()
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)