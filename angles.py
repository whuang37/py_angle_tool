import tkinter as tk
import math
from PIL import Image, ImageTk

class Application:
    def __init__(self, master):
        self.master = master
        self.master.title("Angle Tool")
        self.canvas = tk.Canvas(self.master, highlightthickness = 0) 
        self.canvas.pack(fill = "both", expand = True)
        
        # open an image from the folder to display on the canvas
        image = ImageTk.PhotoImage(file = "test.jpg")
        imageid = self.canvas.create_image(0, 0, anchor = "nw", image = image)
        self.canvas.lower(imageid)
        self.canvas.image = image # saves a copy of the image for garbage colelction
        
        dimensions = "{0}x{1}".format(image.width(), image.height())
        self.master.geometry(dimensions)
if __name__ == "__main__":
    root = tk.Tk()
    app = Application(root)
    root.mainloop()
