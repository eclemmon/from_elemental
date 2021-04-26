import tkinter as tk
from sub_guis import scoregui, server_settings_gui, instrument_and_network_settings_gui, manual_settings_gui
import section_manager


class Main(tk.Tk):
    def __init__(self, sections_manager):
        tk.Tk.__init__(self)
        self.sections_manager = sections_manager
        self.withdraw()
        self.instrument = None
        self.settings = None
        self.score_gui = None
        self.instrument_net_settings = instrument_and_network_settings_gui.InstrumentNetworkSettingsGui(self)

    def run(self):
        self.mainloop()

    def run_score_gui(self):
        self.settings.withdraw()
        self.score_gui = scoregui.ScoreGUI(self, self.sections_manager, self.settings.cell_paths)

    def get_settings_automatically_via_local_network(self):
        self.instrument_net_settings.withdraw()
        self.settings = server_settings_gui.ServerSettingsGUI(self)

    def manually_set_settings(self):
        self.instrument_net_settings.withdraw()
        self.settings = manual_settings_gui.ManualSettingsGui(self)




if __name__ == "__main__":
    sections = [("Cosmic", 10),
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
