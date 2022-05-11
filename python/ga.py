"""
    Algorytm Genetyczny

    TODO: Opis GA do inżynierki

"""

import time
from functools import partial
from random import choices, randint, randrange, random
from typing import List, Callable, Tuple
import pandas as pd
import numpy as np
from helper import result_log

from gnb import simple_gnb

Genome = List[int]
Population = List[Genome]
Columns = np.array

FitnessFunc = Callable[[Genome], int]
PopulateFunc = Callable[[], Population]
SelectionFunc = Callable[[Population, List[float]], Tuple[Genome, Genome]]
PopulationSortedFunc = Callable[[Population, FitnessFunc], Tuple[Population, List[float]]]
CrossoverFunc = Callable[[Genome, Genome], Tuple[Genome, Genome]]
MutationFunc = Callable[[Genome], Genome]

dataset = pd.read_csv("../../dane_ids/train.csv")
dataset_test = pd.read_csv("../../dane_ids/test.csv")

columns = dataset.columns.tolist()
label_column = columns[-1]
columns = np.array(columns[:-1])
columns_length = len(columns)


# columns = dataset.columns.tolist()
# columns = columns[0:3] + [columns[-1]]

# Generuje genotyp o długości wynoszącej ilość kolumn w tabeli
def generate_genome(columns: Columns) -> Genome:
    return choices([0, 1], k=len(columns))


# Generuje populacje składającą się z wielu genów
def generate_population(size: int, columns: Columns) -> Population:
    return [generate_genome(columns) for _ in range(size)]


# Krzyżowanie 1 punktowe
def single_point_crossover(a: Genome, b: Genome) -> Tuple[Genome, Genome]:
    if len(a) != len(b):
        raise ValueError("Musi być ta sama długość genomów")

    length = len(a)
    if length < 2:
        return a, b

    p = randint(1, length - 1)
    return a[0:p] + b[p:], b[0:p] + a[p:]


# Mutacja genomów dla "n" indeksów
def mutation(genome: Genome, num: int = 1, probability: float = 0.5) -> Genome:
    for _ in range(num):
        index = randrange(len(genome))
        genome[index] = genome[index] if random() > probability else abs(genome[index] - 1)

    return genome


# Zwracanie wyniku jako kolumn dla tabeli
def genome_to_columns(genome: Genome, columns: Columns) -> Columns:
    result = []

    for i in range(len(columns)):
        if genome[i] == 1:
            result += [columns[i]]

    return result


# Zwraca parę obiektów dla wag wygenerowanych za pomocą metody fitness
def selection_pairs(population: Population, weights: List[float]) -> Population:
    return choices(
        population=population,
        weights=weights,
        k=2
    )


# Fitness
# Poprawić, aby nie było samo F1
def fitness(genome: Genome, columns: Columns, dataset: pd.DataFrame, dataset_test: pd.DataFrame) -> int:
    if len(genome) != len(columns):
        raise ValueError("Musi być ta sama długość")

    logical_genome = [i == 1 for i in genome]

    tmp_columns = np.append(columns[logical_genome], label_column)
    tmp_dataset = dataset[tmp_columns]
    tmp_dataset_test = dataset_test[tmp_columns]

    result = simple_gnb(dataset=tmp_dataset, dataset_test=tmp_dataset_test)

    result_log(result=result, columns=tmp_columns)
    return result.loc[0, "f1"]


def population_sorted(population: Population, fitness_func: FitnessFunc) -> Tuple[Population, List[float]]:
    weights = []
    for i in range(len(population)):
        weights.append(fitness_func(population[i]))

    for i in range(len(weights)):
        for j in range(len(weights)):
            if weights[j] < weights[i]:
                weights[j], weights[i] = weights[i], weights[j]
                population[j], population[i] = population[i], population[j]

    return population, weights


def run_evolution(
        populate_func: PopulateFunc,
        fitness_func: FitnessFunc,
        selection_func: SelectionFunc = selection_pairs,
        crossover_fun: CrossoverFunc = single_point_crossover,
        mutation_fun: MutationFunc = mutation,
        population_sorted_fun: PopulationSortedFunc = population_sorted,
        generation_limit: int = 100,
        limit: float = 0.9
) -> Tuple[Population, int]:
    population = populate_func()

    for i in range(generation_limit):
        print("\n\n======= Populacja: {0} ========\n\n".format(i))
        population, weights = population_sorted_fun(population, fitness_func)

        if weights[0] > limit:
            break

        next_generation = population[0:2]

        for j in range(int(len(population) / 2) - 1):
            parents = selection_func(population, weights)
            offspring_a, offspring_b = crossover_fun(parents[0], parents[1])

            offspring_a = mutation_fun(offspring_a)
            offspring_b = mutation_fun(offspring_b)

            next_generation += [offspring_a, offspring_b]

        population = next_generation

    population, weights = population_sorted_fun(population, fitness_func)

    return population, i



start = time.time()
population, generations = run_evolution(
    populate_func=partial(
        generate_population, size=10, columns=columns
    ),
    fitness_func=partial(
        fitness, columns=columns, dataset=dataset, dataset_test=dataset_test
    ),
    generation_limit=100,
)
end = time.time()

print(f"number of generations:  {generations}")
print(f"best solution:  {genome_to_columns(population[0], columns)}")
print(f"Time:  {end - start}s")

result = fitness(population[0], columns=columns, dataset=dataset, dataset_test=dataset_test)
print("\n{0:.4f}\n".format(result))