from genetic_alg import log


def main():
    import argparse

    parser = argparse.ArgumentParser(description="미디어를 압축 인코딩합니다.")

    parser.add_argument("-i", dest="input", action="append", required=True, help="하나 이상의 입력 소스 파일 및 디렉토리 경로")
    parser.add_argument("-o", dest="output", default="out", help="출력 디렉토리 경로")
    parser.add_argument("--log-dir", dest="log_path", default=log.DIR_PATH, help="로그 디렉토리 경로")
    parser.add_argument("--log-level", dest="log_level", choices=["debug", "info", "warning", "error", "critical"], help="로그 출력 레벨")
    parser.add_argument("--no-graph", dest="use_graph", action="store_false", help="그래프 시각화 사용여부")

    args = vars(parser.parse_args())

    # 기본 로그 출력경로 설정
    log.DIR_PATH = args["log_path"]


if __name__ == "__main__":
    main()
