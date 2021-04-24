import tkinter as tk


class FlashableLabel(tk.Label):
    def flash(self, flashes=10, count=0):
        bg = self.cget('background')
        fg = self.cget('foreground')
        self.configure(background=fg, foreground=bg)
        count += 1
        if count < flashes:
            self.after(250, self.flash, count)
