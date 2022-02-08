import itertools
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

flatten_iter = itertools.chain.from_iterable
def get_factors(n):
    return sorted(list((flatten_iter((i, n//i) 
                for i in range(1, int(n**0.5)+1) if n % i == 0))))


def get_row_cnt_for_csv(filename):
    if filename.endswith(".gz"):
        import gzip
        with gzip.open(filename) as f:
            cnt = sum(1 for _ in f)
            return cnt
    else:
        with open(filename) as f:
            cnt = sum(1 for _ in f)
            return cnt
        
row_cnt = get_row_cnt_for_csv("test.csv.gz")


factors = get_factors(row_cnt)

for factor in factors[::-1]:
    if factor < 1_000_000:
        chunksize = factor
        break
        

creds = {"user": "user",
         "password": "pwd",
         "account":'east-us-2.azure',
         "warehouse": "wh",
         "database": "db", 
         "schema": "schema"}

def get_sf_conn(creds):
    conn = snowflake.connector.connect(**creds)
    return conn

data = LockedIterator(pd.read_csv("test.csv.gz", chunksize=chunksize))

def read():
    sf_conn = get_sf_conn(creds)
    while 1:
        global data
        try:
            tmp = next(data)
            write_pandas(sf_conn, tmp, "your_table", "your_db", "your_schema")
        except:
            break
    
threads =[threading.Thread(target=read) for i in range(20)]
for t in threads:
    t.start()
for t in threads:
    t.join()
