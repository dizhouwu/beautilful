import itertools
import threading
import pandas as pd
import snowflake

class LockedIterator:
    def __init__(self, it):
        self._lock = threading.Lock()
        self._it = it.__iter__()

    def __iter__(self):
        return self

    def __next__(self):
        with self._lock:
            return next(self._it)


def get_factors(n):
    flatten_iter = itertools.chain.from_iterable
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
        
def get_chunksize(factors):
    for factor in factors[::-1]:
        if factor < 1_000_000:
            chunksize = factor
            return chunksize
        
def get_sf_conn(creds):
    conn = snowflake.connector.connect(**creds)
    return conn

def upload_csv_to_sf(filename, table, db, schema):
    creds = {"user": "user",
         "password": "password",
         "account":'account',
         "warehouse": "warehouse",
         "database": "database", 
         "schema": "schema"}
    
    row_cnt = get_row_cnt_for_csv(filename)
    factors = get_factors(row_cnt)
    chunksize = get_chunksize(factors)
    
    data = LockedIterator(pd.read_csv(filename, chunksize=chunksize))
    
    def _upload():
        sf_conn = get_sf_conn(creds)
        while 1:
            try:
                tmp = next(data)
                write_pandas(sf_conn, tmp, table, db, schema)
            except:
                break
                
    threads =[threading.Thread(target=_upload) for i in range(20)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
