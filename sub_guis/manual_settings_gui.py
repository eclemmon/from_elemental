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


class ManualSettingsGui(tk.Toplevel):
    def __init__(self, root):
        self.root = root
        tk.Toplevel.__init__(self)
        self.protocol("WM_DELETE_WINDOW", root.destroy)
        self.title('Manually select cells across sections')
        self.grid_no = 2
        self.radio_button_values = {}
        self.cell_paths = None

        if self.root.instrument == "violin":
            path = pathlib.Path(__file__).parent
            self.path = os.path.join(path, "../violin_cells/")
        else:
            path = pathlib.Path(__file__).parent
            self.path = os.path.join(path, "../cello_cells/")
        print(self.path)
        self.file_names = image_data_loader.get_image_names(self.path)

        # Initialize instructions
        instructions_text = """
        Violinist hits the 'randomize' button, 
        and tells the cellist which cells have been selected. 
        The cello player then selects the remaining cells.
        """
        self.instructions = tk.Label(self, text=instructions_text,
                                     font=("Rosewood Std Regular", 25), pady=10, padx=10)
        self.instructions.grid(row=0, columnspan=3)

        # Initialize labels
        self.is_selected = tk.Label(self, text="Selected", font=("Rosewood Std Regular", 25), pady=10, padx=10)
        self.is_selected.grid(row=1, column=1)
        self.is_not_selected = tk.Label(self, text="Not Selected", font=("Rosewood Std Regular", 25), pady=10, padx=10)
        self.is_not_selected.grid(row=1, column=2)

        # Build radio buttons
        for counter, value in enumerate(self.file_names):
            button_val = tk.IntVar()
            label = tk.Label(self, text=value, font=("Rosewood Std Regular", 15), pady=5, padx=5)
            label.grid(row=counter+2, column=0, sticky=tk.E)
            radio_button1 = tk.Radiobutton(self, text="", variable=button_val, value=1,
                                           font=("Rosewood Std Regular", 10), pady=5, selectcolor="Black")
            radio_button1.grid(row=counter + 2, column=1)
            radio_button2 = tk.Radiobutton(self, text="", variable=button_val, value=2,
                                           font=("Rosewood Std Regular", 10), pady=5, selectcolor="Black")
            radio_button2.grid(row=counter + 2, column=2)
            self.radio_button_values[value] = button_val
            self.grid_no += 1

        # Build command buttons
        self.randomize = tk.Button(self, text="Randomize", command=self.random_select, font=("Rosewood Std Regular", 25), padx=7)
        self.randomize.grid(row=self.grid_no, column=1)
        self.submit = tk.Button(self, text="Submit", command=self.on_submit, font=("Rosewood Std Regular", 25), padx=7)
        self.submit.grid(row=self.grid_no, column=2)

        # Padding bottom
        self.padding1 = tk.Label(self, pady=5).grid(row=self.grid_no+1, columnspan=3)

    def random_select(self):
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
        result = []
        for key, val in self.radio_button_values.items():
            if val.get() == 1:
                result.append(key)
        self.cell_paths = cell_assigner.CellAssigner(image_data_loader.get_these_images(self.path, result))
        self.root.run_score_gui()



if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    mansetgui = ManualSettingsGui(root)
    root.mainloop()
