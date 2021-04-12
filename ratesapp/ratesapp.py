from flask import Flask, jsonify
from typing import Any

app = Flask(__name__)

@app.route("/api/<rate_date>")
def rates_by_date(rate_date: str) -> Any:
    
    return jsonify({ "date": rate_date })

