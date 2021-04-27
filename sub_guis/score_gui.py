"""
Score GUI Module
"""

__author__ = "Eric Lemmon"
__copyright__ = "Copyright 2021, Eric Lemmon"
__credits = ["Eric Lemmon, Anne Sophie Andersen"]
__version__ = "0.9"
__maintainer__ = "Eric Lemmon"
__email__ = "ec.lemmon@gmail.com"
__status__ = "Testing"


import tkinter as tk
import image_data_loader
import timer
import cell_assigner
from section_manager import SectionManager
from sub_guis import flashable_label
from PIL import ImageTk, Image



class ScoreGUI(tk.Toplevel):
    # configure root
    def __init__(self, root, section_manager, cell_assigner, preroll=5, section_start=1):
        tk.Toplevel.__init__(self)
        self.root = root
        self.protocol("WM_DELETE_WINDOW", root.destroy)
        width = str(self.winfo_screenwidth())
        height = str(self.winfo_screenheight())
        self.geometry("{}x{}".format(width, height))
        self.timer = timer.Timer()
        self.preroll = timer.Timer(preroll)
        self.piece_length = section_manager.get_total_timing()
        self.section_manager = section_manager
        self.start_from(section_start)
        self.image_paths = cell_assigner.cells
        self.first_section = True

        # If click, advance to next image
        self.title('Image Viewer App')

        # Set an image
        self.image_path = None
        if section_start == 1:
            text = "### TACET ###"
        else:
            text = ""
        self.label = tk.Label(self, text=text, pady=5, font=("Rosewood Std Regular", 50))
        self.label.grid(row=1, column=0, columnspan=2)

        # Initialize and run timer
        self.timer_display = flashable_label.FlashableLabel(self, text=self.preroll.get_formatted_time(),
                                                            font=("Rosewood Std Regular", 50))
        self.timer_display.grid(row=0, column=0)
        self.update_timer()

        # Set section text
        self.section = flashable_label.FlashableLabel(self, text="PRE-ROLL",
                                                      font=("Rosewood Std Regular", 50))
        self.section.grid(row=0, column=1)
        self.after((self.preroll.get_time()+1)*1000, self.update_section)

        # Set kill button
        self.close_program = tk.Button(self, text="QUIT", font=("Rosewood Std Regular", 50),
                                       command=self.close, border=20, activeforeground="black", padx=7)
        self.close_program.grid(row=2, column=0)
        # Set next button
        self.next_button = tk.Button(self, text="NEXT CELL", font=("Rosewood Std Regular", 50),
                                     command=self.on_click, border=20, activeforeground="black", padx=7)
        self.next_button.grid(row=2, column=1)
        self.padding = tk.Label(self, pady=5).grid(row=3, columnspan=2)

    def resize_image(self, image):
        ratio = min(1300/image.width, 680/image.height)
        return image.resize((int(image.width*ratio), int(image.height*ratio)), Image.ANTIALIAS)

    def get_new_image(self):
        image_path = image_data_loader.select_random_image(self.image_paths)
        print(self.image_path, image_path)
        if image_path == self.image_path:
            print("SAME PATH!")
            self.after(ms=0, func=self.set_new_image)
        else:
            self.image_path = image_path
            new_image = Image.open(image_path)
            print(new_image)
            return ImageTk.PhotoImage(self.resize_image(new_image))

    def set_new_image(self):
        new_image = self.get_new_image()
        self.label.image = new_image
        self.label.config(image=new_image)

    def update_timer(self):
        if self.timer.get_time() == self.piece_length:
            self.timer_display.config(text="THE PIECE IS ENDING")
            self.after(0, self.end_of_piece_protocol)
        else:
            if self.preroll.get_time() > 0:
                self.timer_display.config(text=self.preroll.get_formatted_time())
                self.preroll.decrement()
            else:
                self.timer_display.config(text=self.timer.get_formatted_time())
                self.timer.increment()
            self.after(1000, self.update_timer)

    def on_click(self):
        if self.section_manager.current_section == 1:
            pass
        else:
            self.label.config(text="")
            self.set_new_image()

    def end_of_piece_protocol(self):
        end_seconds = 10
        self.timer_display.flash(flashes=end_seconds*4)
        self.after(end_seconds*1000, func=root.destroy)

    def update_section(self):
        if self.first_section == True:
            duration_of_section = self.section_manager.get_current_section_timing()
            self.after(duration_of_section * 1000, func=self.update_section)
            self.section.config(text=self.section_manager.get_current_section_name())
            self.section.flash(flashes=10)
            self.first_section = False
        else:
            self.section_manager.next()
            duration_of_section = self.section_manager.get_current_section_timing()
            self.section.config(text=self.section_manager.get_current_section_name())
            self.section.flash(flashes=10)
            self.after(duration_of_section*1000, func=self.update_section)

    def start_from(self, section_value):
        timing = self.section_manager.start_from_section(section_value)
        self.timer.set_time(timing)

    def close(self):
        self.after(0, func=self.root.destroy)




if __name__ == '__main__':
    root = tk.Tk()
    root.withdraw()
    sections = [("Cosmic", 10),
                ("Element Introduction", 90),
                ("Life Forms", 90),
                ("Emergence of Individuals", 40),
                ("Emergence of collective", 40),
                ("Conflict between collective and individual", 50),
                ("INCISION", 10),
                ("Trancendence: COSMIC RE-FRAMED", 60)]
    section_manager = SectionManager(sections)
    cells = cell_assigner.CellAssigner(image_data_loader.get_image_paths())
    gui = ScoreGUI(root, section_manager, cells)
    gui.state('zoomed')
    root.mainloop()


