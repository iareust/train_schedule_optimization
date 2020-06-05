from simpy import Environment
import math


class TrainEnvironment(Environment):
    """
    SimPy Environment with extensions to track the performance of the train network

    """

    def __init__(self):
        super().__init__()

        self.total_delay = {}
        self.total_early = {}
        self.total_handled = 0
        self.total_passengers = 0
        self.total_drive_h = 0

    def delay(self) -> int:
        return sum(self.total_delay.values())

    def add_delay(self, line_id: str, amount: int):
        if not line_id in self.total_delay.keys():
            self.total_delay[line_id] = int(0)

        self.total_delay[line_id] += int(amount)

    def early(self) -> int:
        return sum(self.total_early.values())

    def add_early(self, line_id: str, amount: int):
        if not line_id in self.total_early.keys():
            self.total_early[line_id] = int(0)

        self.total_early[line_id] += int(amount)

    def get_reward_handled(self):
        inner_function = 1.0-math.sqrt(1.0-(self.total_handled/self.total_passengers)**2)
        return min(1.0, max(0.0, inner_function))

    def get_reward_delay(self, tolarance_per_line, num_lines):
        inner_function = (1.0-((self.delay()-tolarance_per_line*num_lines)/(self.total_drive_h-tolarance_per_line*num_lines)))**2
        return min(1.0, max(0.0, inner_function))

    def get_reward_early_arrival(self):
        inner_function = math.sqrt(1.0-min(1.0, 4.0*(self.early()/self.total_drive_h)**2))
        return min(1.0, max(0.0, inner_function))
