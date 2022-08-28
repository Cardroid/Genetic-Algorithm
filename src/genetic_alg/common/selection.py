from copy import deepcopy

from genetic_alg import log
from genetic_alg.model.gene import Gene
from genetic_alg.model.genepool import GenePool


def rank(genepool: GenePool, end_rank_ratio: float = 0.1):
    genepool_len = len(genepool)
    end_rank = round(genepool_len * end_rank_ratio)
    if end_rank > genepool_len:
        end_rank = genepool_len

    parents_list = [Gene(deepcopy(g.get_data()), g.gene_rand_func) for g in genepool[:end_rank]]

    if len(parents_list) < 5:
        log.get_logger(rank).warning("선택된 부모 유전자 수가 적습니다. (유전자 풀의 다양성이 떨어질 수 있습니다.)")

    return parents_list
