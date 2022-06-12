"""
Course: Artificial Intelligence 2021/2022

Lecturer:
Marcelli      Angelo      amarcelli@unisa.it
Della Cioppa  Antonio     adellacioppa@unisa.it

Group:
Salvati       Vincenzo    0622701550      v.salvati10@studenti.unisa.it
Mansi         Paolo       0622701542      p.mansi5@studenti.unisa.it

@file Chronometer.py


PURPOSE OF THE FILE: set and read chronometer.
"""

import time


class Chronometer:
    """Object Chronometer

    Attributes:
        start_time (float): system time
        end_time (float): system time
        log (List[float]): list of executions time
    """

    def __init__(self):
        """Init chronometer

        """
        self.start_time = 0
        self.end_time = 0
        self.log = []

    def start(self):
        """Start chronometer

        """
        self.start_time = self.second_to_millisecond()

    def stop(self):
        """Stop chronometer

        """
        self.end_time = self.second_to_millisecond()

    def get_execution_time(self):
        """Return execution time

        Returns:
            (float): execution time in milliseconds
        """
        return self.end_time - self.start_time

    def append_log(self):
        """Append execution time to the chronometer's log

        """
        self.log.append(self.get_execution_time())

    def get_log(self):
        """Return the chronometer's log

        Returns:
            (List[float]): log list
        """
        return self.log

    def stop_and_append_log(self):
        """Stop chronometer and append execution time to the chronometer's log

        """
        self.stop()
        self.append_log()

    def mean_log(self):
        """Return mean of the chronometer's log

        Returns:
            (float): mean log in milliseconds
        """
        return sum(self.get_log()) / len(self.get_log())

    @staticmethod
    def second_to_millisecond():
        """Return system time

        Returns:
            (float): system time in milliseconds
        """
        return round(time.time() * 1000)
