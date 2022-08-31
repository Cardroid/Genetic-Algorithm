# 유전 알고리즘 프로젝트

### 설치 방법

```
python -m pip install git+https://github.com/Cardroid/Genetic-Algorithm.git
```

### 실행 방법

#### 도움말

##### 입력

```
gene -h
```

##### 출력

```
usage: gene [-h]
            [-i INPUT]
            [-o OUTPUT]
            [--list]
            [-m {divide}]
            [--log-dir LOG_PATH]
            [--log-level {debug,info,warning,error,critical}]
            [--no-setup]
            [--no-graph]
            [--no-progress-graph]

유전 알고리즘 프로젝트

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT              데이터 파일 경로
  -o OUTPUT             출력 디렉토리 경로
  --list                사용 가능한 모드 리스트 확인
  -m {divide}           사용 모드
  --log-dir LOG_PATH    로그 디렉토리 경로
  --log-level {debug,info,warning,error,critical}
                        로그 출력 레벨
  --no-setup            자세한 설정 사용 여부 (해당 옵션을 사용할 경우, 기본값으로 진행합니다.)
  --no-graph            그래프 시각화 사용여부
  --no-progress-graph   유전자 풀 진행 그래프 사용여부
```

### 실행 예시

#### 분배 문제

```
gene -m divide -i [데이터 경로]
```

#### 데이터 파일 형식

```
배분 비율
배분 해야할 수
```

##### 예시

```
0.5 0.5
10 20 30 40 50
```
