import tkinter as tk
import math
from PIL import Image, ImageTk
from tkinter import filedialog
class Application:
    def __init__(self, master):
        
        self.file_name = tk.StringVar(value = filedialog.askopenfilename())
        self.master = master
        self.master.title("Angle Tool")
        self.canvas = tk.Canvas(self.master, highlightthickness = 0) 
        
        # open an image from the folder to display on the canvas
        im = Image.open(self.file_name.get())
        image = ImageTk.PhotoImage(im)
        imageid = self.canvas.create_image(0, 0, anchor = "nw", image = image)
        self.canvas.lower(imageid)
        self.canvas.image = image # saves a copy of the image for garbage colelction
        self.canvas.pack(fill = "both", expand = True)
        
        dimensions = "{0}x{1}".format(image.width(), image.height())
        self.master.geometry(dimensions)
        
        # binds for initial line creation
        self.canvas.bind("<Button-1>", self.angle_tool)
        
        self.prev_angle = 0
        self.passed = False
        
        self.points = []
        self.old_x = None
        self.old_y = None

    def angle_tool(self, event):
        # first point selected
        coords= (self.canvas.canvasx(event.x), self.canvas.canvasy(event.y))
        old_coords = (self.old_x, self.old_y)
        
        if self.old_x and self.old_y:
            self.canvas.create_line(old_coords, coords, smooth = True, splinesteps = 36, capstyle = "round",
                                fill = "white", width = 5, tag = "line")
        self.old_x, self.old_y = coords
        self.points.append(coords)
        
        if len(self.points) == 2: # if only one line is drawn
            self.canvas.bind("<Motion>", self.calc_angle)
        elif len(self.points) == 3:
            self.canvas.unbind("<Button-1>")
            self.canvas.unbind("<ButtonRelease-1>")
            self.canvas.unbind("<B1-Motion>")
            self.canvas.unbind("<Motion>")
            
            self.canvas.bind("<Button-1>", self.clear_canvas)
        
    def ghost_line(self, event):
        # gray line indicating where angle is
        old_coords = (self.old_x, self.old_y)
        ghost_coords = (self.canvas.canvasx(event.x), self.canvas.canvasy(event.y))
        if self.old_x and self.old_y: 
            self.canvas.delete("ghost")
            self.canvas.create_line(old_coords, ghost_coords, smooth = True, splinesteps = 36, capstyle = "round",
                                fill = "gray", width = 5, tag = "ghost")
        
    def clear_canvas(self, event):
        self.canvas.delete("line")
        self.canvas.delete("angle")
        self.canvas.delete("ghost")
        
        self.curr_angle = None
        
        self.canvas.unbind("<Button-1>")
        self.canvas.bind("<Button-1>", self.angle_tool)
        
    def angle(self, cur_coords):
        # gets atan where origin is placed at mid point
        def atan_angle(a, x_sign, y_sign):
            degree = math.degrees(math.atan2(x_sign*(a[1] - self.points[1][1]), y_sign*(a[0] - self.points[1][0])))
            return degree
        
        first_angle = atan_angle(self.points[0], -1, 1)
        
        # rotates the axises according to where the first angle is
        if (first_angle > 0) & (first_angle <= 90):
            axis_angle = atan_angle(cur_coords, -1, 1)
        elif (first_angle > 90) & (first_angle <= 180):
            axis_angle = atan_angle(cur_coords, 1, -1)
        elif (first_angle < 0) & (first_angle >= -90):
            axis_angle = atan_angle(cur_coords, -1, 1)
        else:
            axis_angle = atan_angle(cur_coords, 1, -1)
            
        if first_angle > 90:
            first_angle = -(180 - first_angle)
        elif first_angle < -90:
            first_angle = -(-180 - first_angle)
            
        # checks if the mouse has passed 180 degrees
        if ((175 < self.prev_angle <= 180) & (-180 <= axis_angle < -175)) or ((175 < axis_angle <= 180) & (-180 <= self.prev_angle < -175)):
            if self.passed == False:
                self.passed = True
            else:
                self.passed = False
                
        # adds 360 if the angle passes 180
        if (self.passed == True) & (axis_angle - first_angle <= 0):
            a = 360
        elif (self.passed == True) & (axis_angle - first_angle > 0):
            a = -360
        else: 
            a = 0 
            
        curr_angle = axis_angle + a - first_angle
        
        if abs(curr_angle) >= 359.00:
            self.passed = False
            a = 0
            
        self.prev_angle = axis_angle
        return abs(curr_angle)
    
    def calc_angle(self, event):
        old_coords = (self.old_x, self.old_y)
        coords = (self.canvas.canvasx(event.x), self.canvas.canvasy(event.y))
        self.curr_angle = self.angle(coords)

        self.canvas.delete("ghost")
        self.canvas.create_line(old_coords, coords,
                                fill = "gray", width = 5, tag = "ghost")
        self.canvas.create_text(coords[0] + 10, coords[1] + 10, fill = "white", font = "Calibri 12",
                                text = str(self.curr_angle), tag = "ghost", anchor = "nw")
        
    def get_angle(self):
        return self.curr_angle

if __name__ == "__main__":
    root = tk.Tk()
    App = Application(root)
    root.mainloop()

