import streamlit as st
import matplotlib.pyplot as plt
import random
import time
from itertools import zip_longest

# 기존에 만들어둔 알고리즘 모듈 재사용!
from algorithms.bubble_sort import bubble_sort
from algorithms.selection_sort import selection_sort

# --- [1] 페이지 설정 ---
st.set_page_config(page_title="알고리즘 시각화 대시보드", layout="wide")

st.title("📊 Sorting Algorithm Visualizer")
st.markdown("파이썬으로 구현한 정렬 알고리즘을 **웹 대시보드**에서 비교해봅시다.")

# --- [2] 사이드바 (컨트롤 패널) ---
with st.sidebar:
    st.header("⚙️ 설정")
    n = st.slider("데이터 개수 (N)", min_value=10, max_value=100, value=30, step=5)
    speed = st.slider("애니메이션 속도 (초)", 0.01, 0.5, 0.05)

    start_btn = st.button("시각화 시작! 🚀", type="primary")


# --- [3] 메인 시각화 함수 ---
def run_visualization(n, speed):
    # 데이터 생성

    max_data_size = 100
    if n > max_data_size:
        st.error(f"보안 경고: 데이터 개수는 {max_data_size}개를 초과할 수 없습니다.")
        return  # 함수 강제 종료

    if speed < 0.01:
        st.warning("속도가 너무 빠르면 브라우저가 멈출 수 있습니다.")
        speed = 0.01  # 최소 속도 강제 조정

    raw_data = list(range(1, n + 1))
    random.shuffle(raw_data)

    data1 = raw_data[:]
    data2 = raw_data[:]

    stats1 = {'comp': 0, 'swap': 0}
    stats2 = {'comp': 0, 'swap': 0}

    # 그래프 자리 잡기 (빈 공간 생성)
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Bubble Sort")
        chart_placeholder1 = st.empty()  # 그래프가 들어갈 빈 상자 1
        stats_placeholder1 = st.empty()  # 텍스트가 들어갈 빈 상자 1

    with col2:
        st.subheader("Selection Sort")
        chart_placeholder2 = st.empty()  # 그래프가 들어갈 빈 상자 2
        stats_placeholder2 = st.empty()  # 텍스트가 들어갈 빈 상자 2

    # Matplotlib Figure 생성 (딱 한 번만 생성)
    fig1, ax1 = plt.subplots(figsize=(5, 4))
    fig2, ax2 = plt.subplots(figsize=(5, 4))

    # 제너레이터 생성
    gen1 = bubble_sort(data1, stats1)
    gen2 = selection_sort(data2, stats2)

    # --- [4] 애니메이션 루프 ---
    for frames in zip_longest(gen1, gen2, fillvalue=None):
        bubble_state, select_state = frames

        # --- 왼쪽 (버블) 그리기 ---
        ax1.clear()  # 이전 그림 지우기
        if bubble_state:
            arr, idx_list = bubble_state
            # 기존 스타일 그대로 적용
            bars = ax1.bar(range(n), arr, color='b', edgecolor='black', linewidth=0.5, align='edge', width=1.0)
            for i in idx_list:
                bars[i].set_facecolor('r')
        else:
            # 완료 시
            ax1.bar(range(n), data1, color='purple', edgecolor='black', linewidth=0.5, align='edge', width=1.0)

        ax1.set_xlim(0, n)
        ax1.set_ylim(0, int(n * 1.1))
        ax1.axis('off')  # 축 눈금 숨기기 (깔끔하게)

        # --- 오른쪽 (선택) 그리기 ---
        ax2.clear()
        if select_state:
            arr, idx_list = select_state
            bars = ax2.bar(range(n), arr, color='b', edgecolor='black', linewidth=0.5, align='edge', width=1.0)
            for i in idx_list:
                bars[i].set_facecolor('r')
        else:
            ax2.bar(range(n), data2, color='purple', edgecolor='black', linewidth=0.5, align='edge', width=1.0)

        ax2.set_xlim(0, n)
        ax2.set_ylim(0, int(n * 1.1))
        ax2.axis('off')

        # --- 화면 업데이트 ---
        # Matplotlib 그림을 Streamlit 상자에 집어넣음
        chart_placeholder1.pyplot(fig1)
        chart_placeholder2.pyplot(fig2)

        # 텍스트 업데이트
        stats_placeholder1.info(f"비교: {stats1['comp']} | 교환: {stats1['swap']}")
        stats_placeholder2.info(f"비교: {stats2['comp']} | 교환: {stats2['swap']}")

        # 속도 조절
        time.sleep(speed)

    st.success("정렬이 완료되었습니다! 🎉")


# 버튼이 눌리면 함수 실행
if start_btn:
    run_visualization(n, speed)