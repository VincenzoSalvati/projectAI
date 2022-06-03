import time


class ChronoMeter:
    def __init__(self):
        self.start_time = 0
        self.end_time = 0
        self.log = []

    def start(self):
        self.start_time = self.current_milli_time()

    def stop(self):
        self.end_time = self.current_milli_time()

    def get_execution_time(self):
        return self.end_time - self.start_time

    def append_log(self):
        self.log.append(self.get_execution_time())

    def get_log(self):
        return self.log

    def stop_and_append_log(self):
        self.stop()
        self.append_log()

    def print_time(self):
        print(f"execution time: {self.get_execution_time()} ms")

    def mean_log(self):
        return sum(self.get_log()) / len(self.get_log())

    @staticmethod
    def current_milli_time():
        return round(time.time() * 1000)
