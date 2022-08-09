import numpy as np
import pandas as pd

dataset = pd.read_csv("../../days/Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv")
dataset.loc[:, " Label"] = [1.0 if i == "BENIGN" else 0.0 for i in dataset.loc[:, " Label"]]

x = dataset[list(dataset.columns[:-1])]
y = dataset[dataset.columns[-1]]


x = x.replace([np.inf, -np.inf], np.nan)
x = x.fillna(0)

x.astype('float')

def corr_criteria(y, X, absolute_values = False):
    corr_dict = {}
    if absolute_values:
        for column in X.columns:
            corr_dict[column]= round(abs(np.corrcoef(y, X[column])[1][0]),3)
    else:
         for column in X.columns:
            corr_dict[column]= round(np.corrcoef(y, X[column])[1][0],3)
    corr_sorted = {k: v for k, v in sorted(corr_dict.items(),
                                           key=lambda item: item[1],
                                           reverse=True)}
    return corr_sorted



i = 0
for k in corr_criteria(y,x, absolute_values = True):
    print(k)
    i += 1
    if i == 41:
        break
