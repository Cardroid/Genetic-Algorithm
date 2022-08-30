from typing import Callable, List

from genetic_alg.model.abc import BaseGene


class Gene(BaseGene):
    def __init__(self, init_data: List[int], mutation_func: Callable) -> None:
        super().__init__(init_data)
        self.__mutation_func = mutation_func

    @property
    def mutation_func(self):
        return self.__mutation_func

    def fitness_calc(self, calc_func: Callable):
        self._fitness = calc_func(self)
        return self._fitness

    def mutation(self):
        self.__mutation_func(self._data)

    def __str__(self) -> str:
        return ",".join([str(d) for d in self._data])

    def __repr__(self) -> str:
        return ",".join([str(d) for d in self._data])
