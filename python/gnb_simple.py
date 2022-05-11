"""
Operacja wykorzystująca GNB (Gaussian Naive Bayes), aby na podstawie stworzonego modelu posiadające pola BENIGN i
inne, które są zamieniane na 1 i 0

 TODO: dodać do inżynierki algorytm GNB oraz ładny schemat i opis

"""
import numpy as np
import pandas as pd
from gnb import simple_gnb
from helper import yellow_arrow, result_log, read_b, print_stats

dataset = pd.read_csv("../../dane_ids/train.csv")
dataset_test = pd.read_csv("../../dane_ids/test.csv")

result = simple_gnb(dataset=dataset, dataset_test=dataset_test)

print_stats(result)
