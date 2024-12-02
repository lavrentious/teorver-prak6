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

        stat_series = dataset.stat_series()
        h = dataset.get_h()  # ширина интервала
        m = dataset.get_m()  # количество интервалов

        x_start = stat_series[0].stat - (h / 2)
        for _ in range(m):
            cnt = 0  # количество статистик в интервале
            for stat in dataset.stat_series():
                if x_start <= stat.stat < x_start + h:
                    cnt += stat.count
            label = f"{round(x_start, 3)} : {round(x_start + h, 3)}"
            ax.bar(x_start, cnt / dataset.size(), width=h, label=label)
            # ax.fill_between((x_start, x_start + h), (value, value), label=label)
            x_start += h

        ax.legend(loc="upper left", bbox_to_anchor=(1.05, 1.0))
        ax.set_title("Гистограмма")
        ax.set_xlabel("x")
        ax.set_ylabel("F(x)")
        plt.tight_layout()
        plt.savefig(self._joined_path(file_path))

    def count_polygon(self, dataset: Dataset, file_path: str) -> None:
        fig, ax = plt.subplots()

        stat_series = dataset.stat_series()
        h = dataset.get_h()  # ширина интервала
        m = dataset.get_m()  # количество интервалов

        x_start = stat_series[0].stat - (h / 2)
        xs: List[float] = []
        ys: List[int] = []
        for _ in range(m):
            cnt = 0  # количество статистик в интервале
            for stat in dataset.stat_series():
                if x_start <= stat.stat < x_start + h:
                    cnt += stat.count
            # ax.plot(x_start + h / 2, cnt / dataset.size(), marker="o")
            xs.append(x_start + h / 2)
            ys.append(cnt)

            x_start += h

        ax.plot(xs, ys, marker="o")

        ax.set_title("Полигон частот")
        ax.set_xlabel("x")
        ax.set_ylabel("F(x)")
        plt.tight_layout()
        plt.savefig(self._joined_path(file_path))
