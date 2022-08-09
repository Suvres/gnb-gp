import pandas as pd
import numpy as np
from scipy.stats import spearmanr


dataset = pd.read_csv("../../days/Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv")
x = dataset[list(dataset.columns[:-1])]
y = dataset[dataset.columns[-1]]

x = x.replace([np.inf, -np.inf], np.nan)
x = x.fillna(0)

def corr_spearman_criteria(y, X, absolute_values=False,
                           alpha=0.05, return_pval=False):
    corr_pval = {}
    corr_val = {}

    for column in X.columns:
        if spearmanr(y, X[column])[1] > 0.05:
            corr_pval[column] = "Zmienna jest nieskorelowana, p-val: {:.3f}".format(spearmanr(y, X[column])[1])
        else:
            corr_pval[column] = "Zmienna jest skorelowana, p-val: {:.3f}".format(spearmanr(y, X[column])[1])

        if absolute_values:
            corr_val[column] = round(abs(spearmanr(y, X[column])[0]), 3)
        else:
            corr_val[column] = round(spearmanr(y, X[column])[0], 3)
        corr_sorted = {k: v for k, v in sorted(corr_val.items(),
                                               key=lambda item: item[1],
                                               reverse=True)}
    if return_pval:
        return corr_pval
    else:
        return corr_sorted


i = 0
for k in corr_spearman_criteria(y, x, absolute_values=True):
    print(k)
    i += 1
    if i == 41:
        break