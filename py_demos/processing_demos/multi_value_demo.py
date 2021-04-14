from multiprocessing.sharedctypes import Synchronized # type: ignore
import time
import multiprocessing as mp

def server_app(shared_data: Synchronized) -> None:
    while True:
        time.sleep(5)
        with shared_data.get_lock():
            shared_data.value = shared_data.value + 10

if __name__ == "__main__":

    shared_data: Synchronized = mp.Value('i', 100)
    start_time = time.time()

    a_process = mp.Process(target=server_app, args=(shared_data,))
    a_process.start()

    for _ in range(10):
        time.sleep(3)
        print(shared_data.value)

    a_process.terminate()
    a_process.join()