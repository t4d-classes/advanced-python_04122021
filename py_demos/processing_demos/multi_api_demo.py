import time
import multiprocessing as mp

def server_app() -> None:
    while True:
        pass

if __name__ == "__main__":

    start_time = time.time()

    a_process = mp.Process(target=server_app)
    a_process.start()

    time.sleep(2)

    print(a_process.is_alive())

    time.sleep(2)

    a_process.terminate()
    a_process.join()

    print(a_process.is_alive())

    a_process = mp.Process(target=server_app)
    a_process.start()
    a_process.terminate()
    a_process.join()

    print(time.time() - start_time)