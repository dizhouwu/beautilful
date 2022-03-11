import pandas as pd
import numpy as np
import tracemalloc
from joblib import Parallel, delayed

tracemalloc.start()
data = np.random.random((1000000, 600))
data = pd.DataFrame(data)


_, peak = tracemalloc.get_traced_memory()
print(peak)


def foo(data, i):
    print(data.iloc[0, 0])




results = Parallel(n_jobs=4)(delayed(foo)(data, i) for i in range(4))

_, peak = tracemalloc.get_traced_memory()
print(peak)
