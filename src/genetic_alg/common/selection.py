from copy import deepcopy
import random

from genetic_alg import log
from genetic_alg.model.gene import Gene
from genetic_alg.model.genepool import GenePool


def method_helper(original_function, *args, **kwargs):
    def wrapper(genepool):
        return original_function(genepool, *args, **kwargs)

    return wrapper


def rank(genepool: GenePool, best_rank_ratio: float = 0.5):
    genepool_len = len(genepool)
    best_rank_end_index = round(genepool_len * best_rank_ratio)
    if best_rank_end_index > genepool_len - 1:
        best_rank_end_index = genepool_len - 1

    parents_list = [Gene(deepcopy(g.get_data()), g.gene_rand_func) for g in genepool[:best_rank_end_index]]

    if len(parents_list) < 10:
        log.get_logger(rank).warning("선택된 부모 유전자 수가 적습니다. (유전자 풀의 다양성이 떨어질 수 있습니다.)")

    return parents_list


def heuristic_rank(genepool: GenePool, best_rank_ratio: float = 0.1, randoom_sample_cutoff_ratio: float = 0.4, randoom_sample_k: int = 20):
    parents_list = rank(genepool, best_rank_ratio)

    genepool_len = len(genepool)
    random_rank_end_index = round(genepool_len * (1.0 - randoom_sample_cutoff_ratio))
    if random_rank_end_index > genepool_len - randoom_sample_k - 1:
        random_rank_end_index = genepool_len - randoom_sample_k - 1

    parents_list.extend([Gene(deepcopy(g.get_data()), g.gene_rand_func) for g in random.sample(genepool[random_rank_end_index:], k=randoom_sample_k)])

    return parents_list
