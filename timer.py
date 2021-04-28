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
    """
    A timer class for counting, setting and formatting time.
    """
    def __init__(self, start_time=0):
        """
        Initializes Timer class.
        :param start_time: The starting time in seconds.
        """
        self.time = start_time

    def get_time(self):
        """
        Gets the current time.
        :return: self.time in seconds.
        """
        return self.time

    def increment(self, amount=None):
        """
        Increments time up by one second.
        :return: None
        """
        if amount is None:
            self.time += 1
        else:
            self.time += amount

    def decrement(self, amount=None):
        """
        Decrements time up by one second.
        :return: None
        """
        if amount is None:
            self.time -= 1
        else:
            self.time -= amount

    def set_time(self, new_time):
        """
        Sets the current time in seconds.
        :param new_time: The time in seconds.
        :return: None
        """
        self.time = new_time

    def get_formatted_time(self):
        """
        Gets the formatted time in minutes and seconds.
        :return: formatted time in 00:00
        """
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
