import threading
import time

def do_it() -> None:
    time.sleep(0.0000001)
    print("did it")


thread1 = threading.Thread(target=do_it)


print("getting ready to call start")
thread1.start()

print("some thread independent operation")

thread1.join()

print("done")