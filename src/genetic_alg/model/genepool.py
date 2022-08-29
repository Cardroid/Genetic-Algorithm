import random
from typing import Callable

from genetic_alg.model.abc import BaseGenePool


class GenePool(BaseGenePool):
    def __init__(self) -> None:
        super().__init__()

    def fitness_calc(self, calc_func: Callable):  # 적응도 계산
        total_fitness = 0
        for gene in self._data:
            fitness = gene.fitness_calc(calc_func)
            total_fitness += fitness

        self._data.sort(key=lambda g: g.fitness)

        average_fitness = total_fitness / len(self._data)

        self._best_fitness = self[0].fitness
        self._median_fitness = self[round(len(self) / 2)].fitness
        self._average_fitness = average_fitness
        self._worst_fitness = self[-1].fitness

        return (self._best_fitness, self._median_fitness, average_fitness, self._worst_fitness)

    def next_generation(self, selector: Callable, crossover: Callable):  # 다음 세대
        assert len(self._data) % 2 == 0, "유전자 수가 짝수가 아닙니다."

        parents_pair_list = selector(self)

        crossover(parents_pair_list, self, self[0])

    def mutation(self, ratio):  # 돌연변이
        mutation_count = round(len(self) * ratio)

        if ratio > 0 and mutation_count < 1:
            mutation_count = 1

        for gene in random.sample(self[1:], k=mutation_count):
            gene.mutation()
