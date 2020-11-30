import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

engine = create_engine("sqlite:///hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

app = Flask(__name__)

@app.route("/")
def welcome():
    return(
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.prcp).order_by(Measurement.date).all()
    
    precip_list = []

    for date, prcp in results:
        precip_dict = {}
        precip_dict["Date"] = date
        precip_dict["Precipitation"] = prcp
        precip_list.append(precip_dict)

    
    return jsonify(precip_list)



@app.route("/api/v1.0/stations")
def station():
    session = Session(engine)

    stations = []

    results = session.query(Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation).all()
    for station, name, latitude, longitude, elevation in results:
        station_dict = {}
        station_dict["Station"] = station
        station_dict["Name"] = name
        station_dict["Lat"] = latitude
        station_dict["Lon"] = longitude
        station_dict["Elevation"] = elevation
        stations.append(station_dict)

    return jsonify(station_dict)


@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    last_year = session.query(Measurement.date).order_by((Measurement.date).desc()).first()
    prev_year = (dt.datetime.strptime(last_year[0],'%Y-%m-%d') - dt.timedelta(days=365)).strftime('%Y-%m-%d')

    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= prev_year).order_by(Measurement.date).all()

    tobs_list = []

    for date, tobs in results:
        tobs_dict = {}
        tobs_dict["Date"] = date
        tobs_dict["Temp Observation"] = tobs
        tobs_list.append(tobs_dict)

    return jsonify(tobs_list)



#@app.route("/api/v1.0/<start>")
#def start():




#@app.route("/api/v1.0/<start>/<end>")
#def end():


if __name__ == "__main__":
    app.run(debug=True)