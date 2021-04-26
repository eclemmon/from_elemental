import tkinter as tk
import random
import image_data_loader


class ManualSettingsGui(tk.Toplevel):
    def __init__(self, root):
        self.root = root
        tk.Toplevel.__init__(self)
        self.protocol("WM_DELETE_WINDOW", root.destroy)
        self.title('Manually select cells across sections')
        self.radio_button_values = {

        }

        # Initialize instructions
        instructions_text = """
        Violinist hits the 'randomize' button, and tells the cellist which cells have been selected. 
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
        for counter, value in enumerate(image_data_loader.get_image_names("/Users/ericlemmon/Desktop/NMFS_collab/score_gui/violin_cells/")):
            button_val = tk.IntVar()
            label = tk.Label(self, text=value, font=("Rosewood Std Regular", 25), pady=10, padx=10)
            label.grid(row=counter+2, column=0)
            radio_button1 = tk.Radiobutton(self, text="", variable=button_val, value=1,
                                           font=("Rosewood Std Regular", 20), pady=10)
            radio_button1.grid(row=counter + 2, column=1)
            radio_button2 = tk.Radiobutton(self, text="", variable=button_val, value=2,
                                           font=("Rosewood Std Regular", 20), pady=10)
            radio_button2.grid(row=counter + 2, column=2)

    def random_select(self):
        pass


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    mansetgui = ManualSettingsGui(root)
    root.mainloop()
