import time
import threading
from typing import Mapping


class TestThread(threading.Thread):
    def __init__(self, map: Mapping[str, int]) -> None:
        super().__init__()
        self.map = map

    def run(self):
        for key, value in self.map.items():
            time.sleep(value)


test_dict = {"a": 1, "b": 2, "c": 3}
trd = TestThread(test_dict)
trd.start()
time.sleep(2)
test_dict["d"] = 4
