import time

log = []


class ChronoMeter:
    start_time = 0
    end_time = 0

    def start(self):
        self.start_time = self.current_milli_time()

    def stop(self):
        self.end_time = self.current_milli_time()

    def get_execution_time(self):
        return self.end_time - self.start_time

    def stop_and_append_log(self):
        self.stop()
        log.append(self.get_execution_time())

    def print_time(self):
        print(f"execution time: {self.get_execution_time()} ms")

    @staticmethod
    def current_milli_time():
        return round(time.time() * 1000)

    @staticmethod
    def mean_log():
        return sum(log) / len(log)
