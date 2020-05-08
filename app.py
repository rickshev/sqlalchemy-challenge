from matplotlib import style
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
import datetime as dt
from flask import Flask, jsonify
from flask_sqlalchemy import sqlalchemy

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)
Base.classes.keys()

measurement = Base.classes.measurement
station = Base.classes.station

session = Session(engine)

# flask app
app = Flask(__name__)

@app.route("/")
def home():
    return(
        f"Available routes:</br>"
        f"/api/v1.0/precipitation</br>"
        f"/api/v1.0/stations</br>"
        f"/api/v1.0/tobs</br>"
        f"/api/v1.0/<start></br>"
        f"/api/v1.0/<start>/<end></br>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():


@app.route("/api/v1.0/stations")
def stations():
    results = session.query(station.name).all()
    station_list = list(np.ravel(results))
    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    station_query = session.query(measurement.station, func.count(measurement.station)).\
                    group_by(measurement.station).\
                    order_by(func.count(measurement.station).desc()).all()

    active_station = station_query[0][0]
    active_station_name = session.query(station.name).filter(station.station == active_station)
    active_station_name = active_station_name[0][0]

    last_date = session.query(measurement.date).order_by(measurement.date.desc()).first()
    last_date = last_date[0]

    first_date = dt.date(2017, 8, 23) - dt.timedelta(days = 365)

    temp_data = session.query(measurement.date, measurement.tobs).\
                filter(measurement.date >= first_date).\
                filter(measurement.station == active_station).\
                order_by(measurement.date).all()
    
    temp_list = []
    for t in temp_data:
        temp_dict = {temp_data.date: temp_data.tobs, "Station": temp_data.station}
        temp_list.append(temp_dict)
    
    return print(f"The most active station is {active_station}, {active_station_name}")
    return jsonify(temp_list)

@app.route("/api/v1.0/<start>")
def start(start):
    
