"""
Flashable Label Module derived from Bryan Oakley's answer on flashing tkinter labels on stackoverflow
https://stackoverflow.com/questions/21419032/flashing-tkinter-labels
"""

__author__ = "Eric Lemmon"
__copyright__ = "Copyright 2021, Eric Lemmon"
__credits = ["Eric Lemmon, Anne Sophie Andersen, Bryan Oakley"]
__version__ = "0.9"
__maintainer__ = "Eric Lemmon"
__email__ = "ec.lemmon@gmail.com"
__status__ = "Testing"


import tkinter as tk


class FlashableLabel(tk.Label):
    """
    A small flashable label class based on Bryan Oakley's answer on StackExchange.
    """
    def flash(self, flashes=10, count=0):
        """
        Flashes the label.
        :param flashes: the number of color changes, so the number of flashes will likely be experienced as
        flashes / 2
        :param count: count variable to recursively call the function while modifying the count elegantly.
        :return: None
        """
        bg = self.cget('background')
        fg = self.cget('foreground')
        self.configure(background=fg, foreground=bg)
        count += 1
        if count < flashes:
            self.after(250, self.flash, flashes, count)
