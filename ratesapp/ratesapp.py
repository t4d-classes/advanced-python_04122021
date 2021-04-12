from flask import Flask, jsonify, abort
from typing import Any
import pathlib, csv, math

rates: list[dict[str,Any]] = []

data_file_path = pathlib.Path("data", "eurofxref-hist.csv")

with open(data_file_path) as data_file:
    data_file_csv = csv.DictReader(data_file)

    for rate_row in data_file_csv:

        rate = { "Date": rate_row["Date"], "EUR": 1.0 }

        for rate_col in rate_row:
            if rate_col != "Date" and len(rate_col) > 0:
                if rate_row[rate_col] == "N/A":
                    rate[rate_col] = math.nan
                else:
                    rate[rate_col] = float(str(rate_row[rate_col]))

        rates.append(rate)


app = Flask(__name__)

@app.route("/api/<rate_date>")
def rates_by_date(rate_date: str) -> Any:

    for rate in rates:
        if rate["Date"] == rate_date:
            return jsonify(rate)
    
    abort(404)

