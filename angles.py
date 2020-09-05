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
        
        # binds for initial line creation
        self.canvas.bind("<Button-1>", self.set_start)
        
    def set_start(self, event):
        self.f_coords= (self.canvas.canvasx(event.x), self.canvas.canvasy(event.y))
        
        self.canvas.bind("<Motion>", self.f_ghost_line)
        self.canvas.unbind("<Button-1>")
        self.canvas.bind("<Button-1>", self.create_first_line)
        
    def f_ghost_line(self, event):
        ghost_coords = (self.canvas.canvasx(event.x), self.canvas.canvasy(event.y))
        
        self.canvas.delete("ghost")
        self.canvas.create_line(ghost_coords, self.f_coords,
                                fill = "gray", width = 5, tag = "ghost")
        
    def create_first_line(self, event):
        self.mid_coords = (self.canvas.canvasx(event.x), self.canvas.canvasy(event.y))
        self.canvas.create_line(self.f_coords, self.mid_coords, 
                                fill = "black", width = 5, tag = "first_line")
        
        self.canvas.unbind("<Button-1>")
        self.canvas.bind("<ButtonRelease-1>", self.create_second_line)
        self.canvas.unbind("<Motion>")
        self.canvas.bind("<Motion>", self.l_ghost_line)
        self.canvas.bind("<B1-Motion>", self.calc_angle)
    def l_ghost_line(self, event):
        ghost_coords = (self.canvas.canvasx(event.x), self.canvas.canvasy(event.y))
        
        self.canvas.delete("ghost")
        self.canvas.create_line(ghost_coords, self.mid_coords,
                                fill = "gray", width = 5, tag = "ghost")
        
    def create_second_line(self, event):
        self.l_coords = (self.canvas.canvasx(event.x), self.canvas.canvasy(event.y))
        self.canvas.create_line(self.mid_coords, self.l_coords, 
                                fill = "black", width = 5, tag = "first_line")
        
    def angle(self, cur_coords):
        # slope of existing line
        print(self.mid_coords, self.f_coords)
        m = (self.mid_coords[1] - self.f_coords[1]) / (self.mid_coords[0] - self.f_coords[0])

        # calculations done below are from the ax + by = c line form
        # from the existing line
        a = -m
        b = 1
        c = -self.mid_coords[1] + m * self.mid_coords[0]
        
        # distance of line from cur coords to existing line
        distance1 = abs(a * cur_coords[0] + b * cur_coords[1] + c) / math.sqrt(a**2 + b**2)
        
        # distance from cur coords to mid point
        x_diff = cur_coords[0] - self.mid_coords[0]
        y_diff = cur_coords[1] - self.mid_coords[1]
        distance2 = math.sqrt(x_diff**2 + y_diff**2)
        angle = math.degrees(math.asin(distance1 / distance2))
        
        return angle
    
    def calc_angle(self, event):
        cur_coords = (self.canvas.canvasx(event.x), self.canvas.canvasy(event.y))
        
        angle = self.angle(cur_coords)
        print(angle)

if __name__ == "__main__":
    root = tk.Tk()
    app = Application(root)
    root.mainloop()
