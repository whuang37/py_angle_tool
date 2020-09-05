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
        
        self.prev_angle = 0
        self.passed = False
        
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
        m = (self.mid_coords[1] - self.f_coords[1]) / (self.mid_coords[0] - self.f_coords[0])

        # calculations done below are from the ax + by = c line form
        # from the existing line
        a = -m
        b = 1
        c = -self.mid_coords[1] + m * self.mid_coords[0]
        
        # coords of closest point on the line to cur coords
        x = (b*(b*cur_coords[0] - a*cur_coords[1]) - a*c)/(a**2 + b**2)
        y = (a*(-b*cur_coords[0] + a*cur_coords[1]) - b*c)/(a**2 + b**2)
        
        close_coords = (x,y)
        
        def dist(a, b):
            dist = math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)
            return dist
        
        dist1 = dist(close_coords, cur_coords)
        dist2 = dist(cur_coords, self.mid_coords)
        
        angle = math.degrees(math.acos(dist1/dist2))
        return angle
    
    def calc_angle(self, event):
        cur_coords = (self.canvas.canvasx(event.x), self.canvas.canvasy(event.y))

        def atan_angle(a, x_sign, y_sign):
            degree = math.degrees(math.atan2(x_sign*(a[1] - self.mid_coords[1]), y_sign*(a[0] - self.mid_coords[0])))
            return degree
        
        first_angle = atan_angle(self.f_coords, -1, 1)
        
        if (first_angle > 0) & (first_angle <= 90):
            axis_angle = atan_angle(cur_coords, -1, 1)
        elif (first_angle > 90) & (first_angle <= 180):
            axis_angle = atan_angle(cur_coords, 1, -1)
        elif (first_angle < 0) & (first_angle >= -90):
            axis_angle = atan_angle(cur_coords, -1, 1)
        else:
            axis_angle = atan_angle(cur_coords, 1, -1)
            
        if ((175 < self.prev_angle <= 180) & (-180 <= axis_angle < -175)) or ((175 < axis_angle <= 180) & (-180 <= self.prev_angle < -175)):
            if self.passed == False:
                self.passed = True
            else:
                self.passed = False
                
        if (self.passed == True) & (axis_angle <= 0):
            a = 360
        elif (self.passed == True) & (axis_angle > 0):
            a = -360
        else: 
            a = 0 
        
        curr_angle = axis_angle + a - first_angle
        
        if abs(curr_angle) >= 360:
            self.passed = False
            a = 0
        
        print(abs(curr_angle))
        print(self.passed)
        self.prev_angle = axis_angle

if __name__ == "__main__":
    root = tk.Tk()
    app = Application(root)
    root.mainloop()
