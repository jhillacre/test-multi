import ctypes
import multiprocessing
import random
import sys
from time import sleep


def init_worker(counter):
    global _worker_id

    with counter.get_lock():
        counter.value += 1
        _worker_id = counter.value

def do_work(x):
    print(_worker_id, 'starting', x)
    sleep(random.uniform(1, 3))
    print(_worker_id, 'ending', x)
    return x, sys.stdin.closed, sys.stdout.closed, sys.stderr.closed


if __name__ == '__main__':
    counter = multiprocessing.Value(ctypes.c_int, 0)
    pool = multiprocessing.Pool(
        processes=8,
        initializer=init_worker,
        initargs=[counter])
    test_results = pool.imap_unordered(do_work, (
        x for x in range(32)
    ))

    while True:
        try:
            print('done', test_results.next(timeout=0.1))
        except multiprocessing.TimeoutError:
            continue
        except StopIteration:
            pool.close()
            break

    pool.join()
