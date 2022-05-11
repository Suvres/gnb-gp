import pandas as pd
from sklearn.naive_bayes import GaussianNB
from sklearn import metrics
import time
import tracemalloc
import numpy as np
from helper import yellow_arrow, green_star, read_b


def simple_gnb(dataset: pd.DataFrame, dataset_test: pd.DataFrame) -> pd.DataFrame:
    """
    Metoda wykorzystująca moduł sklearn, aby za pomocą Gaussian Naive Bayes wytrenować model za pomocą dataset.
    Następnie za pomocą dataset_test, przetestować model. Metoda zwraca wszystkie parametry związane z obliczeniami:
    [dokładność, precyzję, czułość, ocena, największa wykorzystana pamięć, czas trwania]

    :param dataset:
    :param dataset_test:
    :return:
    """

    # --- Wstępne informacje
    print("\n")
    print("=============================")
    print("=== Klasyfikowanie danych ===")
    print("=============================\n")

    print("\n == Wielkość plików dataset == \n")
    dataSize = read_b(dataset.memory_usage(index=False, deep=True).sum())
    dataTestSize = read_b(dataset_test.memory_usage(index=False, deep=True).sum())

    print(yellow_arrow + "Dane dla modelu")
    print("\t" + yellow_arrow + "Rozmiar: {0}".format(dataSize))
    print("\t" + yellow_arrow + "Ilość wierszy: {0}".format(dataset.shape[0]))

    print(yellow_arrow + "Dane testowe")
    print("\t" + yellow_arrow + "Rozmiar: {0}".format(dataTestSize))
    print("\t" + yellow_arrow + "Ilość wierszy: {0}".format(dataset_test.shape[0]))

    # --- Proces GNB --
    print("\n\n == Proces == \n")

    tracemalloc.start()
    start = time.time()

    # --- Usunięcie NaN za pomocą 0
    print(green_star + "Zamiana Nan oraz Inf na 0")

    dataset = dataset.replace([np.inf, -np.inf], np.nan)
    dataset = dataset.fillna(0)

    dataset_test = dataset_test.replace([np.inf, -np.inf], np.nan)
    dataset_test = dataset_test.fillna(0)

    # --- Zamiana etykiet na 1 i 0
    print(green_star + "Obróbka danych")

    dataset.loc[:, " Label"] = [1 if i == "BENIGN" else 0 for i in dataset.loc[:, " Label"]]
    dataset_test.loc[:, " Label"] = [1 if i == "BENIGN" else 0 for i in dataset_test.loc[:, " Label"]]

    # --- Przygotowanie X i Y gdzie X to dane, a Y to etykiety
    x = dataset.drop([" Label"], axis=1)
    y = dataset.loc[:, " Label"].values

    x_test = dataset_test.drop([" Label"], axis=1)
    y_test = dataset_test.loc[:, " Label"].values

    x.replace([np.inf, -np.inf], np.nan)
    x_test.replace([np.inf, -np.inf], np.nan)

    x = x.fillna(0)
    x_test = x_test.fillna(0)

    # ---Tworzenie GaussianNB oraz uczenie
    print(green_star + "Trenowanie danych")

    nb = GaussianNB()
    nb.fit(x, y)

    # --- Obliczenie predykcji
    print(green_star + "Obliczanie predykcji")
    y_pred = nb.predict(x_test)

    # --- Obliczanie metryk
    print(green_star + "Obliczanie metryk")

    acc = metrics.accuracy_score(y_test, y_pred)
    prec = metrics.precision_score(y_test, y_pred)
    rec = metrics.recall_score(y_test, y_pred)
    f1 = 2 * prec * rec / (rec + prec)

    end = time.time()

    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    # --- Zakończenie procesu
    print(green_star + "Zakończenie procesu")

    return pd.DataFrame({
        'accuracy': [acc],
        'precision': [prec],
        'recall': [rec],
        'f1': [f1],
        'peak': [peak],
        'time': [end - start]
    }, dtype=np.float)
