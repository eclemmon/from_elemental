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
        self.font_text = "Avenir Next"
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
    DURATION = 600

    section_instructions = (
        "Electronics Introduction\nTacet",
        "Tacet, then after 30 seconds imitate electronics",
        "Play whole or part of cell. Introduce rarely, then with increasing frequency",
        "(apply to cells + electronics only):\n\nACTIONS:\n• Imitate\n• Embellish\n\nANTI-ACTIONS:\n• Obfuscate",
        "(apply to all including players):\n\nActions:\n• Imitate\n• Embellish\n\nAnti-Actions:\n• Obfuscate",
        "(apply to all including players):\n\nActions:\n• Imitate\n• Embellish\n• Improvised "
        "response\n\nAnti-Actions:\n• Obfuscate\n• Contrast\n\nIncrease rate of actions / anti-actions progressively",
        "(cosmos interjects):\n\nRespond with either:\n• Panic, or\n• Calmness",
        "Actions (gradual):\n\n• Align with electronics (i.e. unison, parallel)\n• harmonics with electronics"
    )
    sections = [("Cosmic", generate_timings(40, DURATION), section_instructions[0]),
                ("Element Introduction (tacet)", 30, section_instructions[1]),
                ("Element Introduction", generate_timings(90, DURATION)-30, section_instructions[1]),
                ("Life Forms", generate_timings(90, DURATION), section_instructions[2]),
                ("Emergence of Individuals", generate_timings(40, DURATION), section_instructions[3]),
                ("Emergence of Collective", generate_timings(40, DURATION), section_instructions[4]),
                ("Conflict between collective and individual", generate_timings(50, DURATION), section_instructions[5]),
                ("INCISION", generate_timings(10, DURATION), section_instructions[6]),
                ("Trancendence: COSMIC RE-FRAMED", generate_timings(60, DURATION), section_instructions[7])]
    sm = section_manager.SectionManager(sections)
    # print(generate_timings(10, 600))
    # print(sm.get_total_timing())
    main = Main(sm)
    main.run()
