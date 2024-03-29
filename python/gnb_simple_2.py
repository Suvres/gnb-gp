"""
Operacja wykorzystująca GNB (Gaussian Naive Bayes), aby na podstawie stworzonego modelu posiadające pola BENIGN i
inne, które są zamieniane na 1 i 0

 TODO: dodać do inżynierki algorytm GNB oraz ładny schemat i opis

"""
import numpy as np
import pandas as pd
from gnb import simple_gnb
from helper import yellow_arrow, result_log, read_b, print_stats

dataset = pd.read_csv("../../days/Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv")
dataset_test = pd.read_csv("../../days/Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv")
cols = pd.read_csv("./sol_spear.csv")

result = simple_gnb(dataset=dataset[cols.columns], dataset_test=dataset_test[cols.columns])

print_stats(result)
