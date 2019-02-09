import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
import time


#################################################
# Database Setup
#################################################
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
#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """ (List all available api routes)"""
    return (
        f"Welcome to Climate Analysis for Honolulu, Hawaii! <br/>" 
        f"<br/>"
        f"available routes:<br/>"
        f"<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"   
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start-date[YYYY-MM-DD]<br/>"
        f"/api/v1.0/start-date/[YYYY-MM-DD]/end-date/[YYYY-MM-DD]<br/>"             
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return a list with precipitation data and date"""
    # Query all passengers
    results = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >='2016-08-23').\
    order_by(Measurement.date).all()
    session.commit()

    # Create a dictionary
    all_prcp = []
    for prcp in results:
        prcp_dict = {}
        prcp_dict["date"] = prcp[0]
        prcp_dict["prcp"] = prcp[1]
        all_prcp.append(prcp_dict)
    time.sleep(2)
    return jsonify(all_prcp)
   
@app.route("/api/v1.0/stations")
def stations():
    """Return a list of weather stations"""
    # Query data table station and list variables (station number and name)
    results = session.query(Station.station, Station.name).all()
    session.commit()
    
     # Create a dictionary from the row data and append to a list, places
    places=[]
    for place in results:
        place_dict = {}
        place_dict["station_ID"] = place[0]
        place_dict["station_name"] = place[1]
        places.append(place_dict)
    time.sleep(2)
    return jsonify(places)

@app.route("/api/v1.0/tobs")
def tobs():
    """Return a list of temperature observations and dates (last 12 months)"""
    # Query data table measures for dates and temperature observations (tobs)
    # Include all observations begining 12 months before last date in database
    results = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.date >='2016-08-23').\
    order_by(Measurement.date).all()   
    session.commit()

    # Create a dictionary from the row data and append to a list, all_tobs
    all_tobs = []
    for tob in results:
        tob_dict = {}
        tob_dict["date"] = tob[0]
        tob_dict["tobs"] = tob[1]
        all_tobs.append(tob_dict)
    time.sleep(2)
    return jsonify(all_tobs)

@app.route("/api/v1.0/start-date/<start>")
def describe_temp_start_date(start):
    """Fetch the minimum, average and maximum temperature using a date
       variable supplied by the user"""
   
    result=session.query(func.min(Measurement.tobs),\
    func.avg(Measurement.tobs),func.max(Measurement.tobs)).filter(Measurement.date >= start).all()
    session.commit()
    time.sleep(2)
    return jsonify(result)
    
@app.route("/api/v1.0/start-date/<start>/end-date/<end>")
def calc_temps(start, end):
    """Fetch the minimum, average and maximum temperature using a start and end date 
    variable supplied by the user"""

    result=session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs),\
    func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    session.commit()
    time.sleep(2)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
