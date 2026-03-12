from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

import random



from algorithms.bubble_sort import bubble_sort
from algorithms.selection_sort import selection_sort
from algorithms.insertion_sort import insertion_sort
from algorithms.merge_sort import merge_sort
from algorithms.heap_sort import heap_sort
from algorithms.quick_sort import quick_sort

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
    "quick": quick_sort
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
        func = ALGO_MAP[algo_name] # 실행할 함수 꺼내기

        history = []
        history.append({"arr": arr[:], "active": [], "comp": 0, "swap": 0}) # 시작 상태

        # 제너레이터(yield)를 돌면서 history에 사진을 찍어 모읍니다.
        for state in func(arr, stats):
            if state is None: # 알고리즘이 yield None을 뱉으면 무시
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
                        "swap": stats['swap']}) # 완료 상태
        results[algo_name] = history

    return results


# 도커에서 HTML을 띄워주기 위한 라우터
@app.get("/")
def serve_frontend():
    return FileResponse("index.html")