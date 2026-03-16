from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

import asyncio
import random


from algorithms.bubble_sort import bubble_sort
from algorithms.selection_sort import selection_sort
from algorithms.insertion_sort import insertion_sort
from algorithms.merge_sort import merge_sort
from algorithms.heap_sort import heap_sort
from algorithms.quick_sort import quick_sort
from algorithms.shell_sort import shell_sort
from algorithms.counting_sort import counting_sort
from algorithms.raidx_sort import radix_sort
from algorithms.bucket_sort import bucket_sort

app = FastAPI()

# 프론트에서 api 호출 권한 허용
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 문자열 이름과 실제 함수를 연결해주는 딕셔너리
ALGO_MAP = {
    "bubble": bubble_sort,
    "selection": selection_sort,
    "insertion": insertion_sort,
    "merge": merge_sort,
    "heap": heap_sort,
    "quick": quick_sort,
    "shell": shell_sort,
    "counting": counting_sort,
    "radix": radix_sort,
    "bucket": bucket_sort
}


@app.get("/api/sort")
def get_multiple_sorts(algos: str = "bubble,selection", n: int = 30):

    # 공통 원본 배열
    base_arr = list(range(1, n + 1))
    random.shuffle(base_arr)

    algo_list = algos.split(",")
    results = {}

    for algo_name in algo_list:
        if algo_name not in ALGO_MAP:
            continue

        arr = base_arr[:]  # 원본 복사
        stats = {'comp': 0, 'swap': 0}
        func = ALGO_MAP[algo_name]  # 실행할 함수 꺼내기

        history = []
        history.append({"arr": arr[:], "active": [],
                       "comp": 0, "swap": 0})  # 시작 상태

        # 제너레이터(yield)를 돌면서 history에 사진을 찍어 모읍니다.
        for state in func(arr, stats):
            if state is None:  # 알고리즘이 yield None을 뱉으면 무시
                continue

            # state는 (arr, [비교/교환중인 인덱스들]) 형태입니다.
            current_arr, active_indices = state
            history.append({
                "arr": current_arr[:],
                "active": active_indices,
                "comp": stats['comp'],
                "swap": stats['swap']
            })
        history.append({"arr": arr[:],
                        "active": [],
                        "comp": stats['comp'],
                        "swap": stats['swap']})  # 완료 상태
        results[algo_name] = history

    return results


# WebSocket을 이용한 실시간 정렬 (중지 기능 지원)
@app.websocket("/ws/sort")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        # 클라이언트로부터 설정 수신 (예: {"algos": "bubble", "n": 30})
        data = await websocket.receive_json()
        target_algos = data.get("algos", "bubble").split(",")
        n = int(data.get("n", 30))

        base_arr = list(range(1, n + 1))
        random.shuffle(base_arr)

        for algo_name in target_algos:
            if algo_name not in ALGO_MAP:
                continue

            arr = base_arr[:]
            stats = {'comp': 0, 'swap': 0}
            func = ALGO_MAP[algo_name]

            for state in func(arr, stats):
                if state is None:
                    continue

                current_arr, active_indices = state
                # 현재 상태 전송
                await websocket.send_json({
                    "algo": algo_name,
                    "arr": current_arr,
                    "active": active_indices,
                    "comp": stats['comp'],
                    "swap": stats['swap']
                })
                # 시각화 속도 조절 및 중단 체크를 위한 대기
                await asyncio.sleep(0.05)

    except WebSocketDisconnect:
        print("Client disconnected (Stop requested)")

# 도커에서 HTML을 띄워주기 위한 라우터


@app.get("/")
def serve_frontend():
    return FileResponse("index.html")
