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

        from matplotlib import pyplot as plt
        from matplotlib.animation import FuncAnimation

        figure_counter = 0

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
    target_list_sum_str_len = len(str(target_list_sum))
    answer_list = [target_list_sum * dest for dest in dest_list]
    logger.info(f"분배 수: [{dest_list_len}], 분배 항목 수: [{target_list_len}]")

    # Setup
    settings = {}

    settings["gene_count"] = dest_list_len * 40
    if settings["gene_count"] > 1000:
        settings["gene_count"] = 1000

    settings["epoch"] = round(settings["gene_count"] * target_list_len / 10)

    settings["mutation_ratio"] = 0.2
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

        settings["epoch"] = try_input(int, f"학습 중단 세대을 입력해주세요 (int) [{settings['epoch']}]: ", settings["epoch"])
        settings["target_fitness"] = try_input(float, f"목표 적응도를 입력해주세요 (0일 경우, 적응도 종료조건이 비활성화 됩니다) (float) [{settings['target_fitness']}]: ", settings["target_fitness"])
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

    epoch_str_len = len(str(settings["epoch"]))
    if use_graph:
        x_list, y_best_list, y_average_list = [], [], []

        for gene in genepool:
            gene.fitness_calc(calculate_fitness)

        gene_x_list = [i for i in range(1, len(genepool) + 1)]

        plt.figure(figure_counter, figsize=(16, 8), dpi=80)
        figure_counter += 1
        plt.scatter(gene_x_list, [fit.fitness for fit in genepool])

        plt.xlabel("Gene Number")
        plt.ylabel("Fitness")

        plt.title(f"Init Gene Fitness")
        plt.tight_layout()
        plt.show()

        plt.figure(figure_counter, figsize=(16, 8), dpi=80)
        figure_counter += 1

        e_idx = 0
        is_frame_update_need = [True]

        def animate(i):
            if is_frame_update_need[0]:
                plt.cla()
                plt.scatter(gene_x_list, [fit.fitness for fit in genepool])

                plt.title((f"Epoch {str(e_idx).rjust(epoch_str_len)} ".ljust(20) + f"Best: {round(best_fitness, 3)} ".ljust(20) + f"Avg: {round(genepool.average_fitness, 3)}".ljust(20)))
                plt.xlabel("Gene Number")
                plt.ylabel("Fitness")

                is_frame_update_need[0] = False

        ani = FuncAnimation(plt.gcf(), animate)

        plt.title(f"Epoch {str(e_idx).rjust(epoch_str_len)}")
        plt.xlabel("Gene Number")
        plt.ylabel("Fitness")

        plt.autoscale(enable=True)
        plt.tight_layout()
        plt.show(block=False)

    before_best_fitness = -1
    for e_idx in tqdm(range(settings["epoch"]), leave=False, desc="Generation evolving..."):
        best_fitness, median_fitness, average_fitness, worst_fitness = genepool.fitness_calc(calculate_fitness)

        if use_graph:
            x_list.append(e_idx)
            y_best_list.append(best_fitness)
            # y_median_list.append(median_fitness)
            y_average_list.append(average_fitness)
            # y_worst_list.append(worst_fitness)

            if e_idx % 10 == 0:
                is_frame_update_need[0] = True
                plt.pause(0.06)

        if best_fitness <= settings["target_fitness"]:
            logger.info(f"목표 적응도를 달성하였으므로 자동으로 종료됩니다.")
            break

        # if e_idx % 100 == 99:
        if before_best_fitness != best_fitness:
            before_best_fitness = best_fitness
            logger.info(
                (
                    f"[{str(e_idx + 1).rjust(epoch_str_len)} 세대] "
                    f"최고 적응도: [{round(best_fitness, 1)}] "
                    # f"중앙 적응도: [{round(median_fitness)}] "
                    f"평균 적응도: [{round(average_fitness, 1)}] "
                    f"최저 적응도: [{round(worst_fitness, 1)}]\n"
                    "상위 유전자: " + str(genepool[0])
                    # "상위 유전자: " + "\n상위 유전자: ".join([str(g) for g in genepool[:3]])
                )
            )

        genepool.mutation(settings["mutation_ratio"])
        genepool.next_generation(
            selection.method_helper(
                selection.heuristic_rank,
                best_rank_ratio=0.1,
                randoom_sample_cutoff_ratio=0.4,
                randoom_sample_k=20,
            ),
            crossover.two_point_crossover,
        )

    gene_answer_list = [[] for _ in range(len(answer_list))]
    for target_idx, dest_idx in enumerate(genepool[0].get_data()):
        gene_answer_list[dest_idx].append(target_list[target_idx])

    logger.info(
        (
            f"[결과] "
            f"최고 적응도: [{round(genepool.best_fitness, 1)}] "
            # f"중앙 적응도: [{round(genepool.median_fitness)}] "
            f"평균 적응도: [{round(genepool.average_fitness, 1)}] "
            f"최저 적응도: [{round(genepool.worst_fitness, 1)}]\n"
            "상위 유전자: " + str(genepool[0])
        )
    )

    result_msg = ["[최종정리]"]
    gene_answer_list_str_len = len(str(len(gene_answer_list)))
    for idx, divide in enumerate(gene_answer_list):
        result_msg.append(
            f"[{str(idx + 1).zfill(gene_answer_list_str_len)}]번 "
            f"합계: [{str(divide_sum := sum(divide)).rjust(target_list_sum_str_len)}] "
            f"목표 합계: [{str(answer_list[idx]).rjust(target_list_sum_str_len + 2)}] "
            f"비율: [{str(round((divide_sum / target_list_sum) * 100, 2)).rjust(6)}%] "
            f"목표 비율: [{str(round(dest_list[idx] * 100, 2)).rjust(6)}%] "
            "분배목록: [" + ",".join([str(d) for d in divide]) + "]"
        )
    logger.info("\n".join(result_msg))

    if use_graph:
        plt.figure(figure_counter, figsize=(16, 8), dpi=80)
        figure_counter += 1

        plt.plot(x_list, y_best_list)
        # plt.plot(x_list, y_median_list)
        plt.plot(x_list, y_average_list)
        # plt.plot(x_list, y_worst_list)

        # plt.title("")
        plt.xlabel("Epoch")
        plt.ylabel("Fitness")
        plt.tight_layout()

        plt.tight_layout()
        plt.show()

    result["result"] = gene_answer_list

    return result


MODE_PROPERTY = {
    "desc": "분배 문제를 해결합니다. (기본 모드)",
    "req_desc": "데이터 파일의 첫 번째 줄에 분배 개수 및 배율, 두 번째 줄에 분배 해야하는 수를 작성해주세요. (띄어쓰기로 구분)",
    "func": main,
}
