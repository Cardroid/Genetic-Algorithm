import os
from pprint import pformat
import random
from time import time
from typing import Callable

from tqdm import tqdm

from genetic_alg import log
from genetic_alg.model.gene import Gene
from genetic_alg.model.genepool import GenePool
from genetic_alg.common import selection, crossover


def main(**kwargs):
    assert "input" in kwargs and os.path.isfile(kwargs["input"]), "데이터 파일이 존재하지 않습니다."

    result = {}

    data_filepath = kwargs["input"]
    use_setup = kwargs.get("use_setup", True)
    use_graph = kwargs.get("use_graph", True)

    logger = log.get_logger(main)

    if use_graph:
        logger.debug("그래프 시각화를 사용합니다.")

    logger.info("데이터 파일 로드 중...")

    with open(data_filepath, "r", encoding="utf-8") as f:
        dest_line, target_line, *_ = f.readlines()

    try:
        dest_list = [float(d) for d in dest_line.split(" ")]
        target_list = [int(t) for t in target_line.split(" ")]
    except:
        logger.error("데이터 파싱에 실패했습니다.")
        return

    if len(dest_list) == 0 or len(target_list) == 0:
        logger.error("누락된 데이터가 존재합니다.")
        return

    if sum(dest_list) != 1.0:
        logger.warning(f"분배 비율의 합이 1 이 아닙니다.")

    dest_list_len = len(dest_list)
    target_list_len = len(target_list)
    target_list_sum = sum(target_list)
    answer_list = [target_list_sum * dest for dest in dest_list]
    logger.info(f"분배 수: [{dest_list_len}], 분배 항목 수: [{target_list_len}]")

    # Setup
    settings = {}

    settings["gene_count"] = dest_list_len * 20
    if settings["gene_count"] > 300:
        settings["gene_count"] = 300

    settings["epoch"] = settings["gene_count"] * target_list_len

    settings["mutation_ratio"] = 0.05
    settings["target_fitness"] = 0

    if use_setup:
        result["time_offset"] = time()
        tqdm.write("사전 설정을 시작합니다. 입력이 비어있을 경우 [기본값]으로 설정됩니다.")

        def try_input(converter: Callable, msg: str, default=None):
            while True:
                value = input(msg)

                if default != None and value == "":
                    tqdm.write(f"기본값 [{default}]이 적용되었습니다.")
                    return default

                try:
                    parsed_value = converter(value)
                except:
                    tqdm.write(f"[{value}]는 올바른 값이 아닙니다. 다시 입력해주세요.")
                else:
                    return parsed_value

        settings["epoch"] = try_input(int, f"중단할 세대을 입력해주세요 (int) [{settings['epoch']}]: ", settings["epoch"])
        settings["target_fitness"] = try_input(float, f"목표 적합도를 입력해주세요 (0일 경우, 적합도 종료조건이 비활성화 됩니다) (float) [{settings['target_fitness']}]: ", settings["target_fitness"])
        settings["gene_count"] = try_input(int, f"유전자 수를 입력해주세요 (int) [{settings['gene_count']}]: ", settings["gene_count"])
        settings["mutation_ratio"] = try_input(float, f"돌연변이 비율을 입력해주세요 (float) [{settings['mutation_ratio']}]: ", settings["mutation_ratio"])

        result["time_offset"] = time() - result["time_offset"]

    logger.info(f"사전 설정이 완료되었습니다.\nSettings: {pformat(settings)}")
    result["settings"] = settings

    genepool = GenePool()
    gene_rand_func = lambda: random.randint(0, dest_list_len - 1)
    genepool.add_genes([Gene([gene_rand_func() for _ in range(target_list_len)], gene_rand_func) for _ in range(settings["gene_count"])])

    logger.info(f"초기화가 완료되었습니다.")

    def calculate_fitness(gene: Gene):
        gene_data = gene.get_data()

        gene_answer_list = [0 for _ in range(len(answer_list))]

        total_error = 0
        for target_idx, dest_idx in enumerate(gene_data):
            gene_answer_list[dest_idx] += target_list[target_idx]

        for dest_idx, dest_answer in enumerate(answer_list):
            total_error += abs(dest_answer - gene_answer_list[dest_idx])

        return total_error

    zfill_len = len(str(settings["epoch"]))
    for e_idx in tqdm(range(settings["epoch"]), leave=False):
        genepool.fitness_calc(calculate_fitness)
        if e_idx % 100 == 99:
            logger.info(
                (
                    f"[{str(e_idx + 1).zfill(zfill_len)} 세대] "
                    f"최고 적합도: [{round(genepool.best_fitness)}] "
                    f"중앙 적합도: [{round(genepool.median_fitness)}] "
                    f"평균 적합도: [{round(genepool.average_fitness)}] "
                    f"최저 적합도: [{round(genepool.worst_fitness)}]\n"
                    # "상위 유전자: " + str(genepool[0])
                    "상위 유전자: " + "\n상위 유전자: ".join([str(g) for g in genepool[:3]])
                )
            )

        genepool.mutation(settings["mutation_ratio"])
        genepool.next_generation(selection.rank, crossover.two_point_crossover)

    gene_answer_list = [[] for _ in range(len(answer_list))]
    for target_idx, dest_idx in enumerate(genepool[0].get_data()):
        gene_answer_list[dest_idx].append(target_list[target_idx])

    logger.info(
        (
            f"[결과] "
            f"최고 적합도: [{round(genepool.best_fitness)}] "
            f"중앙 적합도: [{round(genepool.median_fitness)}] "
            f"평균 적합도: [{round(genepool.average_fitness)}] "
            f"최저 적합도: [{round(genepool.worst_fitness)}]\n"
            "상위 유전자: " + str(genepool[0])
        )
    )

    result_msg = ["[최종정리]"]
    gene_answer_list_str_len = len(str(len(gene_answer_list)))
    for idx, divide in enumerate(gene_answer_list):
        result_msg.append(f"[{str(idx + 1).zfill(gene_answer_list_str_len)}]번 합계: [{sum(divide)}] 분배목록: [" + ",".join([str(d) for d in divide]) + "]")
    logger.info("\n".join(result_msg))

    result["result"] = gene_answer_list

    return result


MODE_PROPERTY = {
    "desc": "분배 문제를 해결합니다. (기본 모드)",
    "req_desc": "데이터 파일의 첫 번째 줄에 분배 개수 및 배율, 두 번째 줄에 분배 해야하는 수를 작성해주세요. (띄어쓰기로 구분)",
    "func": main,
}
