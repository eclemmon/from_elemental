#!/usr/local/bin/python3

import tkinter as tk
import image_data_loader
import timer
import flashable_label
from section_manager import SectionManager
from PIL import ImageTk, Image



class GUI(tk.Tk):
    # configure root
    def __init__(self, section_manager, preroll=5):
        tk.Tk.__init__(self)

        self.timer = timer.Timer()
        self.preroll = preroll
        self.piece_length = section_manager.get_total_timing()
        self.section_manager = section_manager

        # If click, advance to next image
        self.title('Image Viewer App')
        self.bind("<Button-1>", self.on_click)

        # Set an image
        self.image_path = None
        img = self.get_new_image()
        self.label = tk.Label(self, image=img)
        self.label.grid(row=1, column=0, columnspan=2)
        self.set_new_image()

        # Initialize and run timer
        self.timer_display = flashable_label.FlashableLabel(self, text=self.timer.get_formatted_time(), font=("Rosewood Std Regular", 50))
        self.timer_display.grid(row=0, column=0)
        self.update_timer()

        # Set section text
        self.section = flashable_label.FlashableLabel(self, text=self.section_manager.get_current_section_name(), font=("Rosewood Std Regular", 50))
        self.section.grid(row=0, column=1)
        self.after(self.section_manager.get_current_section_timing()*1000, self.update_section)

    def resize_image(self, image):
        ratio = min(1300/image.width, 680/image.height)
        return image.resize((int(image.width*ratio), int(image.height*ratio)), Image.ANTIALIAS)

    def get_new_image(self):
        image_path = image_data_loader.get_random_image_path()
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
        self.after(end_seconds*1000, func=self.destroy)

    def update_section(self):
        self.section_manager.next()
        duration_of_section = self.section_manager.get_current_section_timing()
        self.section.config(text=self.section_manager.get_current_section_name())
        self.section.flash(flashes=10)
        self.after(duration_of_section*1000, func=self.update_section)

    def start_from(self, section_value):
        timing = self.section_manager.start_from_section(section_value)
        self.timer.set_time(timing)




if __name__ == '__main__':
    sections = [("Cosmic", 10),
                ("Element Introduction", 90),
                ("Life Forms", 90),
                ("Emergence of Individuals", 40),
                ("Emergence of collective", 40),
                ("Conflict between collective and individual", 50),
                ("INCISION", 10),
                ("Trancendence: COSMIC RE-FRAMED", 60)]
    section_manager = SectionManager(sections)
    gui = GUI(section_manager)
    gui.state('zoomed')
    gui.mainloop()


