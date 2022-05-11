from typing import List

import pandas as pd
from colorama import Fore
from datetime import datetime

yellow_arrow = Fore.YELLOW + " > " + Fore.RESET
green_star = "[" + Fore.GREEN + "*" + Fore.RESET + "] "


def result_log(result: pd.DataFrame, columns):
    dt = datetime.now()
    date = dt.strftime('%Y-%m-%d %H:%M:%S')
    columns_names = ",".join(columns)

    log = "[{0}] columns: [{1}], " \
          "accuracy: {2:.4f}, " \
          "precision: {3:.4f}, " \
          "recall: {4:.4f}, " \
          "f1: {5:.4f}, " \
          "peak: {6}," \
          " time: {7:.2f}\n".format(date, columns_names, result.loc[0, "accuracy"],
                                    result.loc[0, "precision"], result.loc[0, "recall"],
                                    result.loc[0, "f1"], read_b(result.loc[0, "peak"]), result.loc[0, "time"])

    file = open('ga.log', 'a')
    file.write(log)
    file.close()


def read_b(x):
    if x < 1024:
        return "{0:.2f} B".format(x)
    elif x < (1024 * 1024):
        return "{0:.2f} KB".format(x/1024)
    elif x < (1024 * 1024 * 1024):
        return "{0:.2f} MB".format(x / (1024 * 1024))
    elif x < (1024 * 1024 * 1024 * 1024):
        return "{0:.2f} GB".format(x / (1024 * 1024 * 1024))


def save_solution(columns):
    file = open("solution.csv", "w")
    file.write(";".join(columns))
    file.close()


def print_stats(result: pd.DataFrame):
    print("\n\n == Statystyki == \n")
    print(yellow_arrow + "Accuracy: {0:.4f}".format(result.loc[0, 'accuracy']))
    print(yellow_arrow + "Precision score: {0:.4f}".format(result.loc[0, 'precision']))
    print(yellow_arrow + "Recall score: {0:.4f}".format(result.loc[0, 'recall']))
    print(yellow_arrow + "f1 score: {0:.4f}".format(result.loc[0, 'f1']))

    print("\n ===================================== \n")

    print(yellow_arrow + "Czas procesu: {0:.2f} s".format(result.loc[0, 'time']))
    print(yellow_arrow + "Największe zużycie pamięci {0}".format(read_b(result.loc[0, 'peak'])))
