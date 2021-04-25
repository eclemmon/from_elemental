import tkinter as tk
import settings_gui
import gui
import section_manager

class Main(tk.Tk):
    def __init__(self, sections_manager):
        tk.Tk.__init__(self)
        self.sections_manager = sections_manager
        self.withdraw()
        self.settings = settings_gui.SettingsGUI(self)

    def run(self):
        self.mainloop()

    def run_main_gui(self):
        self.settings.withdraw()
        main_gui = gui.GUI(self, self.sections_manager, self.settings.cell_paths)



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
