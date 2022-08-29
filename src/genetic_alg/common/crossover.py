import random
from typing import List, Tuple

from genetic_alg.model.gene import Gene
from genetic_alg.model.genepool import GenePool


def single_point_crossover(gene_list: List[Tuple[Gene, Gene]], genepool: GenePool, elite_gene: Gene):
    gene_len = len(gene_list[0])
    genepool_len = len(genepool)

    crossover_idx = 0
    while crossover_idx < genepool_len:
        child_gene = genepool[crossover_idx]

        if child_gene is elite_gene:
            crossover_idx += 1
            continue

        x, y = random.sample(gene_list, k=2)
        # 000000|0000000000000000000
        cut_line = random.randint(1, gene_len - 2)

        gene_idx = 0
        for d in x[:cut_line]:
            child_gene[gene_idx] = d
            gene_idx += 1

        for d in y[cut_line:]:
            child_gene[gene_idx] = d
            gene_idx += 1

        crossover_idx += 1


def two_point_crossover(gene_list: List[Tuple[Gene, Gene]], genepool: GenePool, elite_gene: Gene):
    gene_len = len(gene_list[0])
    genepool_len = len(genepool)

    crossover_idx = 0
    while crossover_idx < genepool_len:
        child_gene = genepool[crossover_idx]

        if child_gene is elite_gene:
            crossover_idx += 1
            continue

        x, y = random.sample(gene_list, k=2)
        # 000000|0000000000000000000
        l_cut_line = random.randint(1, gene_len - 3)
        # 000000|0000000000000|00000
        r_cut_line = random.randint(l_cut_line, gene_len - 2)

        gene_idx = 0
        for d in x[:l_cut_line]:
            child_gene[gene_idx] = d
            gene_idx += 1

        for d in y[l_cut_line:r_cut_line]:
            child_gene[gene_idx] = d
            gene_idx += 1

        for d in x[r_cut_line:]:
            child_gene[gene_idx] = d
            gene_idx += 1

        crossover_idx += 1


def uniform_crossover(gene_list: List[Tuple[Gene, Gene]], genepool: GenePool, elite_gene: Gene):
    pass
