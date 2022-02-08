import threading
import pandas as pd

class LockedIterator:
    def __init__(self, it):
        self._lock = threading.Lock()
        self._it = it.__iter__()

    def __iter__(self):
        return self

    def __next__(self):
        with self._lock:
            return next(self._it)
          
data = LockedIterator(pd.read_csv(filename,chunksize=chunksize))
def read():
    sf_conn = get_sf_conn(creds)
    while 1:
        global data
        try:
            next(data)
            write_pandas(sf_conn, tmp, "your_table", "your_database", "your_schema")
        except:
            break
    
threads =[ threading.Thread(target=read) for i in range(20)]
for t in threads:
    t.start()
for t in threads:
    t.join()
