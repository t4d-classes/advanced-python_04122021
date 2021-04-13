from flask import Flask
from typing import Any
import random
import time

app = Flask(__name__)

@app.route("/")
def random_num() -> Any:

    time.sleep(random.randint(1, 10) * 0.15)

    return str(random.randint(1, 100))
