# import dependencies
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
from flask import Flask, jsonify

# connect to database with automap
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Base.classes.keys()

# assign variable names to tables
measurement = Base.classes.measurement
station = Base.classes.station

# create session
session = Session(engine)

# flask app
app = Flask(__name__)

# home page that shows routes
@app.route("/")
def home():
    return(
        f"Available routes:</br>"
        f"/api/v1.0/precipitation</br>"
        f"/api/v1.0/stations</br>"
        f"/api/v1.0/tobs</br>"
        f"/api/v1.0/<start_date></br>"
        f"/api/v1.0/<start_date>/<end_date></br>"
    )

# precipitation route displaying last year of precipitation data
@app.route("/api/v1.0/precipitation")
def precipitation():
    results_prec = session.query(measurement.date, measurement.prcp).filter(measurement.date >= "2016-08-23").all()

    precip_list = list(np.ravel(results_prec))
    
    return jsonify(precip_list)

# stations route
@app.route("/api/v1.0/stations")
def stations():
    results_stat = session.query(station.name).all()

    station_list = list(np.ravel(results_stat))

    return jsonify(station_list)

# temperature route
@app.route("/api/v1.0/tobs")
def tobs():
    active_station_list = session.query(measurement.station, func.count(measurement.station)).\
                         group_by(measurement.station).\
                         order_by(func.count(measurement.station).desc()).all()
    
    active_station = active_station_list[0][0]

    results_temp = session.query(measurement.date, measurement.tobs).\
                filter(measurement.date >= "2016-08-23").\
                filter(measurement.station == active_station).\
                order_by(measurement.date).all()

    temp_list = list(np.ravel(results_temp))

    return jsonify(temp_list)

# start date route displaying temperatures
@app.route("/api/v1.0/<start_date>")
def start(start_date):
    results_date = session.query(measurement.date, func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).\
                       filter(measurement.date >= start_date).all()
    
    date_dict = {}
    
    for dt in results_date:
        diction = {}
        diction["Date"] = dt.date
        diction["Min"] = dt.func.min(measurement.tobs)
        diction["Max"] = dt.func.min(measurement.tobs)
        diction["Average"] = dt.func.avg(measurement.tobs)
        date_dict.append(diction)
    
    return jsonify(date_dict)

# start/end date route displaying all temperatures from start date to end date
@app.route("/api/v1.0/<start_date>/<end_date>")
def startend(start_date, end_date):
    results_date_2 = session.query(measurement.date, func.min(measurement.tobs, func.max(measurement.tobs), func.avg(measurement.tobs)).\
                        filter(measurement.date >= start_date).filter(measurement.date <= end_date).order_by(measurement.date).all()
    
    dates_dict = {}

    for x in results_date_2:
        dictionn = {}
        dictionn["Date"] = x.results_date_2[0]
        dictionn["Min"] = x.results_date_2[1]
        dictionn["Max"] = x.results_date_2[2]
        dictionn["Average"] = x.results_date_2[3]
        dates_dict.append(dictionn)
    
    return jsonify(dates_dict)

if __name__ == "__main__":
    app.run(debug=True)