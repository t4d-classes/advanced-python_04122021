import time
import requests
import threading


def get_random_nums(results: list[str]) -> None:
    response = requests.request("GET", "http://127.0.0.1:5000/")
    results.append(response.text)

if __name__ == "__main__":

    start_time = time.time()

    results: list[str] = []
    threads: list[threading.Thread] = []

    for _ in range(30):
        a_thread = threading.Thread(target=get_random_nums, args=(results,))
        a_thread.start()
        threads.append(a_thread)
        
    for a_thread in threads:
        a_thread.join()

    print(len(results))

    print(time.time() - start_time)