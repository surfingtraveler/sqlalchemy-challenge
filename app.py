# Import the dependencies.
from flask import Flask, jsonify
import datetime as dt
import numpy as np
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Reflect an existing database into a new model
Station = Base.classes.station
Measurement = Base.classes.measurement

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
       f"Available Routes:<br/>"
       f"/api/v1.0/precipitation<br/>"
       f"/api/v1.0/stations<br/>"
       f"/api/v1.0/tobs<br/>"
       f"/api/v1.0/tobs/YYYY-MM-DD<br/>"
       f"/api/v1.0/tobs/YYYY-MM-DD/YYYY-MM-DD"
    )

#################################################

app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query the dates and prcp
    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()  

   # Convert results to a dictionary
    precipitation_data = dict()

    for date, prcp in results:
        precipitation_data[date] = prcp

    # Return the JSON representation of your dictionary.
    return jsonify(precipitation_data)

#################################################

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query the stations
    results = session.query(Station.station).all()

    session.close()

    # Convert results to a list
    station_list = [station[0] for station in results]

    return jsonify(station_list)

#################################################

@app.route("/api/v1.0/tobs")
def temperature():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Find the most active station
    active_stations = session.query(Measurement.station).\
        group_by(Measurement.station).\
        order_by(func.count(Measurement.station).desc()).\
        first()

    # Query the dates and temperature observations for the previous year
    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == active_stations[0]).\
        filter(Measurement.date >= dt.date(2017, 8, 23) - dt.timedelta(days=365)).\
        filter(Measurement.date <= dt.date(2017, 8, 23)).\
        all()

    session.close()

    # Convert results to a list of dictionaries
    temperature_data = dict()
    for date, tobs in results:
        temperature_data.append({"date": date, "tobs": tobs})

    return jsonify(temperature_data)

#################################################

@app.route("/api/v1.0/<start>")
def start_date(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    # Get the temperature summary for a specified start date to the end of the dataset.
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()

    session.close()

    temperature_list = list(np.ravel(results))

    return jsonify(temperature_list)

#################################################

@app.route("/api/v1.0/<start>/<end>")
def date_range(start, end):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    # Query the minimum, average, and maximum temperatures for the start date to the specified end date
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).\
        all()

    session.close()
    
    # Convert results to a flattened list
    temperature_list = list(np.ravel(results))

    return jsonify(temperature_list)



if __name__ == '__main__':
    app.run(debug=True)






        



    









