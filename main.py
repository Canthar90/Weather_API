from flask import Flask, render_template, jsonify
from flask_bootstrap import Bootstrap
import pandas as pd



app = Flask(__name__)
Bootstrap(app)

stations = pd.read_csv("data\stations.txt", skiprows=17)
stations = stations[["STAID","STANAME                                 "]]

@app.route("/")
def home():
    return render_template("home.html", data=stations.to_html())


@app.route("/api/v1/<station>")
def station_data(station):
    station_nr = str(station).zfill(6)
    df = pd.read_csv("data\TG_STAID" +station_nr + ".txt", skiprows=20, parse_dates=["    DATE"])
    reasult = df.to_dict(orient="records")
    return jsonify(reasult)


@app.route("/api/v1/yearly/<station>/<year>")
def station_data_by_year(station, year):
    station_nr = str(station).zfill(6)
    df = pd.read_csv("data\TG_STAID" +station_nr + ".txt", skiprows=20)
    df["    DATE"] = df["    DATE"].astype(str)
    reasult = df[df["    DATE"].str.startswith(str(year))].to_dict(orient="records")
    return jsonify(reasult)


@app.route("/api/v1/<station>/<date>")
def about(station, date):
    station_nr = str(station).zfill(6)
    df = pd.read_csv("data\TG_STAID" +station_nr + ".txt", skiprows=20, parse_dates=["    DATE"])
    temperature = df.loc[df["    DATE"] == date]["   TG"].squeeze()/10
    
    output = {"station": station,
              "date": date,
              "temperature": temperature}
    return jsonify(output)


if __name__ == "__main__":
    app.run(debug=True)