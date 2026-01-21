from itertools import zip_longest
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random

# 분리한 알고리즘 모듈 임포트
from algorithms.bubble_sort import bubble_sort
from algorithms.selection_sort import selection_sort

class SortingVisualizer:
    def __init__(self, data_length=50):
        self.n = data_length
        raw_data = list(range(1, self.n + 1))
        random.shuffle(raw_data)

        # 상태 관리를 위한 딕셔너리 (C++의 구조체처럼 사용)
        self.stats1 = {'comp': 0, 'swap': 0}
        self.stats2 = {'comp': 0, 'swap': 0}

        self.data1 = raw_data[:]
        self.data2 = raw_data[:]

        self.fig, (self.ax1, self.ax2) = plt.subplots(1, 2, figsize=(12, 5))
        self.setup_graph() # 그래프 설정 코드가 길어서 메서드로 분리하면 더 깔끔합니다.

    def setup_graph(self):
        # [왼쪽] 버블 정렬
        self.ax1.set_title("Bubble Sort")
        self.rects1 = self.ax1.bar(range(self.n), self.data1, color='b', edgecolor='white', linewidth=0.5, align='edge', width=1.0)
        self.ax1.set_xlim(0, self.n)
        self.ax1.set_ylim(0, int(self.n * 1.1))
        self.text1 = self.ax1.text(0.02, 0.95, "", transform=self.ax1.transAxes)

        # [오른쪽] 선택 정렬
        self.ax2.set_title("Selection Sort")
        self.rects2 = self.ax2.bar(range(self.n), self.data2, color='g', edgecolor='white', linewidth=0.5, align='edge', width=1.0)
        self.ax2.set_xlim(0, self.n)
        self.ax2.set_ylim(0, int(self.n * 1.1))
        self.text2 = self.ax2.text(0.02, 0.95, "", transform=self.ax2.transAxes)

    def update(self, frames):
        bubble_state, select_state = frames

        # --- 왼쪽 업데이트 ---
        if bubble_state:
            arr, idx_list = bubble_state
            for i, rect in enumerate(self.rects1):
                rect.set_height(arr[i])
                rect.set_facecolor('r' if i in idx_list else 'b')
            # 딕셔너리에서 값을 꺼내와 표시
            self.text1.set_text(f"Comp: {self.stats1['comp']} | Swap: {self.stats1['swap']}")
        else:
            for rect in self.rects1: rect.set_facecolor('purple')

        # --- 오른쪽 업데이트 ---
        if select_state:
            arr, idx_list = select_state
            for i, rect in enumerate(self.rects2):
                rect.set_height(arr[i])
                rect.set_facecolor('r' if i in idx_list else 'b')
            self.text2.set_text(f"Comp: {self.stats2['comp']} | Swap: {self.stats2['swap']}")
        else:
            for rect in self.rects2: rect.set_facecolor('purple')

    def animate(self):
        # 알고리즘 함수에 데이터와 stats 딕셔너리를 함께 넘김
        gen1 = bubble_sort(self.data1, self.stats1)
        gen2 = selection_sort(self.data2, self.stats2)

        anim = animation.FuncAnimation(
            self.fig,
            func=self.update,
            frames=zip_longest(gen1, gen2, fillvalue=None),
            interval=10,
            repeat=False,
            save_count=2000
        )
        plt.show()