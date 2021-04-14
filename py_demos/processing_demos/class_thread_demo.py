import time
import requests
import threading

class GetRandomNumsThread(threading.Thread):

    def __init__(self, results: list[str]) -> None:
        threading.Thread.__init__(self)
        self.results = results

    def run(self) -> None:
        response = requests.request("GET", "http://127.0.0.1:5000/")
        self.results.append(response.text)
        self.do_it()

    def do_it(self) -> None:
        print(self.ident)


if __name__ == "__main__":

    start_time = time.time()

    results: list[str] = []
    threads: list[GetRandomNumsThread] = []

    for _ in range(30):
        a_thread = GetRandomNumsThread(results)
        a_thread.start()
        threads.append(a_thread)
        
    for a_thread in threads:
        a_thread.join()

    print(len(results))

    print(time.time() - start_time)