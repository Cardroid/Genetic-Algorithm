import os

from genetic_alg import log


def main(**kwargs):
    assert "input" in kwargs and os.path.isfile(kwargs["input"]), "데이터 파일이 존재하지 않습니다."

    data_filepath = kwargs["input"]
    use_graph = kwargs.get("use_graph", True)

    logger = log.get_logger(main)
