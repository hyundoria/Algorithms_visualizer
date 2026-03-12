import streamlit as st
import matplotlib.pyplot as plt
import random
import time
from itertools import zip_longest

# 알고리즘 모듈
from algorithms.bubble_sort import bubble_sort
from algorithms.selection_sort import selection_sort
from algorithms.insertion_sort import insertion_sort
from algorithms.merge_sort import merge_sort
from algorithms.heap_sort import heap_sort
from algorithms.quick_Sort import quick_sort

ALGO_MAP = {
    "버블 정렬 (Bubble Sort)": bubble_sort,
    "선택 정렬 (Selection Sort)": selection_sort,
    "삽입 정렬 (Insertion Sort)": insertion_sort,
    "병합 정렬 (Merge Sort)": merge_sort,
    "힙 정렬 (Heap Sort)": heap_sort,
    "퀵 정렬 (Quick Sort)": quick_sort,
}

# --- 페이지 설정 ---
st.set_page_config(page_title="알고리즘 시각화 대시보드", layout="wide")

st.title("📊 Algorithm Visualizer")
st.markdown("파이썬으로 구현한 알고리즘을 **웹 대시보드**에서 비교해봅시다.")

# --- 사이드바 ---
with st.sidebar:
    st.header("⚙️ 설정")

    selected_algos = st.multiselect(
        "비교할 알고리즘 선택",
        options=list(ALGO_MAP.keys()),
        default=["삽입 정렬 (Insertion Sort)", "버블 정렬 (Bubble Sort)"] # 기본으로 띄울 알고리즘
    )

    n = st.slider("데이터 개수 (N)", min_value=10, max_value=50, value=30, step=5)
    speed = st.slider("애니메이션 속도 (초)", 0.01, 0.5, 0.05)

    start_btn = st.button("시각화 시작! 🚀", type="primary")


# --- 메인 시각화 함수 ---
def run_visualization(algo_names, n, speed):
    # 데이터 생성

    if not algo_names:
        st.warning("적어도 하나 이상의 알고리즘을 선택해주세요!")

    max_data_size = 100
    if n > max_data_size:
        st.error(f"데이터 개수는 {max_data_size}개를 초과할 수 없습니다.")
        return  # 함수 강제 종료

    if speed < 0.01:
        st.warning("속도가 너무 빠르면 브라우저가 멈출 수 있습니다.")
        speed = 0.01  # 최소 속도 강제 조정

    # 데이터 생성
    raw_data = list(range(1, n + 1))
    random.shuffle(raw_data)

    # --- 화면 컬럼 동적 생성 ---
    # 선택한 알고리즘 개수만큼 화면을 나눕니다.
    cols = st.columns(len(algo_names))

    generators = []
    placeholders = []
    stats_placeholders = []
    figs = []
    axs = []
    stats_list = []

    # --- 각 알고리즘별 초기화 ---
    for i, (col, name) in enumerate(zip(cols, algo_names)):
        with col:
            st.subheader(name) # 선택한 알고리즘 이름 표시
            chart_ph = st.empty()
            stat_ph = st.empty()

            placeholders.append(chart_ph)
            stats_placeholders.append(stat_ph)

            fig, ax = plt.subplots(figsize=(5, 4))
            figs.append(fig)
            axs.append(ax)

            data_copy = raw_data[:]
            stats = {'comp': 0, 'swap': 0}
            stats_list.append(stats)

            # 딕셔너리에서 함수를 꺼내 제너레이터 생성
            sort_func = ALGO_MAP[name]
            generators.append(sort_func(data_copy, stats))

    # --- 애니메이션 루프 ---
    for frames in zip_longest(*generators, fillvalue=None):
        for i, state in enumerate(frames):
            ax = axs[i]
            ax.clear()  # 이전 그림 지우기

            if state is None:
                # 완료 시 보라색으로 렌더링
                ax.bar(range(n), sorted(raw_data), color='purple', edgecolor='black', linewidth=0.5, align='edge', width=1.0)
            else:
                arr, idx_list = state
                bars = ax.bar(range(n), arr, color='b', edgecolor='black', linewidth=0.5, align='edge', width=1.0)
                for idx in idx_list:
                    if idx < n:
                        bars[idx].set_facecolor('r')

            ax.set_xlim(0, n)
            ax.set_ylim(0, int(n * 1.1))
            ax.axis('off')  # 축 눈금 숨기기

            # 화면 업데이트
            placeholders[i].pyplot(figs[i])
            stats = stats_list[i]
            stats_placeholders[i].info(f"비교: {stats['comp']} | 교환: {stats['swap']}")

        # 속도 조절
        time.sleep(speed)

    st.success("정렬이 완료되었습니다! 🎉")


# 버튼이 눌리면 함수 실행
if start_btn:
    run_visualization(selected_algos, n,speed)