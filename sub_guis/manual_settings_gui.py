"""
Manual Setting GUI Module
"""

__author__ = "Eric Lemmon"
__copyright__ = "Copyright 2021, Eric Lemmon"
__credits = ["Eric Lemmon, Anne Sophie Andersen"]
__version__ = "0.9"
__maintainer__ = "Eric Lemmon"
__email__ = "ec.lemmon@gmail.com"
__status__ = "Testing"

import tkinter as tk
import random
import image_data_loader
import cell_assigner
import pathlib
import os
import main
import section_manager


class ManualSettingsGui(tk.Toplevel):
    def __init__(self, root):
        """
        Initializes the manual settings GUI.
        :param root: the root of the tkinter GUI app, comes from main.py.
        """
        self.root = root
        tk.Toplevel.__init__(self)
        self.protocol("WM_DELETE_WINDOW", root.destroy)
        self.title('Manually select cells across sections')
        self.grid_no = 2
        self.radio_button_values = {}
        self.cell_paths = None

        # Determine the image paths based on the instrument selected in root.instrument
        self.path = image_data_loader.get_path_by_instrument_name(root.instrument)
        self.file_names = image_data_loader.get_image_names(self.path)

        # Initialize instructions
        instructions_text = [
        "Violinist hits the 'randomize' button,",
        "and tells the cellist which cells have been selected.",
        "The cello player then selects the remaining cells."
        ]
        self.header_frame = tk.Frame(self, bg="light steel blue")
        self.header_frame.grid(row=0, columnspan=3, sticky="ew")
        for i in range(len(instructions_text)):
            instructions = tk.Label(self.header_frame, text=instructions_text[i],
                                         font=("Rosewood Std Regular", 25), fg="snow", bg="light steel blue", padx=5)
            instructions.grid(row=i)
            self.header_frame.grid_columnconfigure(0, weight=1)
            self.header_frame.grid_columnconfigure(2, weight=1)

        # Initialize Selected labels
        self.selected_frame = tk.Frame(self, bg="snow")
        self.selected_frame.grid(row=1, columnspan=3, sticky="ew")
        self.is_selected = tk.Label(self.selected_frame, text="Selected", fg="steel blue", bg="snow",
                                    font=("Rosewood Std Regular", 25), pady=10, padx=10)
        self.is_selected.grid(row=0, column=1, sticky="w")
        self.is_not_selected = tk.Label(self.selected_frame, text="Not Selected", fg="steel blue", bg="snow",
                                        font=("Rosewood Std Regular", 25), pady=10, padx=10)
        self.is_not_selected.grid(row=0, column=2, sticky="w")
        self.selected_frame.grid_columnconfigure(0, weight=1)

        # Build radio buttons
        self.buttons_frame = tk.Frame(self, bg="light steel blue")
        self.buttons_frame.grid(row=2, columnspan=3, sticky="ew")
        for counter, value in enumerate(self.file_names):
            button_val = tk.IntVar()
            label = tk.Label(self.buttons_frame, text=value, font=("Rosewood Std Regular", 15),
                             fg="snow", bg="light steel blue", pady=5, padx=22)
            label.grid(row=counter, column=1, sticky=tk.E)
            radio_button1 = tk.Radiobutton(self.buttons_frame, text="", variable=button_val, value=1,
                                           font=("Rosewood Std Regular", 10), pady=5, selectcolor="Black",
                                           fg="snow", bg="light steel blue",)
            radio_button1.grid(row=counter, column=2)
            radio_button2 = tk.Radiobutton(self.buttons_frame, text="", variable=button_val, value=2,
                                           font=("Rosewood Std Regular", 10), pady=5, selectcolor="Black",
                                           fg="snow", bg="light steel blue",)
            radio_button2.grid(row=counter, column=3)

            self.radio_button_values[value] = button_val
            self.grid_no += 1
        self.buttons_frame.grid_columnconfigure(2, weight=1)
        self.buttons_frame.grid_columnconfigure(3, weight=1)


        # Build command buttons
        self.commands_frame = tk.Frame(self, bg="snow")
        self.commands_frame.grid(row=3, columnspan=3, sticky='ew')
        self.randomize = tk.Button(self.commands_frame, text="Randomize", command=self.random_select,
                                   font=("Rosewood Std Regular", 25), padx=7, fg="steel blue", bg="snow")
        self.randomize.grid(row=0, column=1)
        self.submit = tk.Button(self.commands_frame, text="Submit", command=self.on_submit,
                                font=("Rosewood Std Regular", 25), padx=7, fg="steel blue", bg="snow")
        self.submit.grid(row=0, column=2)
        self.commands_frame.grid_columnconfigure(0, weight=1)
        self.commands_frame.grid_columnconfigure(3, weight=1)

        # Padding bottom
        self.padding1 = tk.Label(self.commands_frame, pady=5, bg="snow")
        self.padding1.grid(row=1, columnspan=3)

    def random_select(self):
        """
        Randomly selects the available buttons when pressed. Once half the number of options + 1 have beeen selected
        the other half are selected with the other option by default.
        :return: None
        """
        selected = 0
        not_selected = 0
        half = (len(self.file_names) // 2 + 1)
        for val in self.radio_button_values.values():
            result = random.choice([1, 2])
            if selected == half or not_selected == half:
                if selected == half:
                    val.set(2)
                else:
                    val.set(1)
            else:
                if result == 1:
                    selected += 1
                    val.set(result)
                else:
                    not_selected += 1
                    val.set(result)

    def on_submit(self):
        """
        On submit gets the selected image paths and builds a CellAssigner object, which are then used
        when the score GUI runs as the randomly selected images.
        :return: None
        """
        result = []
        for key, val in self.radio_button_values.items():
            if val.get() == 1:
                result.append(key)
        self.cell_paths = cell_assigner.CellAssigner(image_data_loader.get_these_images(self.path, result))
        self.root.run_score_gui()


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
    root = main.Main(sm)
    root.withdraw()
    mansetgui = ManualSettingsGui(root)
    root.mainloop()
