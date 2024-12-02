from dataset import EmpiricFunction, Dataset

import matplotlib.pyplot as plt
import os
from typing import List


class Chart:
    dir_path: str

    def __init__(self, dir_path: str) -> None:
        self.dir_path = dir_path
        os.makedirs(self.dir_path, exist_ok=True)

    def _joined_path(self, filename: str) -> str:
        return os.path.join(self.dir_path, filename)

    def cdf(self, empiric_function: EmpiricFunction, file_path: str) -> None:
        fig, ax = plt.subplots()

        for start, end, f in empiric_function.items:
            ax.hlines(y=f, xmin=start, xmax=end, label=f"{start} < x <= {end:.2f}")

        ax.set_title("Эмпирическая функция")
        ax.set_xlabel("x")
        ax.set_ylabel("F(x)")
        ax.set_yticks([i / 20.0 for i in range(0, 21)])

        ax.legend(loc="center left", bbox_to_anchor=(1, 0.5), fontsize="small")
        plt.tight_layout()
        plt.savefig(self._joined_path(file_path))

    def histogram(self, dataset: Dataset, file_path: str) -> None:
        fig, ax = plt.subplots()

        intervals = dataset.group()
        for interval in intervals:
            label = f"{round(interval.start, 3)} : {round(interval.end, 3)}"
            count = sum(map(lambda s: s.count, interval.items))
            value = count / dataset.size()
            width = interval.end - interval.start
            ax.bar(interval.start, value, width=width, label=label)

        ax.legend(loc="upper left", bbox_to_anchor=(1.05, 1.0))
        ax.set_title("Гистограмма")
        ax.set_xlabel("x")
        ax.set_ylabel("F(x)")
        plt.tight_layout()
        plt.savefig(self._joined_path(file_path))

    def count_polygon(self, dataset: Dataset, file_path: str) -> None:
        fig, ax = plt.subplots()

        intervals = dataset.group()
        xs: List[float] = []
        ys: List[int] = []
        for interval in intervals:
            xs.append((interval.end + interval.start) / 2)
            ys.append(sum(map(lambda s: s.count, interval.items)))

        ax.plot(xs, ys, marker="o")

        ax.set_title("Полигон частот")
        ax.set_xlabel("x")
        ax.set_ylabel("F(x)")
        plt.tight_layout()
        plt.savefig(self._joined_path(file_path))
