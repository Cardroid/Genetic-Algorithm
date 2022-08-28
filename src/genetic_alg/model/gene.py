from typing import Callable, List

from genetic_alg.model.abc import BaseGene


class Gene(BaseGene):
    def __init__(self, init_data: List[int], gene_rand_func: Callable) -> None:
        super().__init__(init_data)
        self.__gene_rand_func = gene_rand_func

    @property
    def gene_rand_func(self):
        return self.__gene_rand_func

    def fitness_calc(self, calc_func: Callable):
        self._fitness = calc_func(self)
        return self._fitness

    def mutation(self):
        for idx in range(len(self._data)):
            self._data[idx] = self.__gene_rand_func()

    def __str__(self) -> str:
        return ",".join([str(d) for d in self._data])

    def __repr__(self) -> str:
        return ",".join([str(d) for d in self._data])
