from abc import ABCMeta, abstractmethod
from copy import deepcopy
from pprint import pformat
from typing import Any, Callable, List, Union


class BaseClass(metaclass=ABCMeta):
    @abstractmethod
    def _get_data(self) -> Union[List, Any]:
        pass

    def get_data(self) -> Union[List, Any]:
        return self._get_data()

    def deep_clone(self):
        return deepcopy(self)

    def __str__(self) -> str:
        data = self.get_data()
        if data != None:
            return pformat(data)
        else:
            return super().__str__()

    def __repr__(self) -> str:
        data = self.get_data()
        if data != None:
            return pformat(data)
        else:
            return super().__repr__()


class BaseGene(BaseClass):
    def __init__(self, init_data: Union[List[int], None] = None) -> None:
        super().__init__()
        if isinstance(init_data, list):
            self._data = init_data
        else:
            self._data = []
        self._fitness = -1

    @property
    def fitness(self):
        return self._fitness

    @abstractmethod
    def fitness_calc(self, calc_func: Callable, data):
        pass

    def _get_data(self) -> List[int]:
        return self._data

    def __len__(self):
        return len(self._data)

    def __setitem__(self, index, data: int):
        self._data[index] = data

    def __getitem__(self, index) -> int:
        return self._data[index]


class BaseGenePool(BaseClass):
    def __init__(self) -> None:
        super().__init__()
        self._data = []
        self._best_fitness = -1
        self._median_fitness = -1
        self._average_fitness = -1
        self._worst_fitness = -1

    @property
    def best_fitness(self):
        return self._best_fitness

    @property
    def median_fitness(self):
        return self._median_fitness

    @property
    def average_fitness(self):
        return self._average_fitness

    @property
    def worst_fitness(self):
        return self._worst_fitness

    @abstractmethod
    def fitness_calc(self, calc_func: Callable, data):
        pass

    @abstractmethod
    def next_generation(self, selector: Callable, crossover: Callable):
        pass

    @abstractmethod
    def mutation(self, ratio):
        pass

    def _get_data(self) -> List[BaseGene]:
        return self._data

    def add_gene(self, gene: BaseGene):
        self._data.append(gene)

    def add_genes(self, gene: List[BaseGene]):
        self._data.extend(gene)

    def __len__(self):
        return len(self._data)

    def __setitem__(self, index, gene: BaseGene):
        self._data[index] = gene

    def __getitem__(self, index) -> BaseGene:
        return self._data[index]

    def __delitem__(self, index) -> BaseGene:
        del self._data[index]
