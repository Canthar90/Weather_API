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