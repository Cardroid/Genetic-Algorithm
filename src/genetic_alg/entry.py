from pprint import pformat
from genetic_alg import log


def main():
    import argparse

    parser = argparse.ArgumentParser(description="유전 알고리즘 프로젝트")

    parser.add_argument("-i", dest="input", required=True, help="데이터 파일 경로")
    parser.add_argument("-o", dest="output", default="out", help="출력 디렉토리 경로")
    parser.add_argument("-m", dest="mode", default="divide", help="로그 디렉토리 경로")
    parser.add_argument("--log-dir", dest="log_path", default=log.DIR_PATH, help="로그 디렉토리 경로")
    parser.add_argument("--log-level", dest="log_level", default=log.ROOT_LOG_LEVEL, choices=["debug", "info", "warning", "error", "critical"], help="로그 출력 레벨")
    parser.add_argument("--no-graph", dest="use_graph", action="store_false", help="그래프 시각화 사용여부")

    args = vars(parser.parse_args())

    # 로그 설정
    log.DIR_PATH = args["log_path"]
    log.ROOT_LOG_LEVEL = args["log_level"]

    logger = log.get_logger("main")

    logger.info(f"[프로그램 시작점]\nArgs: {pformat(args)}")


if __name__ == "__main__":
    main()
