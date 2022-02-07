import itertools
import json
import numpy as np
import pandas as pd
from sklearn.decomposition import NMF
import sys
import time

def get_clusters_from_H(H):
    """
    For each column in H, identify the sample's cluster based on the
    maximum value in the column. Return a series containing the 
    cluster assignments
    """
    assignments = pd.Series(
        H.apply(
            func = np.argmax,
            axis = 0
        )
    )
    assignments.index = H.columns
    return assignments

N_ITER = 100

MIN_K = 2
MAX_K = 9

EXPR = pd.read_csv(
    sys.argv[1],
    sep = '\t',
    index_col = 0,
    skiprows = 2
).drop(labels = "Description", axis = 1)

TOGETHER_COUNTS = {
    k: pd.DataFrame(
        np.eye(EXPR.shape[1]),
        index = EXPR.columns,
        columns = EXPR.columns
    )
    for k in range(MIN_K, MAX_K+1)
}

np.random.seed(49)
rand_seeds = np.random.randint(2**32 - 1, size = N_ITER)

t0 = time.time()

for k in range(MIN_K, MAX_K+1):
    print(f"Starting k = {k}")
    for i in range(N_ITER):
        print(f"\tStarting iteration {i + 1}")
        decomp = NMF(
            n_components = k,
            solver = 'mu',
            max_iter = 2000,
            random_state = rand_seeds[i],
            beta_loss = "kullback-leibler",
            init = "random"
        )
        
        W = decomp.fit_transform(EXPR)
        H = decomp.components_
        H = pd.DataFrame(H)
        H.columns = EXPR.columns
        
        assignments = get_clusters_from_H(H)
        
        unique_pairs = itertools.combinations(assignments.index, r = 2)
        
        for pair in unique_pairs:
            s1 = pair[0]
            s2 = pair[1]
            
            if assignments[s1] == assignments[s2]:
                TOGETHER_COUNTS[k].loc[s1, s2] += 1
                TOGETHER_COUNTS[k].loc[s2, s1] += 1

t1 = time.time()

res = {
    "file": sys.argv[1],
    "n_iter": N_ITER,
    "min_k": MIN_K,
    "max_k": MAX_K,
    "time": t1 - t0
}

with open(sys.argv[2], 'w') as f:
    f.write(json.dumps(res))
