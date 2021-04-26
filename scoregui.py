#!/usr/local/bin/python3

import tkinter as tk
import image_data_loader
import timer
import flashable_label
import cell_assigner
from section_manager import SectionManager
from PIL import ImageTk, Image



class ScoreGUI(tk.Toplevel):
    # configure root
    def __init__(self, root, section_manager, cell_assigner, preroll=5):
        tk.Toplevel.__init__(self)
        self.root = root
        self.protocol("WM_DELETE_WINDOW", root.destroy)
        self.timer = timer.Timer()
        self.preroll = preroll
        self.piece_length = section_manager.get_total_timing()
        self.section_manager = section_manager
        self.image_paths = cell_assigner.cells

        # If click, advance to next image
        self.title('Image Viewer App')
        self.bind("<Button-1>", self.on_click)

        # Set an image
        self.image_path = None
        img = self.get_new_image()
        self.label = tk.Label(self, image=img, pady=5)
        self.label.grid(row=1, column=0, columnspan=2)
        self.set_new_image()

        # Initialize and run timer
        self.timer_display = flashable_label.FlashableLabel(self, text=self.timer.get_formatted_time(),
                                                            font=("Rosewood Std Regular", 50))
        self.timer_display.grid(row=0, column=0)
        self.update_timer()

        # Set section text
        self.section = flashable_label.FlashableLabel(self, text=self.section_manager.get_current_section_name(),
                                                      font=("Rosewood Std Regular", 50))
        self.section.grid(row=0, column=1)
        self.after(self.section_manager.get_current_section_timing()*1000, self.update_section)

        # Set kill button
        self.close_program = tk.Button(self, text="QUIT", font=("Rosewood Std Regular", 50),
                                       command=self.close, border=20, activeforeground="black", padx=7)
        self.close_program.grid(row=2, columnspan=2)
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
            self.timer_display.config(text=self.timer.get_formatted_time())
            self.timer.increment()
            self.after(1000, self.update_timer)

    def on_click(self, event):
        self.set_new_image()

    def end_of_piece_protocol(self):
        end_seconds = 10
        self.timer_display.flash(flashes=end_seconds*4)
        self.after(end_seconds*1000, func=root.destroy)

    def update_section(self):
        self.section_manager.next()
        duration_of_section = self.section_manager.get_current_section_timing()
        self.section.config(text=self.section_manager.get_current_section_name())
        self.section.flash(flashes=10)
        self.after(duration_of_section*1000, func=self.update_section)

    def start_from(self, section_value):
        timing = self.section_manager.start_from_section(section_value)
        self.timer.set_time(timing)

    def close(self):
        self.after(0, func=root.destroy)




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


