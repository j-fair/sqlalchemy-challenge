import numpy as np
import datetime as dt
import scipy
from scipy import stats

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()

Base.prepare(engine, reflect = True)

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

app = Flask(__name__)

@app.route("/")
def home():
    return (
        f"All available routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"

    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)

    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    data = []
    for date, rain, in results:
        data_dict = {}
        data_dict["date"] = date
        data_dict["prcp"] = rain
        data.append(data_dict)

    return jsonify (data)

@app.route("/api/v1.0/stations")
def stations():
    stations = session.query(Station.station, Station.name).all()
    stations_list = list(stations)
    return jsonify(stations_list)


@app.route("/api/v1.0/tobs")
def tobs():
    year_prior = dt.date(2017,8,23) - dt.timedelta(days=365)
    tobs_data = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= year_prior)

    tobs_data_list = list(tobs_data)

    return jsonify(tobs_data_list)


@app.route('/api/v1.0/<start>')
@app.route('/api/v1.0/<start>/<end>')
def date_range(start=None, end=None):

    session = Session(engine)

    if end != None:
        temps = session.query(
            func.round(func.min(Measurement.tobs),2),
            func.round(func.max(Measurement.tobs),2),
            func.round(func.avg(Measurement.tobs),2)).\
            filter(Measurement.date >= start).\
            filter(Measurement.date <= end).all()

        temps_list = list(temps)
        return jsonify(temps_list)

    else:
        temps = session.query(
            func.round(func.min(Measurement.tobs),2),
            func.round(func.max(Measurement.tobs),2),
            func.round(func.avg(Measurement.tobs),2)).\
            filter(Measurement.date >= start).all()
        
        temps_list = list(temps)
        return jsonify (temps_list)
    



if __name__ == '__main__':
    app.run(debug=True)