import threading
import queue


class LockedIterator:
    def __init__(self, it):
        self._lock = threading.Lock()
        self._it = it.__iter__()

    def __iter__(self):
        return self

    def __next__(self):
        with self._lock:
            return next(self._it)


locked_it = LockedIterator((range(100)))

it = iter(range(100))
num_worker_threads = 3


def run_thread(locked_it):
    def _work():
        while 1:
            try:
                tmp = next(locked_it)
                print(tmp * 2, end="\n")
            except StopIteration:
                break

    threads = [threading.Thread(target=_work) for i in range(num_worker_threads)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()


def run_queue(it):
    def _producer():
        while 1:
            while not q.full():
                try:
                    q.put(next(it))
                except StopIteration:
                    break

    def _consumer():
        while 1:
            tmp = q.get()
            print(tmp * 2, end="\n")
            q.task_done()

    buffer_size = 10
    q = queue.Queue(buffer_size)
    t = threading.Thread(target=_producer)
    t.setDaemon(True)
    t.start()

    for i in range(num_worker_threads):
        t = threading.Thread(target=_consumer)
        t.setDaemon(True)
        t.start()

    q.join()


if __name__ == "__main__":
    import timeit

    print(timeit.timeit("run_queue(it)", globals=globals(), number=1))
    print(timeit.timeit("run_thread(locked_it)", globals=globals(), number=1))
