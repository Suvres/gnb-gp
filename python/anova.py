from sklearn.feature_selection import SelectKBest, f_classif
import pandas as pd
import numpy as np


dataset = pd.read_csv("../../days/Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv")
X = dataset[list(dataset.columns[:-1])]
y = dataset[dataset.columns[-1]]

X = X.replace([np.inf, -np.inf], np.nan)
X = X.fillna(0)

#przekształcenie
skb = SelectKBest(score_func=f_classif, k=41) #wybieramy 3 zmienne
skb.fit(X,y)
X_new = skb.transform(X) #nasz nowy df z wybranymi zmiennymi objaśniającymi

print(X.shape,'\n', X_new.shape)
columns = X.columns[skb.get_support()]
for i in columns:
    print(i)