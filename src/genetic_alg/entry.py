from ast import arg
from pprint import pformat
from time import time

from genetic_alg import log
from genetic_alg.functions import divide

# 모드 정의
MODE_LIST = {
    "divide": divide.MODE_PROPERTY,
}


def main():
    import argparse

    parser = argparse.ArgumentParser(description="유전 알고리즘 프로젝트")

    parser.add_argument("-i", dest="input", default=None, help="데이터 파일 경로")
    parser.add_argument("-o", dest="output", default="out", help="출력 디렉토리 경로")
    parser.add_argument("--list", dest="view_list", action="store_true", help="사용 가능한 모드 리스트 확인")
    parser.add_argument("-m", dest="mode", default="divide", choices=list(MODE_LIST.keys()), help="사용 모드")
    parser.add_argument("--log-dir", dest="log_path", default=log.DIR_PATH, help="로그 디렉토리 경로")
    parser.add_argument("--log-level", dest="log_level", default=log.ROOT_LOG_LEVEL, choices=["debug", "info", "warning", "error", "critical"], help="로그 출력 레벨")
    parser.add_argument("--no-setup", dest="use_setup", action="store_false", help="자세한 설정 사용 여부 (해당 옵션을 사용할 경우, 기본값으로 진행합니다.)")
    parser.add_argument("--no-graph", dest="use_graph", action="store_false", help="그래프 시각화 사용여부")
    parser.add_argument("--no-progress-graph", dest="use_progress_graph", action="store_false", help="유전자 풀 진행 그래프 사용여부")

    args = vars(parser.parse_args())

    # 모드 리스트를 확인할 경우
    if args["view_list"]:
        for mode, content in MODE_LIST.items():
            print((f"[{mode}]\n" f"설명: {content['desc']}\n" f"필요사항: {content['req_desc']}"))
        return

    # 로그 설정
    log.DIR_PATH = args["log_path"]
    log.ROOT_LOG_LEVEL = args["log_level"]

    logger = log.get_logger(main)

    logger.info(f"[프로그램 시작점]\nArgs: {pformat(args)}")

    mode = args["mode"]
    if mode in MODE_LIST:
        logger.info(f"[{mode}] 모드를 사용합니다.")

        mode_content = MODE_LIST[mode]
        mode_func = mode_content["func"]

        start_time = time()
        try:
            result = mode_func(**args)  # 해당 모드의 함수 실행
        except AssertionError as ex:
            logger.error(f"오류가 발생했습니다.\nException: {pformat(ex)}")
        else:
            if isinstance(result, dict):
                start_time += result.get("time_offset", 0)
        logger.info(f"실행에 [{time() - start_time}] 초가 소모되었습니다.")
    else:
        logger.error(f"[{mode}]는 구현되지 않았거나, 지원하지 않는 모드입니다. 지원하는 모드를 확인하려면 --list 옵션을 사용하세요.")


if __name__ == "__main__":
    main()
