"""
Main Module
"""

__author__ = "Eric Lemmon"
__copyright__ = "Copyright 2021, Eric Lemmon"
__credits = ["Eric Lemmon, Anne Sophie Andersen"]
__version__ = "0.9"
__maintainer__ = "Eric Lemmon"
__email__ = "ec.lemmon@gmail.com"
__status__ = "Testing"


import tkinter as tk
import section_manager
import math
from sub_guis import score_gui
from sub_guis import server_settings_gui
from sub_guis import instrument_and_network_settings_gui
from sub_guis import manual_settings_gui


class Main(tk.Tk):
    def __init__(self, sections_manager):
        """
        Initializes the main program as a tkinter root.
        :param sections_manager: Sections manager controls the length of sections and the text displayed during each
        at the top of the main score GUI.
        """
        tk.Tk.__init__(self)
        self.sections_manager = sections_manager
        self.instrument = None
        self.settings = None
        self.score_gui = None
        self.preroll = None
        self.section_start = None
        self.image_trigger = None
        # Set some global styles
        self.color_1 = "#0A2463"
        self.color_2 = "#FFFAFF"
        self.color_3 = "#009FFD"
        self.font_header = "THE LED DISPLAY ST"
        self.font_text = "LOTTE PAPERFANG"
        self.instrument_net_settings = instrument_and_network_settings_gui.\
            InstrumentNetworkSettingsGui(self, color_1=self.color_1, color_2=self.color_2, color_3=self.color_3,
                                         font_header=self.font_header, font_text=self.font_text)
        self.withdraw()

    def run(self):
        """
        Initializes tkinter's main loop.
        :return: None
        """
        self.mainloop()

    def run_score_gui(self):
        """
        Withdraws the settings windows and initializes the main score window of the piece.
        :return: None
        """
        self.settings.withdraw()
        self.score_gui = score_gui.ScoreGUI(self, self.sections_manager, self.settings.cell_paths,
                                            preroll=self.preroll, section_start=self.section_start,
                                            image_trigger=self.image_trigger, color_1=self.color_1,
                                            color_2=self.color_2, color_3=self.color_3, font_header=self.font_header,
                                            font_text=self.font_text)

    def get_settings_automatically_via_local_network(self):
        """
        Withdraws the instrument and network setting window and initializes the GUI to distribute scores automatically.
        :return: None
        """
        self.instrument_net_settings.withdraw()
        self.settings = server_settings_gui.ServerSettingsGUI(self, color_1=self.color_1, color_2=self.color_2,
                                                              color_3=self.color_3, font_header=self.font_header,
                                                              font_text=self.font_text)

    def manually_set_settings(self):
        """
        Withdraws the instrument and network setting window and initializes the GUI to manually set the the
        selected scores
        :return: None
        """
        self.instrument_net_settings.withdraw()
        self.settings = manual_settings_gui.ManualSettingsGui(self, color_1=self.color_1, color_2=self.color_2,
                                                              color_3=self.color_3, font_header=self.font_header,
                                                              font_text=self.font_text)

def generate_timings(old_init_time, new_total_time):
    return math.ceil(old_init_time / 420 * new_total_time)

if __name__ == "__main__":

    sections = [("Cosmic", generate_timings(40, 600), "Electronics Introduction\nTacet"),
                ("Element Introduction", generate_timings(90, 600), "lorum\nipsum"),
                ("Life Forms", generate_timings(90, 600), "lorum\nipsum"),
                ("Emergence of Individuals", generate_timings(40, 600), "lorum\nipsum"),
                ("Emergence of collective", generate_timings(40, 600), "lorum\nipsum"),
                ("Conflict between collective and individual", generate_timings(50, 600), "lorum\nipsum"),
                ("INCISION", generate_timings(10, 600), "lorum\nipsum"),
                ("Trancendence: COSMIC RE-FRAMED", generate_timings(60, 600), "lorum\nipsum")]
    sm = section_manager.SectionManager(sections)
    # print(generate_timings(10, 600))
    # print(sm.get_total_timing())
    main = Main(sm)
    main.run()
