import random
import time


class Behavior:
    def __init__(self):
        self.delay_function = time.sleep

    def random_pause(self, min_value=1, max_value=5):
        self.delay_function(self.get_random_delay(min_value, max_value))

    def get_random_delay(self, min_value=1, max_value=5):
        return random.uniform(min_value, max_value)

