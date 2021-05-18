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
        self.instrument_net_settings = instrument_and_network_settings_gui.InstrumentNetworkSettingsGui(self)
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
                                            image_trigger=self.image_trigger)

    def get_settings_automatically_via_local_network(self):
        """
        Withdraws the instrument and network setting window and initializes the GUI to distribute scores automatically.
        :return: None
        """
        self.instrument_net_settings.withdraw()
        self.settings = server_settings_gui.ServerSettingsGUI(self)

    def manually_set_settings(self):
        """
        Withdraws the instrument and network setting window and initializes the GUI to manually set the the
        selected scores
        :return: None
        """
        self.instrument_net_settings.withdraw()
        self.settings = manual_settings_gui.ManualSettingsGui(self)


if __name__ == "__main__":
    sections = [("Cosmic", 40),
                ("Element Introduction", 90),
                ("Life Forms", 90),
                ("Emergence of Individuals", 40),
                ("Emergence of collective", 40),
                ("Conflict between collective and individual", 50),
                ("INCISION", 10),
                ("Trancendence: COSMIC RE-FRAMED", 60)]
    sm = section_manager.SectionManager(sections)
    main = Main(sm)
    main.run()
