from typing import List

import pandas as pd
from colorama import Fore
from datetime import datetime

yellow_arrow = Fore.YELLOW + " > " + Fore.RESET
green_star = "[" + Fore.GREEN + "*" + Fore.RESET + "] "


def result_log(result: pd.DataFrame, columns):
    dt = datetime.now()
    date = dt.strftime('%Y-%m-%d %H:%M:%S;%f')
    columns_names = ",".join(columns)

    log = "[{0}] columns: [{1}], " \
          "accuracy: {2:.4f}, " \
          "precision: {3:.4f}, " \
          "recall: {4:.4f}, " \
          "f1: {5:.4f}, " \
          "peak: {5:.4f}," \
          " time: {6:.2f}\n".format(date, columns_names, result.loc[0, "accuracy"],
                                    result.loc[0, "precision"], result.loc[0, "recall"],
                                    result.loc[0, "f1"], result.loc[0, "peak"], result.loc[0, "time"])

    file = open('ga.log', 'a')
    file.write(log)
    file.close()
