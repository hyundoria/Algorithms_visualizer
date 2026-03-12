# Algorithms Visualizer

다양한 정렬 알고리즘의 작동 방식을 실시간으로 비교하고 시각화하는 풀스택 웹 애플리케이션입니다. 
FastAPI 백엔드에서 계산된 정렬 시뮬레이션 데이터를 받아 브라우저에서 고성능 애니메이션으로 구현합니다.

## 주요 기능
- **실시간 알고리즘 비교**: 버블, 선택, 삽입, 병합, 힙, 퀵 정렬 동시 비교
- **사용자 컨트롤러**: 데이터 개수(N) 조절 (10~100개) 및 애니메이션 속도 실시간 조절
- **실시간 통계**: 각 알고리즘별 비교 횟수(Comparison) 및 교환 횟수(Swap) 수치화

## 기술 스택
- **Backend**: Python 3.13, FastAPI, Uvicorn
- **Frontend**: HTML5, CSS3, Vanilla JavaScript (ES6+)
- **DevOps**: Docker, Render (Cloud Deployment)

## 실행 방법

프로젝트를 로컬 환경에서 도커로 실행하려면 다음 명령어를 입력하세요.

   docker build -t algo-app .
   docker run -p 8080:80 algo-app
   브라우저에서 http://localhost:8080 접속
