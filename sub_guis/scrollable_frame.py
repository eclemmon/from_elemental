"""
Scrollable frame module
H/t TheLizzard
https://stackoverflow.com/questions/66213754/unable-to-scroll-frame-using-mouse-wheel-adding-horizontal-scrollbar/66215091#66215091
"""

import tkinter as tk


class ScrollableFrame(tk.Frame):
    """
    Partly taken from:
        https://blog.tecladocode.com/tkinter-scrollable-frames/
        https://stackoverflow.com/a/17457843/11106801

    master_frame---------------------------------------------------------
    | dummy_canvas-----------------------------------------  y_scroll--  |
    | | self---------------------------------------------  | |         | |
    | | |                                                | | |         | |
    | | |                                                | | |         | |
    | | |                                                | | |         | |
    | |  ------------------------------------------------  | |         | |
    |  ----------------------------------------------------   ---------  |
     --------------------------------------------------------------------
    """
    def __init__(self, master=None, scroll_speed=2, **kwargs):
        assert isinstance(scroll_speed, int), "`scroll_speed` must be an int"
        self.scroll_speed = scroll_speed

        self.master_frame = tk.Frame(master)
        self.dummy_canvas = tk.Canvas(self.master_frame, **kwargs)
        super().__init__(self.dummy_canvas)

        self.scrollbar = tk.Scrollbar(self.master_frame, orient="vertical",
                                        command=self.dummy_canvas.yview)
        self.dummy_canvas.bind_all("<MouseWheel>", self.scrolling_windows,
                                   add=True)
        self.dummy_canvas.bind_all("<Button-4>", self.scrolling_linux, add=True)
        self.dummy_canvas.bind_all("<Button-5>", self.scrolling_linux, add=True)
        self.bind("<Configure>", self.scrollbar_scrolling, add=True)

        self.dummy_canvas.create_window((0, 0), window=self, anchor="nw")
        self.dummy_canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side="right", fill="y")
        self.dummy_canvas.pack(side="right", expand=True, fill="both")

    def scrolling_windows(self, event):
        assert event.delta != 0, "On Windows, `event.delta` should never be 0"
        y_steps = int(-event.delta/abs(event.delta)*self.scroll_speed)
        self.dummy_canvas.yview_scroll(y_steps, "units")

    def scrolling_linux(self, event):
        y_steps = self.scroll_speed
        if event.num == 4:
            y_steps *= -1
        self.dummy_canvas.yview_scroll(y_steps, "units")

    def scrollbar_scrolling(self, event):
        region = list(self.dummy_canvas.bbox("all"))
        region[2] = max(self.dummy_canvas.winfo_width(), region[2])
        region[3] = max(self.dummy_canvas.winfo_height(), region[3])
        self.dummy_canvas.configure(scrollregion=region)

    def resize(self, fit=None, height=None, width=None):
        if (fit == "fit_width") or (fit == "fit_all"):
            super().update()
            self.dummy_canvas.config(width=super().winfo_width())
        if (fit == "fit_height") or (fit == "fit_all"):
            super().update()
            self.dummy_canvas.config(height=super().winfo_height())
        if height is not None:
            self.dummy_canvas.config(height=height)
        if width is not None:
            self.dummy_canvas.config(width=width)

    def pack(self, **kwargs):
        self.master_frame.pack(**kwargs)

    def grid(self, **kwargs):
        self.master_frame.grid(**kwargs)

    def place(self, **kwargs):
        self.master_frame.place(**kwargs)

    def pack_forget(self, **kwargs):
        self.master_frame.pack_forget(**kwargs)

    def grid_forget(self, **kwargs):
        self.master_frame.grid_forget(**kwargs)

    def place_forget(self, **kwargs):
        self.master_frame.place_forget(**kwargs)