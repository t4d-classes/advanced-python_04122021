import time
import requests
import threading


if __name__ == "__main__":

    start_time = time.time()

    results = []
    threads: list[threading.Thread] = []

    for _ in range(30):
        response = requests.request("GET", "http://127.0.0.1:5000/")
        results.append(response.text)

    print(len(results))

    print(time.time() - start_time)