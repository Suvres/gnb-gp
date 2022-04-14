import pandas as pd
from read_b import read_b
from gnb import simple_gnb
from helper import yellow_arrow

dataset = pd.read_csv("../../dane_ids/train.csv")
dataset_test = pd.read_csv("../../dane_ids/test.csv")

result = simple_gnb(dataset=dataset, dataset_test=dataset_test)

print("\n\n == Statystyki == \n")
print(yellow_arrow + "Accuracy: {0:.4f}".format(result.loc[0, 'accuracy']))
print(yellow_arrow + "Precision score: {0:.4f}".format(result.loc[0, 'precision']))
print(yellow_arrow + "Recall score: {0:.4f}".format(result.loc[0, 'recall']))
print(yellow_arrow + "f1 score: {0:.4f}".format(result.loc[0, 'f1']))

print("\n ===================================== \n")

print(yellow_arrow + "Czas procesu: {0:.2f} s".format(result.loc[0, 'time']))
print(yellow_arrow + "Największe zużycie pamięci {0}".format(read_b(result.loc[0, 'peak'])))
