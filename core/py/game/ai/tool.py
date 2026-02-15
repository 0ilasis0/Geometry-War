import random
from typing import Sequence


class RandomTool:
    @staticmethod
    def calc_fluctuation(base_value: float, rate_range: Sequence[float]) -> float:
        """
        計算波動數值

        :param base_value: 基準值 (例如 action_interval)
        :param rate_range: 波動範圍 (例如 (0.8, 1.2))
        :return: base_value * random_rate
        """
        if not rate_range:
            return base_value

        r_min = min(rate_range)
        r_max = max(rate_range)

        if r_min == r_max:
            return base_value * r_min

        return base_value * random.uniform(r_min, r_max)

    @staticmethod
    def random_in_range(value_range: Sequence[float]) -> float:
        """
        單純取得範圍內的隨機值 (不乘基數)
        """
        return random.uniform(min(value_range), max(value_range))
