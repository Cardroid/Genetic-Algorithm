import os

from genetic_alg import log


def main(**kwargs):
    assert "input" in kwargs and os.path.isfile(kwargs["input"]), "데이터 파일이 존재하지 않습니다."

    data_filepath = kwargs["input"]
    use_graph = kwargs.get("use_graph", True)

    logger = log.get_logger(main)

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

    logger.info(f"분배 수: [{len(dest_list)}], 분배 항목 수: [{len(target_list)}]")


MODE_PROPERTY = {
    "desc": "분배 문제를 해결합니다. (기본 모드)",
    "req_desc": "데이터 파일의 첫 번째 줄에 분배 개수 및 배율, 두 번째 줄에 분배 해야하는 수를 작성해주세요. (띄어쓰기로 구분)",
    "func": main,
}
