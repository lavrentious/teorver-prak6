from dataset import Dataset

from logger import Logger, LogLevel
from typing import List
import sys
from tabulate import tabulate


def main() -> None:
    # init
    logger = Logger(LogLevel.DEBUG)

    file_path = sys.argv[1]
    logger.debug(f"{file_path=}")

    data: List[float] = []
    with open(file_path, "r") as f:
        data = [float(x) for x in f.read().strip("\n").split("\n")]
    dataset = Dataset(data)

    logger.debug(f"{dataset.data=}")

    # 1. вариационный ряд
    print("1. Вариационный ряд: ", dataset.var_series())
    print("1.1 первая порядковая статистика: ", dataset.var_series()[0])
    print("1.1 n-ая порядковая статистика: ", dataset.var_series()[-1])
    print("1.2 размах: ", dataset.width())

    # 2. статистический ряд
    print("2. Статистический ряд: ")
    stat_series = dataset.stat_series()
    print(
        tabulate(
            [[stat.stat, stat.count, stat.p] for stat in stat_series],
            headers=["Статистика", "Частота", "Отн. частота"],
            tablefmt="heavy_grid",
        )
    )
    print("2.1 Оценка мат. ожидания: ", dataset.mean())
    print("2.1 Оценка дисперсии: ", dataset.variance())
    print("2.1.1 Исправленная дисперсия: ", dataset.corrected_variance())
    print("2.2 Среднее квадратичное отклонение: ", dataset.std())
    print("2.2.1 Исправленное среднее квадратичное отклонение: ", dataset.corrected_std())

    # 3. эмпирическая функция распределения
    print('3. Эмпирическая функция распределения:')
    print(dataset.cdf().to_string())

if __name__ == "__main__":
    main()
