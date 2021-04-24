import tkinter as tk
import image_data_loader
import timer
import flashable_label
from PIL import ImageTk, Image



class GUI(tk.Tk):
    # configure root
    def __init__(self, minutes=7, seconds=30, preroll=5):
        tk.Tk.__init__(self)

        self.timer = timer.Timer()
        self.preroll=preroll
        self.piece_length = minutes * 60 + seconds

        # If click, advance to next image
        self.title('Image Viewer App')
        # self.button = tk.Button(master=self, text="Next", command=self.set_new_image)
        # self.button.pack(side="bottom", ipady=10, ipadx=10, pady=10)
        self.bind("<Button-1>", self.on_click)

        # Set an image
        self.image_path = None
        img = self.get_new_image()
        self.label = tk.Label(self, image=img)
        self.label.pack(expand="yes", side="bottom", pady=20)
        self.set_new_image()

        # Initialize and run timer
        self.timer_display = tk.Label(self, text=self.timer.get_formatted_time(), width=200, height=200, font=("Rosewood Std Regular", 100))
        self.timer_display.pack(side="bottom", ipady=10, pady=10)
        self.update_timer()


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
        self.after(10*1000, func=self.destroy)










if __name__ == '__main__':
    gui = GUI(0, 5)
    gui.state('zoomed')
    gui.mainloop()


