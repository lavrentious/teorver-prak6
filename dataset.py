from typing import List, Tuple
from collections import Counter
import math


class StatItem:
    stat: float
    count: int
    p: float  # относительная частота (p = ni/n)

    def __init__(self, stat: float, count: int, size: int) -> None:
        self.stat = stat
        self.count = count
        self.p = count / size


class EmpiricFunction:
    items: List[Tuple[float, float, float]]  # interval_start, interval_end, f

    # F(interval_start <= x < interval_end)
    def __init__(self, stat_series: List[StatItem]) -> None:
        self.items = []
        inf = float("inf")
        self.items.append((-inf, stat_series[0].stat, 0))
        for stat in stat_series[1:]:
            self.items.append(
                (self.items[-1][1], stat.stat, self.items[-1][2] + stat.p)
            )
        self.items.append((stat_series[-1].stat, inf, 1))

    def to_string(self) -> str:
        ans = ""
        for interval_start, interval_end, f in self.items:
            left_sign = "<" if interval_start == -float("inf") else "<="
            right_sign = "<"

            l = "-∞" if interval_start == -float("inf") else str(interval_start)
            r = "∞" if interval_end == float("inf") else str(interval_end)

            ans += f"{l}\t{left_sign}\tx\t{right_sign}\t{r}\t:\t{round(f, 3)}\n"
        return ans


class Dataset:

    data: List[float]

    def __init__(self, data: List[float]) -> None:
        self.data = data

    def size(self) -> int:
        return len(self.data)

    # вариационный ряд
    def var_series(self) -> List[float]:
        return sorted(self.data)

    # размах выборки
    def width(self) -> float:
        return self.var_series()[-1] - self.var_series()[0]

    # статистический ряд
    # статистика: количество вхождений
    def stat_series(self) -> List[StatItem]:
        c = sorted(Counter(self.data).items(), key=lambda x: x[0])
        return [StatItem(stat, count, len(self.data)) for stat, count in c]

    # выборочное среднее (матемтаическое ожидание)
    def mean(self) -> float:
        ans: float = 0.0
        for stat in self.stat_series():
            ans += stat.stat * stat.count
        return ans / len(self.data)

    # выборочная дисперсия
    def variance(self) -> float:
        ans: float = 0.0
        for stat in self.stat_series():
            ans += (stat.stat - self.mean()) ** 2 * stat.count
        return ans / len(self.data)

    # среднее квадратичное отклонение
    def std(self) -> float:
        return self.variance() ** 0.5

    # исправленная выборочная дисперсия
    def corrected_variance(self) -> float:
        n = len(self.data)
        return n * self.variance() / (n - 1)

    # исправленное среднее квадратичное отклонение
    def corrected_std(self) -> float:
        return self.corrected_variance() ** 0.5

    # эмпирическая функция распределения
    def cdf(self) -> EmpiricFunction:
        return EmpiricFunction(self.stat_series())

    # величина интервала статистического ряда (формула Стерджеса)
    def get_h(self) -> float:
        return self.width() / (1 + math.log2(self.size()))

    # число интервалов (формула Стерджеса)
    def get_m(self) -> int:
        return math.ceil(1 + math.log2(self.size()))
