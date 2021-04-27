"""
Timer Module
"""

__author__ = "Eric Lemmon"
__copyright__ = "Copyright 2021, Eric Lemmon"
__credits = ["Eric Lemmon, Anne Sophie Andersen"]
__version__ = "0.9"
__maintainer__ = "Eric Lemmon"
__email__ = "ec.lemmon@gmail.com"
__status__ = "Testing"

class Timer:
    def __init__(self, start_time=0):
        self.time = start_time

    def get_time(self):
        return self.time

    def increment(self):
        self.time += 1

    def decrement(self):
        self.time -= 1

    def set_time(self, new_time):
        self.time = new_time

    def get_formatted_time(self):
        mins, secs = divmod(self.time, 60)
        timeformat = '{:02d}:{:02d} \r'.format(mins, secs)
        return timeformat

if __name__ == "__main__":
    timer = Timer(120)
    print(timer.get_time())
    timer.increment()
    print(timer.get_time())
    timer.decrement()
    print(timer.get_time())
    timer.set_time(1000)
    print(timer.get_time())
