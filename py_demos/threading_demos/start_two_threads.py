import threading
import time

mydata = threading.local()

def do_something() -> None:
    print("mydata.iam = " + mydata.iam)

def do_it(some_param: str) -> None:
    time.sleep(0.5)

    mydata.iam = f"{threading.get_ident()}, {threading.current_thread().name}"

    print(", ".join([
        f"did it: {some_param}",
        f"thread id: {threading.get_ident()}",
        f"thread name: {threading.current_thread().name}"]))

    do_something()


thread1 = threading.Thread(target=do_it, args=('message a',), name="thread a")
thread1.start()

thread2 = threading.Thread(target=do_it, args=('message b',), name="thread b")
thread2.start()

print(f"active threads: {threading.active_count()}")

thread1.join()
thread2.join()

print("done")