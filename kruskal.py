from itertools import zip_longest
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random


class SortingVisualizer:

    def __init__(self, data_length=30):
        self.n = data_length
        raw_data = list(range(1, self.n + 1))
        random.shuffle(raw_data)

        # 비교 횟수 & 교환 횟수 초기화
        self.comparisons1 = 0
        self.swaps1 = 0

        self.comparisons2 = 0
        self.swaps2 = 0

        self.data1 = raw_data[:]
        self.data2 = raw_data[:]

        self.fig, (self.ax1, self.ax2) = plt.subplots(1, 2, figsize=(14, 6))

        # [왼쪽] 버블 정렬
        self.ax1.set_title("Bubble Sort")
        self.rects1 = self.ax1.bar(
            range(self.n),
            self.data1, color='b',
            edgecolor='white', # 테두리 색상D
            linewidth=0.5,     # 테두리 두께 (얇게)
            align='edge',      # 막대를 눈금의 오른쪽에 맞춤
            width=1.0          # 막대 너비를 꽉 채움)
        )
        self.ax1.set_ylim(0, int(self.n * 1.1))
        self.text1 = self.ax1.text(0.02, 0.95, "", transform=self.ax1.transAxes, fontsize=10)

        # [오른쪽] 선택 정렬
        self.ax2.set_title("Selection Sort")
        self.rects2 = self.ax2.bar(
            range(self.n),
            self.data2,
            color='b',
            edgecolor='white',
            linewidth=0.5,
            align='edge',
            width=1.0)
        self.ax2.set_ylim(0, int(self.n * 1.1))
        self.text2 = self.ax2.text(0.02, 0.95, "", transform=self.ax2.transAxes, fontsize=10)

    def bubble_sort(self, arr):
        n = len(arr)
        for i in range(n):
            for j in range(0, n - i - 1):
                yield arr, [j, j + 1]  # 비교 시각화

                self.comparisons1 += 1  # 비교 카운트

                if arr[j] > arr[j + 1]:
                    # 교환 발생!
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
                    self.swaps1 += 1  # 교환 카운트 증가
                    yield arr, [j, j + 1]  # 교환 시각화
        yield None

    def selection_sort(self, arr):
        n = len(arr)
        for i in range(n):
            min_idx = i
            for j in range(i + 1, n):
                self.comparisons2 += 1  # 비교 카운트
                yield arr, [i, j, min_idx]  # 탐색 시각화

                if arr[j] < arr[min_idx]:
                    min_idx = j
                    yield arr, [i, j, min_idx]  # 최솟값 갱신 시각화

            # [핵심] 찾은 최솟값이 제자리가 아니라면 교환
            if min_idx != i:
                arr[i], arr[min_idx] = arr[min_idx], arr[i]
                self.swaps2 += 1  # 교환 카운트 증가
                yield arr, [i, min_idx]  # 교환 시각화
            else:
                # 교환이 없어도 진행 상황은 보여줌 (선택 사항)
                yield arr, [i, i]

        yield None

    def update(self, frames):
        bubble_state, select_state = frames

        # --- [왼쪽] 버블 정렬 업데이트 ---
        if bubble_state is not None:
            arr1, idx_list1 = bubble_state
            for i, rect in enumerate(self.rects1):
                rect.set_height(arr1[i])
                if i in idx_list1:
                    rect.set_facecolor('r')
                else:
                    rect.set_facecolor('b')
            # 텍스트 업데이트 (비교 | 교환)
            self.text1.set_text(f"Comp: {self.comparisons1} | Swap: {self.swaps1}")
        else:
            for rect in self.rects1: rect.set_facecolor('purple')

        # --- [오른쪽] 선택 정렬 업데이트 ---
        if select_state is not None:
            arr2, idx_list2 = select_state
            for i, rect in enumerate(self.rects2):
                rect.set_height(arr2[i])
                if i in idx_list2:
                    rect.set_facecolor('r')
                else:
                    rect.set_facecolor('b')
            # 텍스트 업데이트 (비교 | 교환)
            self.text2.set_text(f"Comp: {self.comparisons2} | Swap: {self.swaps2}")
        else:
            for rect in self.rects2: rect.set_facecolor('purple')

    def animate(self):
        gen1 = self.bubble_sort(self.data1)
        gen2 = self.selection_sort(self.data2)

        anim = animation.FuncAnimation(
            self.fig,
            func=self.update,
            frames=zip_longest(gen1, gen2, fillvalue=None),
            interval=10,  # Swap 횟수 차이를 빨리 보기 위해 속도를 높임
            repeat=False,
            save_count=2000
        )
        plt.show()


if __name__ == "__main__":
    visualizer = SortingVisualizer(data_length=30)
    visualizer.animate()