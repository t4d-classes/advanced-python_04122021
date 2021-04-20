from typing import Generator
import itertools
import time
import threading

def fibonacci() -> Generator[int, None, None]:
    """ generate an infinite fibonacci sequence """

    num_1 = 0
    num_2 = 1

    yield num_1
    yield num_2

    while True:

        next_num = num_1 + num_2
        yield next_num
        num_1 = num_2
        num_2 = next_num

for num in itertools.islice(fibonacci(), 0, 10):
    print(num)