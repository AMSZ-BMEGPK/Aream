from copy import deepcopy
import tkinter as tk
from math import cos, radians, sin, sqrt, atan, asin, pi, degrees
from tkinter.constants import ANCHOR, CENTER, FALSE, NO, TRUE
from PIL import ImageTk,Image
import keyboard
from itertools import cycle
from shapely.ops import unary_union 
from shapely.geometry import Polygon
import numpy as np
WIDTH = 30
R1 = 20 # radius of semicircle (represenatation)
R2 = 20 # radius of quarter_circle (represenatation)
EPSILON = 10
STICKY = True
SCALE = 1.25
from shapes import Rectangle, Arc, Shapes, dist, RightTriangle, visual_grid

#TODO: Overlapping not recognized while alignig rects
#TODO: X-label elúszik a canvas mozgatásakor...

class shapeBuilder(tk.Canvas):
    def __init__(self, root, sb_sm):
        super().__init__(root, bd=0, bg=root.colors["secondary_color"],highlightthickness=0)
        self.root=root
        self.sb_sm = sb_sm #own side menu
        self.scale = 10 #scale between drawing and given value
        self.rectangles = []
        self.arcs = []
        self.rightTriangles = []
        self.negatives = []
        self.shapes = Shapes(self,self.rectangles,self.arcs,self.rightTriangles)
        self.clipboard = []
        self.Xcenter = 400
        self.Ycenter = 300
        self.canvas_width = 800
        self.canvas_height = 600
        self.scale_factor = SCALE

        #########* Basic constants #########
        self.current = None
        self.isMoving=False
        self.width1 = WIDTH # rectangle
        self.height1 = WIDTH # rectangle
        self.width2 = WIDTH # triangle
        self.height2 = WIDTH # triangle
        self.r1 = R1 # quarter_circle
        self.r2 = R2 # semi_cricle
        self.last_click_pos = None
        self.starting_pos = None #selecting multiple objects
        self.selecting_area = self.create_rectangle(0,0,0,0)
        self.selected = []
        self.rotation_happend = False #by rotation should release() not trigger
        self.negativ_in_wrong_position = False
        self.active_shape = "Rectangle"
        self.possible_shape_list = ["Rectangle","Semicircle","quarter_circle", "rightTriangle"]
        self.possible_shapes = cycle(self.possible_shape_list)
        next(self.possible_shapes)

        #############* Creating objects for side menu ##############
        # self.place_holder = tk.Label(self.sb_sm,text="",width=30, bg=self.sb_sm["background"], fg=root.colors["text_color"])
        #Gege megoldása az eredményekre: self.label = tk.Label(self.sb_sm,text="EMPTY LABEL", bg=self.sb_sm["background"], fg=root.colors["text_color"])
        # self.results_label = tk.Label(self.sb_sm,text="results label", bg=self.sb_sm["background"], fg=root.colors["text_color"])
        self.l_width = tk.Label(self.sb_sm,text="x pozíció:", bg=self.sb_sm["background"], fg=root.colors["text_color"])
        self.l_height = tk.Label(self.sb_sm,text="y pozíció:", bg=self.sb_sm["background"], fg=root.colors["text_color"])
        self.l_unit1 = tk.Label(self.sb_sm,text=root.unit, bg=self.sb_sm["background"], fg=root.colors["text_color"])
        self.l_unit2 = tk.Label(self.sb_sm,text=f"{self.root.unit}", bg=self.sb_sm["background"], fg=root.colors["text_color"])
        self.buttonimage = tk.PhotoImage(file=f"{root.colors['path']}shape_builder/calculate_button.png")
        self.calc_button = tk.Label(self.sb_sm, image=self.buttonimage, activebackground=self["background"], border = 0, bg =self["background"])
        self.calc_button.bind('<Button-1>', func=lambda e: self.calculate())
        self.e1 = tk.Entry(self.sb_sm, width = 10,bg=root.colors["entry_color"], fg=root.colors["text_color"])
        self.e2 = tk.Entry(self.sb_sm, width = 10,bg=root.colors["entry_color"], fg=root.colors["text_color"])

        # result fonts
        self.result_font = "Roboto", 11

        ## result labels ##
        self.results = tk.Label(self.sb_sm,text="", bg=self.sb_sm["background"], fg=root.colors["text_color"], font=self.result_font)
        self.result1 =  tk.Label(self.sb_sm,text="", bg=self.sb_sm["background"], fg=root.colors["text_color"], font=self.result_font)
        self.result2 =  tk.Label(self.sb_sm,text="", bg=self.sb_sm["background"], fg=root.colors["text_color"], font=self.result_font)
        self.result3 =  tk.Label(self.sb_sm,text="", bg=self.sb_sm["background"], fg=root.colors["text_color"], font=self.result_font)
        self.result4 =  tk.Label(self.sb_sm,text="", bg=self.sb_sm["background"], fg=root.colors["text_color"], font=self.result_font)
        self.result5 =  tk.Label(self.sb_sm,text="", bg=self.sb_sm["background"], fg=root.colors["text_color"], font=self.result_font)
        self.result6 =  tk.Label(self.sb_sm,text="", bg=self.sb_sm["background"], fg=root.colors["text_color"], font=self.result_font)
        self.result7 =  tk.Label(self.sb_sm,text="", bg=self.sb_sm["background"], fg=root.colors["text_color"], font=self.result_font)
        self.result8 =  tk.Label(self.sb_sm,text="", bg=self.sb_sm["background"], fg=root.colors["text_color"], font=self.result_font)
        self.result9 =  tk.Label(self.sb_sm,text="", bg=self.sb_sm["background"], fg=root.colors["text_color"], font=self.result_font)
        self.result10 =  tk.Label(self.sb_sm,text="", bg=self.sb_sm["background"], fg=root.colors["text_color"], font=self.result_font)
        self.result11 =  tk.Label(self.sb_sm,text="", bg=self.sb_sm["background"], fg=root.colors["text_color"], font=self.result_font)
        self.result12 =  tk.Label(self.sb_sm,text="", bg=self.sb_sm["background"], fg=root.colors["text_color"], font=self.result_font)
        self.result13 =  tk.Label(self.sb_sm,text="", bg=self.sb_sm["background"], fg=root.colors["text_color"], font=self.result_font)

        self.results_block = []
        self.results_block.append(self.result1)
        self.results_block.append(self.result2)
        self.results_block.append(self.result3)
        self.results_block.append(self.result4)
        self.results_block.append(self.result5)
        self.results_block.append(self.result6)
        self.results_block.append(self.result7)
        self.results_block.append(self.result8)
        self.results_block.append(self.result9)
        self.results_block.append(self.result10)
        self.results_block.append(self.result11)
        self.results_block.append(self.result12)
        self.results_block.append(self.result13)


        # self.value_button = tk.Button(self.sb_sm, text="Értékadás", command=self.overwrite)
        self.value_buttonimage = tk.PhotoImage(file=f"{root.colors['path']}shape_builder/value_button.png")
        self.value_button = tk.Label(self.sb_sm, image=self.value_buttonimage, activebackground=self["background"], border = 0, bg =self["background"])
        self.value_button.bind('<Button-1>', func=lambda e: self.place_object())
        # self.cls = tk.Button(self.sb_sm,text="Minden törlése", command=self.clear_all)
        #self.pos_lbl = tk.Label(self,text="", bg=self.sb_sm["background"], fg=root.colors["text_color"])
        self.pos_lbl = self.create_text(15 ,15,text="",fill= root.colors['text_color']) # position label

        self.controls = []
        self.controls.append({"unit":self.l_unit1, "unit_type": "length"})
        self.controls.append({"unit":self.l_unit2, "unit_type": "length"})

        #############* Creating + and - buttons ##############
        self.img= (Image.open(f"{self.root.colors['path']}shape_builder/plus.png"))
        resized_image= self.img.resize((30,30), Image.ANTIALIAS)
        self.plus_img= ImageTk.PhotoImage(resized_image)
        self.img= (Image.open(f"{self.root.colors['path']}shape_builder/minus.png"))
        resized_image= self.img.resize((30,30), Image.ANTIALIAS)
        self.minus_img= ImageTk.PhotoImage(resized_image)
        self.img= (Image.open(f"{root.colors['path']}shape_builder/minus_hover.png"))
        resized_image= self.img.resize((30,30), Image.ANTIALIAS)
        self.minus_hover_img = ImageTk.PhotoImage(resized_image)
        self.img= (Image.open(f"{root.colors['path']}shape_builder/plus_hover.png"))
        resized_image= self.img.resize((30,30), Image.ANTIALIAS)
        self.plus_hover_img = ImageTk.PhotoImage(resized_image)
        self.img= (Image.open(f"{self.root.colors['path']}shape_builder/expand.png"))
        resized_image= self.img.resize((30,30), Image.ANTIALIAS)
        self.expand_img= ImageTk.PhotoImage(resized_image)
        self.img= (Image.open(f"{self.root.colors['path']}shape_builder/expand_hover.png"))
        resized_image= self.img.resize((30,30), Image.ANTIALIAS)
        self.expand_hover_img= ImageTk.PhotoImage(resized_image)
        self.minus= self.create_image(self.root.winfo_width()-310, self.root.winfo_height()-50, anchor=tk.NW,image=self.minus_img, tags=("plus_minus"))
        self.plus= self.create_image(self.root.winfo_width()-275, self.root.winfo_height()-50, anchor=tk.NW,image=self.plus_img, tags=("plus_minus"))
        self.expand = self.create_image(self.root.winfo_width()-275, self.root.winfo_height()-85, anchor=tk.NW,image=self.expand_img, tags=("plus_minus"))
        self.tag_bind(self.plus, '<Button-1>', lambda e: self.rescale(self.scale_factor))
        self.tag_bind(self.minus, '<Button-1>', lambda e: self.rescale(self.scale_factor**(-1)))
        self.tag_bind(self.expand, '<Button-1>', lambda e: self.auto_scale())
        self.tag_bind(self.minus, '<Enter>', lambda e: self.itemconfig(self.minus,image=self.minus_hover_img))
        self.tag_bind(self.plus, '<Enter>', lambda e: self.itemconfig(self.plus,image=self.plus_hover_img))
        self.tag_bind(self.expand, '<Enter>', lambda e: self.itemconfig(self.expand,image=self.expand_hover_img))
        self.tag_bind(self.minus, '<Leave>', lambda e: self.itemconfig(self.minus,image=self.minus_img))
        self.tag_bind(self.plus, '<Leave>', lambda e: self.itemconfig(self.plus,image=self.plus_img))
        self.tag_bind(self.expand, '<Leave>', lambda e: self.itemconfig(self.expand,image=self.expand_img))
 
        
        #############* Creating up and down button #################
        self.img= (Image.open(f"{root.colors['path']}shape_builder/up.png"))
        resized_image= self.img.resize((15,30), Image.ANTIALIAS)
        self.up_img= ImageTk.PhotoImage(resized_image)
        self.img= (Image.open(f"{root.colors['path']}shape_builder/down.png"))
        resized_image= self.img.resize((15,30), Image.ANTIALIAS)
        self.down_img= ImageTk.PhotoImage(resized_image)
        self.up= self.create_image(10, 20, anchor=tk.NW,image=self.up_img, tags=("up_down", "navigate"))
        self.down= self.create_image(10, 60, anchor=tk.NW,image=self.down_img, tags=("up_down", "navigate"))
        self.tag_bind(self.up, '<Button-1>', lambda e: self.change_active_shape())
        self.tag_bind(self.down, '<Button-1>', lambda e: self.change_active_shape("down"))

        #############* Creating rotation button #################
        self.img= (Image.open(f"{root.colors['path']}shape_builder/rotate_left.png"))
        resized_image= self.img.resize((20,20), Image.ANTIALIAS)
        self.rotate_left_img= ImageTk.PhotoImage(resized_image)
        self.img= (Image.open(f"{root.colors['path']}shape_builder/rotate_right.png"))
        resized_image= self.img.resize((20,20), Image.ANTIALIAS)
        self.rotate_right_img= ImageTk.PhotoImage(resized_image)
        self.rotate_left= self.create_image(10, 100, anchor=tk.NW,image=self.rotate_left_img, tags=("rotate", "navigate"))
        self.rotate_right= self.create_image(10, 125, anchor=tk.NW,image=self.rotate_right_img, tags=("rotate", "navigate"))
        self.tag_bind(self.rotate_left, '<Button-1>', lambda e: self.rotate(90))
        self.tag_bind(self.rotate_right, '<Button-1>', lambda e: self.rotate(-90))
        
        #############* Creating clear button on canvas ##############
        self.clear_img = tk.PhotoImage(file=f"{root.colors['path']}shape_builder/clear.png")
        self.clear_hover_img = tk.PhotoImage(file=f"{root.colors['path']}shape_builder/clear_hover.png")
        self.clear = self.create_image(10, self.root.winfo_height()-110, anchor=tk.NW,image=self.clear_img, tags=("clear"))
        self.tag_bind(self.clear, '<Button-1>', lambda e: self.clear_all())
        self.tag_bind(self.clear, '<Enter>', lambda e: self.itemconfig(self.clear,image=self.clear_hover_img))
        self.tag_bind(self.clear, '<Leave>', lambda e: self.itemconfig(self.clear,image=self.clear_img))

        ###########* Creating the basic, green rectangle #############
        """
        self.alap = self.create_rectangle(10,10,10+WIDTH,10+WIDTH,fill=root.colors["sb_draw_2nd"])
        self.alap_negyzet = Rectangle(self,10,10,10+WIDTH,10+WIDTH, self.alap)
        self.width_label = self.create_text(20+self.width,10+ self.height/2,text=str(self.width/self.scale))
        self.height_label = self.create_text(10+self.width/2,self.height+ 20,text=str(self.height/self.scale))
        """
        self.alap = self.create_rectangle(30,10,30+WIDTH,10+WIDTH,fill=root.colors["sb_draw_2nd"], tags=("alap_rectangle"))
        self.alap_negyzet = Rectangle(self,self.root,30,10,30+WIDTH,10+WIDTH, self.alap)
        self.width_entry = tk.Entry(self, width = 7,bg=root.colors["secondary_color"], fg=root.colors["text_color"],insertbackground=root.colors['text_color'],borderwidth = 0, highlightthickness = 0)
        self.width_entry.insert(tk.END, str(round(self.width1/self.scale,4)))
        # self.width_entry.place(x = 22 + self.width/2, y = 12 + self.height)
        self.height_entry = tk.Entry(self, width = 7,bg=root.colors["secondary_color"], fg=root.colors["text_color"],insertbackground=root.colors['text_color'],borderwidth = 0, highlightthickness = 0)
        self.height_entry.insert(tk.END, str(round(self.height1/self.scale,4)))
        # self.height_entry.place(x = 32 + self.width, y = 2 + self.height/2)
        self.move_entry()
        # self.height_entry.bind('<FocusOut>', func=lambda e: self.overwrite())
        # self.width_entry.bind('<FocusOut>', func=lambda e: self.overwrite())
        self.height_entry.bind('<Return>', func=lambda e: [self.overwrite(), self.focus_set()])
        self.width_entry.bind('<Return>', func=lambda e: [self.overwrite(), self.focus_set()])
        self.width_entry.bind('<Tab>', func=lambda e: [self.overwrite(), self.focus_height()])
        self.height_entry.bind('<Tab>', func=lambda e: [self.overwrite(), self.focus_width()])

        ###########* Creating basic, green semicircle #############
        self.angle=180
        self.start = 0
        """
        self.alap_circle = self.create_arc(10,60,40,90,extent=self.angle, start = self.start, fill=root.colors["sb_draw_2nd"])
        self.r_label = self.create_text(10+30/2,60+30,text=f"r={30/2}")
        """
        self.alap_semicircle = self.create_arc(30,10,30+2*self.r1,10+2*self.r1,extent=self.angle, start = self.start, fill=root.colors["sb_draw_2nd"], tags=("alap_semicircle"))
        # self.r_label = self.create_text(30+30/2,10+30,text=f"r={30/2}",tags=("alap_circle"))
        self.itemconfigure("alap_semicircle",state="hidden")

        ###########* Creating basic, green quarter_circle #############
        self.angle=90
        self.start = 0
        """
        self.alap_circle = self.create_arc(10,60,40,90,extent=self.angle, start = self.start, fill=root.colors["sb_draw_2nd"])
        self.r_label = self.create_text(10+30/2,60+30,text=f"r={30/2}")
        """
        self.alap_quarter_circle = self.create_arc(30,10,30+2*self.r1,10+2*self.r1,extent=self.angle, start = self.start, fill=root.colors["sb_draw_2nd"], tags=("alap_quarter_circle"))
        # self.r_label = self.create_text(30+30/2,10+30,text=f"r={30/2}",tags=("alap_circle"))
        self.itemconfigure("alap_quarter_circle",state="hidden")
        
        ##########* Creating basic green triangle #############
        self.alap_triangle = RightTriangle(self,self.root,40,40,self.width2,self.height2) #! width+heigth ??? 
        self.delete(self.alap_triangle.canvas_repr)
        self.alap_triangle.canvas_repr = self.create_polygon(self.alap_triangle.points[0][0],self.alap_triangle.points[0][1],self.alap_triangle.points[1][0],self.alap_triangle.points[1][1],self.alap_triangle.points[2][0],self.alap_triangle.points[2][1], fill=self.root.colors["sb_draw"], outline="#000000",tags=("alap_triangle"))
        self.itemconfigure("alap_triangle",state="hidden")
        self.itemconfigure("alap_triangle",fill=root.colors["sb_draw_2nd"])
        ##########* Creating axis #############
        self.x_axis = self.create_line(10,self.Ycenter,self.Xcenter*2,self.Ycenter, arrow=tk.LAST,fill= root.colors["draw_tertiary"], tags=("orig_axes")) #Drawing X-axis
        self.x_label = self.create_text(2*self.Xcenter-5,self.Ycenter+ 20,text="X",fill= root.colors["draw_tertiary"],tags=("orig_axes")) # X lavel
        self.y_axis = self.create_line(self.Xcenter,10,self.Xcenter,self.Ycenter*2, arrow=tk.FIRST,fill= root.colors["draw_tertiary"],tags=("orig_axes")) #Drawing Y-axis
        self.y_label = self.create_text(self.Xcenter +20 ,15,text="Y",fill= root.colors["draw_tertiary"],tags=("orig_axes")) # Y label
        if not self.root.show_orig_axis: self.itemconfigure("orig_axes",state="hidden")
        #########* Evensts and other stuff ############
        self.sticky = tk.BooleanVar(value=True)
        self.is_sticky = tk.Checkbutton(self.sb_sm, text="Automatikus igazítás", variable=self.sticky, onvalue=True, offvalue=False,bg = self.sb_sm["background"], fg=root.colors["text_color"], selectcolor=root.colors['secondary_color'])
        self.bind('<B1-Motion>',self.move) #"drag-and-drop" action
        self.bind('<ButtonRelease-1>',self.release) #when you relase the left mose button
        self.popup_menu = tk.Menu(self, tearoff=0) #right click menu
        self.popup_menu.add_command(label="Törlés",command=self.delete_shape)
        #self.popup_menu.add_command(label="Resize",command=self.resize_rectangle)
        self.popup_menu.add_command(label="Tulajdonságok",command=self.rectangle_info)
        self.popup_menu.add_command(label="Negatív/Pozitív",command=self.set_to_negative)
        self.bind("<Button-3>", self.popup) # right-click event
        self.bind("<Configure>", self.resize_canvas)
        #self.tag_bind("rect",'<Double-Button-1>',self.select)
        self.tag_bind("shape",'<Button-1>',self.select)
        #self.tag_bind("arc",'<Button-1>',self.select)
        self.bind("<Button-1>", self.deselect)
        self.bind("<Motion>", lambda e: self.itemconfig(self.pos_lbl, text=f"x: {round((e.x-self.Xcenter)/self.scale,1)} y: {round((self.Ycenter-e.y)/self.scale,1)}"))
        self.root.bind("<Delete>", self.delete_shape)
        self.root.bind("<Control-i>", self.rectangle_info)
        self.root.bind("<Control-r>", self.resize_rectangle)

        #self.root.bind("<Control-c>", self.add_to_clp)
        #self.root.bind("<Control-v>", self.insert_from_clp)
        #self.root.bind("<Control-t>", self.check_for_negatives)
        #self.root.bind("<Control-n>", lambda e: self.hc.refresh(self.Xcenter-20,self.Ycenter-100, self.hc.r))

        ##############* Packing objects ###############
        # self.place_holder.grid(row=0,column=1,columnspan=5)
        self.l_width.grid(row=1,column=1,padx=(10,0),pady=(20,0))
        self.e1.grid(row=1,column=2,pady=(20,0),padx=2)
        self.l_unit1.grid(row=1,column=3,pady=(20,0))
        self.l_height.grid(row=2,column=1,padx=(10,0))
        self.e2.grid(row=2,column=2,padx=2)
        self.l_unit2.grid(row=2,column=3)
        self.value_button.grid(row=1,rowspan=2, column=5,pady=(15,0),padx=(5,10))
        self.is_sticky.grid(row=3,columnspan=3)
        self.calc_button.grid(row=4,column=1,columnspan=5,padx=(20))
        self.rowcount = 7
        for i in self.results_block:
            i.grid(row=self.rowcount+1, column=1, columnspan=5, padx=30, pady=2, sticky=tk.W)
            self.rowcount += 1

        self.results_block[0].grid(padx=15)
        self.results_block[3].grid(padx=15)
        self.results_block[9].grid(padx=15)
        # self.cls.grid(row=6, column=1,columnspan=3)
        ####################### Draw grid #######################
        self.visual_grid = visual_grid(self,self.root, self.scale, self.Xcenter, self.Ycenter, self.scale_factor)

    def popup(self, e): #right cklick menu shows up
        if not self.isMoving:
            for i in self.shapes:
                if i.is_inside((e.x,e.y)):
                    self.select(e)
                    try:
                        self.popup_menu.tk_popup(e.x_root, e.y_root, 0)
                    finally:
                        self.popup_menu.grab_release()
                    break
    def delete_shape(self, e=None):
        print("deleteing rectangle")
        for i in self.selected:
            if i.negative: self.negatives.remove(i)
            self.delete(i.canvas_repr)
            self.shapes.remove(i)
            self.selected = []
        for k in self.shapes:
            k.is_overlapping()
        self.check_for_negatives()
        self.move_entry()
    def resize_rectangle(self,e=None): #! Something is wrong...
        for i in self.selected:
            if type(i)==Rectangle:
                i.refresh(i.x1, i.y1, i.x1 + self.width1, i.y1 + self.height1)
            elif type(i)==Arc:
                i.refresh(i.center[0],i.center[1],self.width1/2,i.angle, i.start) ##### TODO EZ nEM LESZ JÓ KÖRNÉL
            elif type(i)==RightTriangle:
                print("Warning: resize is not implemented for Right Triangles")
            else:
                print(type(i),"\n" ,i)
                raise TypeError
            i = None
        for k in self.rectangles:
            k.is_overlapping()
        self.check_for_negatives()
    def rectangle_info(self,e=None): #! Formating
        self.clear_results()
        if len(self.selected)>1:
            self.result1.config(text=f"{len(self.selected)} darab objektum van kijelölve")
            return -1
        if len(self.selected)>0: self.result1.config(text= self.selected[0].get_info())
    def set_to_negative(self, object = None):
        if object is None:
            for i in self.selected:
                i.negative = not i.negative
                if i.negative: 
                    self.tag_raise(i.canvas_repr)
                    self.negatives.append(i)
                else: self.negatives.remove(i)
        else:
            object.negative = not object.negative
            if object.negative: 
                self.tag_raise(object.canvas_repr)
                self.negatives.append(object)
            else: self.negatives.remove(object)
        for k in self.shapes: k.is_overlapping()
        self.check_for_negatives()
    def select(self,e, object=None):
        #self.deselect()
        if e is None and object is not None:
            self.selected.append(object)
            for i in self.selected:
                self.itemconfig(i.canvas_repr, fill='pink')
            return 0
        tmp = self.find_closest(e.x,e.y)[0]
        for i in self.shapes:
            if i.canvas_repr == tmp and i not in self.selected:
                self.selected.append(i)
                self.move_entry()
                break
        else:
            print("Selection_Error: Shape not found...")
            return -1  
        for i in self.selected:
            self.itemconfig(i.canvas_repr, fill='pink')
        print("Selecting shape")
    def deselect(self,e=None):
        if self.rotation_happend == True:
            self.rotation_happend = False
            print("Rotation happend")
            return -1
        if e is not None:
            for i in self.shapes:
                if i.is_inside((e.x,e.y)):
                    return 0
        try:
            for i in self.selected:
                print("deselect")
                self.itemconfig(i.canvas_repr, fill=self.root.colors["sb_draw"])
            self.selected = []
        except:
            pass
        for k in self.shapes:
            k.is_overlapping()
        #### move the size entry boxes to the deafult place
        self.move_entry()
    def move(self,e): #? could be better but works..
        if keyboard.is_pressed("Ctrl"):
            if self.last_click_pos is None:
                self.last_click_pos = (e.x, e.y)
            else:
                self.translation(e.x-self.last_click_pos[0],e.y-self.last_click_pos[1])
                self.last_click_pos = (e.x, e.y)
            return 0
        self.itemconfig(self.pos_lbl, text=f"x: {round((e.x-self.Xcenter)/self.scale,1)} y: {round((self.Ycenter-e.y)/self.scale,1)}")
        self.deselect()
        # self.label.config(text=f"")
        #choosing object
        for i in self.shapes:
            if self.current is None and i.is_inside((e.x,e.y)) and self.starting_pos is None:
                self.shapes.remove(i)
                self.current = i
                self.itemconfig(self.current.canvas_repr, fill='light blue')
                break
        else:
            pos = self.coords(self.alap_negyzet.canvas_repr)
            if self.current is None and e.x>=pos[0] and e.x<=pos[2] and e.y>=pos[1] and e.y <=pos[3] and self.starting_pos is None and self.active_shape == "Rectangle":
                self.current = Rectangle(self,self.root,pos[0],pos[1],pos[0]+self.width1,pos[1]+self.height1,self.create_rectangle(pos[0],pos[1],pos[0]+self.width1,pos[1]+self.height1,fill=self.root.colors["sb_draw"], tags=("rect","shape")))
                self.itemconfig(self.current.canvas_repr, fill='light blue')
        if not self.current: # Circle
            pos = self.coords(self.alap_semicircle)
            # cent = (pos[0]+self.r,pos[1]+self.r)
            if self.active_shape == "Semicircle":
                if dist((e.x,e.y), (pos[0]+self.r1,pos[1]+self.r1))<self.r1 and degrees(asin(abs(e.y-(pos[1]+self.r1))/dist((e.x,e.y), (pos[0]+self.r1,pos[1]+self.r1))))<self.angle and self.starting_pos is None:
                    print("kör")
                    #! Nem mindig jó helyre kattintva aktiválódik!!
                    self.current = Arc(self,self.root,e.x,e.y,self.r1,self.angle,self.start)
                    self.itemconfig(self.current.canvas_repr, fill='light blue')
                    print(type(self.current))
            elif self.active_shape == "quarter_circle":
                if dist((e.x,e.y), (pos[0]+self.r2,pos[1]+self.r2))<self.r2 and degrees(asin(abs(e.y-(pos[1]+self.r2))/dist((e.x,e.y), (pos[0]+self.r2,pos[1]+self.r2))))<self.angle and self.starting_pos is None:
                    print("kör")
                    #! Nem mindig jó helyre kattintva aktiválódik!!
                    self.current = Arc(self,self.root,e.x,e.y,self.r2,self.angle,self.start)
                    self.itemconfig(self.current.canvas_repr, fill='light blue')
                    print(type(self.current))
            elif self.active_shape == "rightTriangle":
                if(self.alap_triangle.is_inside([e.x,e.y])):
                    print("Triangle")
                    self.current = RightTriangle(self, self.root, e.x,e.y,self.width2,self.height2,orientation=self.alap_triangle.orientation)
                    self.itemconfig(self.current.canvas_repr, fill="light blue")
                    print(type(self.current))
        if not self.current:
            ############### Selecting multiple objects ##############
            if self.starting_pos is None: 
                self.starting_pos = (e.x,e.y)
                self.itemconfigure(self.selecting_area,state="normal")
            else:
                try:
                    self.coords(self.selecting_area,self.starting_pos[0],self.starting_pos[1],e.x,e.y)
                except:
                    print("Can not show selection area")
            return -1
        pos = self.coords(self.current.canvas_repr)
        if type(self.current)==Rectangle and (self.isMoving or e.x>=pos[0] and e.x<=pos[2] and e.y>=pos[1] and e.y <=pos[3]):
            self.current.refresh(e.x-self.current.width/2,e.y-self.current.height/2,e.x+self.current.width/2,e.y+self.current.height/2)
            self.isMoving = True
            return 0
        elif self.isMoving or type(self.current)==Arc or type(self.current) == RightTriangle: #! Itt valami furán van meírva de úgy néz ki működik
            if type(self.current) == Arc: self.current.refresh(e.x,e.y,self.current.r,self.current.angle,self.current.start)
            elif type(self.current) == RightTriangle: self.current.refresh(e.x,e.y,self.current.width,self.current.height)
            self.isMoving = True
            return 0      
    def release(self,e):
        self.delete("principal_axis")
        self.delete("s_axis")
        self.clear_results()
        if self.root.show_orig_axis:self.itemconfigure("orig_axes",state="normal")
        self.itemconfig(self.pos_lbl, text="")
        #choosing object
        if self.sticky.get() and self.current:
            self.current.align()
            #? prioritási sorrend???    
        if self.isMoving and self.current is not None:
            #self.itemconfig(self.current.canvas_repr, fill=self.root.colors["sb_draw"])
            self.shapes.append(self.current)
            for k in self.shapes:
                k.is_overlapping()
        if self.starting_pos is not None:
            mwc = min(self.starting_pos[0],e.x)
            mec = max(self.starting_pos[0],e.x)
            mnc = min(self.starting_pos[1],e.y)
            msc = max(self.starting_pos[1],e.y)
            for i in self.shapes:    
                if i.center[0] > mwc and i.center[0]< mec and i.center[1] > mnc and i.center[1] < msc:
                    self.select(None, i)
            self.coords(self.selecting_area,mwc,mnc,mec,msc)
            self.starting_pos = None
        self.itemconfigure(self.selecting_area,state="hidden")
        for i in self.negatives: self.tag_raise(i.canvas_repr)
        self.check_for_negatives()
            
            
        self.isMoving = False
        self.current=None
        # self.label.config(text="")
        self.itemconfig(self.pos_lbl, text=f"x: {round((e.x-self.Xcenter)/self.scale,1)} y: {round((self.Ycenter-e.y)/self.scale,1)}")
        self.tag_raise("plus_minus")
        self.tag_raise(self.pos_lbl)
        self.last_click_pos = None
    def calculate(self):
        if len(self.shapes) == 0:
            self.clear_results()
            self.result1.config(text=f"A: 0 mm\nIx: 0 mm\nIy: 0 mm\nIxy: 0") #! Formatting
            return -1
        elif self.negativ_in_wrong_position:
            self.clear_results()
            self.result1.config(text="Hibásan lehelyezett negatív elem!") #! Formatting
            return -1
        Ix = 0
        Iy = 0
        Ixy = 0
        A = 0
        out_str = ""
        self.clear_results()
        if not self.root.calc_for_orig_axis:
            Sx=0
            Sy=0
            for i in self.shapes:
                A += i.area*(1-2* (i.negative))
                Sx += (i.s_center[0]-self.Xcenter)*i.area*(1-2* (i.negative))
                Sy += (self.Ycenter-i.s_center[1])*i.area*(1-2* (i.negative))
            if A <= 0:
                self.clear_results()
                self.result1.config(text=f"Hiba: Az össz terület negatív vagy nulla")
                return -1 
            Sx /= A
            Sy /= A
            Sx += self.Xcenter
            Sy = self.Ycenter - Sy
            a_length = min(min(Sx,Sy),self.canvas_height-Sy,self.canvas_width-Sx)
            self.sx_axis = self.create_line(Sx+10-a_length,Sy,Sx+a_length-10,Sy, arrow=tk.LAST, tags=("s_axis")) #Drawing X-axis
            self.sx_label = self.create_text(Sx+a_length-20,Sy+ 20,text="Xs",tags=("s_axis")) # X lavel
            self.sy_axis = self.create_line(Sx,Sy-a_length+10,Sx,Sy+a_length-10, arrow=tk.FIRST,tags=("s_axis")) #Drawing Y-axis
            self.sy_label = self.create_text(Sx +20 ,Sy-a_length+20 ,text="Ys",tags=("s_axis")) # Y label
            if self.root.orig_axis_dissapier: self.itemconfigure("orig_axes",state="hidden")
            print(Sx/self.scale,Sy/self.scale)
            out_str += f"Sx: {Sx/self.scale}\nSy: {Sy/self.scale}\n"
            #TODO: Sx és Sy koordináták a canvas bal felső sarkától vannak mérve, nem a globális kordináta rendszertől, így kicsit nehéz rajta kiigazodni
            self.result1.config(text="Súlypont koordinátái:")
            self.result2.config(text="Sₓ = " + str(round((Sx - self.Xcenter)/self.scale,4)) + " " + self.root.unit)
            self.result3.config(text="Sᵧ = " + str(round((self.Ycenter - Sy)/self.scale,4)) + " " + self.root.unit)
        else:
            out_str += "Számítások fix tengelyre:\n"
            Sx = self.Xcenter
            Sy = self.Ycenter
            a_length = min(min(Sx,Sy),self.canvas_height-Sy,self.canvas_width-Sx)
            #calc for s_center
            A_t = 0
            Sx_t = 0
            Sy_t = 0
            for i in self.shapes:
                A_t += i.area*(1-2* (i.negative))
                Sx_t += (i.s_center[0]-self.Xcenter)*i.area*(1-2* (i.negative))
                Sy_t += (self.Ycenter-i.s_center[1])*i.area*(1-2* (i.negative))
            Sx_t = Sx_t/A_t
            Sy_t = Sy_t/A_t
            self.result1.config(text=f"Alakzat súlypontja\n(nem erre számol!):")
            self.result2.config(text=f"Súlypont x: {round(Sx_t/self.scale, 4)}")
            self.result3.config(text=f"Súlypont y: {round(Sy_t/self.scale, 4)}")
        A = 0
        for i in self.shapes.rectangles:
            pos = self.coords(i.canvas_repr)
            A_current = (pos[2]-pos[0]) * (pos[3]-pos[1])
            A += (1-2* (i.negative))*A_current
            Ix += (1-2* (i.negative)) * ( ((pos[2]-pos[0]) * (pos[3]-pos[1])**3 )/12+ A_current*(Sy-pos[1]-(pos[3]-pos[1])/2)**2 )
            Iy += (1-2* (i.negative)) * ( (pos[2]-pos[0])**3 * (pos[3]-pos[1]) /12+ A_current*(pos[0]+(pos[2]-pos[0])/2-Sx)**2 )
            Ixy += (1-2* (i.negative)) * ( A_current*(Sx - (pos[0]+(pos[2]-pos[0])/2))*(-1)*(Sy-pos[1]-(pos[3]-pos[1])/2) ) # CHECK

        for i in self.shapes.arcs: #! Not sure if works for not semi or quarter circle, but any arc...
            if i.type=="quarter_circle":
                A += (1-2* (i.negative))*i.area
                Ixc = i.r**4 / (144*pi) *(9*pi**2 -64)
                Iyc = Ixc
                Ixyc = -i.r**4 / (144*pi) *(-(18*pi -64))
            elif i.type == "Semicircle":
                A += (1-2* (i.negative))*i.area
                Iyc = i.r**4 / (72*pi) * 9* pi**2
                Ixc = i.r**4 / (72*pi) * (9*pi**2 - 64)
                Ixyc = 0
            else:
                raise TypeError
            # rotation + translation
            Ix += (1-2* (i.negative))  * ( ((Ixc+Iyc)/2 + (Ixc-Iyc)/2 * cos(2*radians(i.start))-Ixyc*sin(2*radians(i.start)))  + i.area*(Sy-i.s_center[1])**2 )
            Iy += (1-2* (i.negative))  * ( ((Ixc+Iyc)/2 - (Ixc-Iyc)/2 * cos(2*radians(i.start))+Ixyc*sin(2*radians(i.start))) + i.area*(Sx-i.s_center[0])**2 )
            Ixy += (1-2* (i.negative)) * ( (Ixc-Iyc)/2 * sin(2*radians(i.start)) + Ixyc*cos(2*radians(i.start))  + i.area*(Sx-i.s_center[0])*(-Sy+i.s_center[1]) )

        for i in self.rightTriangles:
            A += (1-2* (i.negative))*i.area
            Ixc = (i.height**3 *i.width)/36
            Iyc = (i.width**3 *i.height)/36
            Ixyc = -(i.width**2 * i.height**2 )/72
            
            
            Ix += (1-2* (i.negative)) * ( ((Ixc+Iyc)/2 + (Ixc-Iyc)/2 * cos(2*radians(i.orientation))-Ixyc*sin(2*radians(i.orientation))  + i.area*(Sy-i.s_center[1])**2) )
            Iy += (1-2* (i.negative)) * ( ((Ixc+Iyc)/2 - (Ixc-Iyc)/2 * cos(2*radians(i.orientation))+Ixyc*sin(2*radians(i.orientation)) + i.area*(Sx-i.s_center[0])**2) )
            Ixy += (1-2* (i.negative)) * ( (Ixc-Iyc)/2 * sin(2*radians(i.orientation)) + Ixyc*cos(2*radians(i.orientation)) + i.area*(Sx-i.s_center[0])*(-Sy+i.s_center[1]) )

            print("ezek az eredmenyek")
            print(Iyc)
            print(i.area)
            print(i.area*(Sx-i.s_center[0])**2)
            print(Sx-i.s_center[0])

            print("Warning: Calculate for riht Triangles is not checked")

        self.result4.config(text="Keresztmetszeti jellemzők:")
        self.result5.config(text="A = " + str(round(A/self.scale**2, 4)) + " " + self.root.unit + "²")
        if self.root.calc_for_orig_axis:
            self.result6.config(text="Iₓ = " + str(round(Ix/self.scale**4, 4)) + " " + self.root.unit + "\u2074")
            self.result7.config(text="Iᵧ = " + str(round(Iy/self.scale**4,4)) + " " + self.root.unit + "\u2074")
            self.result8.config(text="Iₓᵧ = " + str(round(Ixy/self.scale**4,4)) + " " + self.root.unit + "\u2074")
            self.result9.config(text="Iₚ = " + str(round(Ix/self.scale**4 + Iy/self.scale**4,4)) + " " + self.root.unit + "\u2074")
        else:
            self.result6.config(text="Iₓₛ = " + str(round(Ix/self.scale**4, 4)) + " " + self.root.unit + "\u2074")
            self.result7.config(text="Iᵧₛ = " + str(round(Iy/self.scale**4,4)) + " " + self.root.unit + "\u2074")
            self.result8.config(text="Iₓₛᵧₛ = " + str(round(Ixy/self.scale**4,4)) + " " + self.root.unit + "\u2074")
            self.result9.config(text="Iₚₛ = " + str(round(Ix/self.scale**4 + Iy/self.scale**4,4)) + " " + self.root.unit + "\u2074")

        if not self.root.calc_for_orig_axis:
            i1, i2, alpha = self.plot_principal_axis(Ix/self.scale**4,Iy/self.scale**4,Ixy/self.scale**4, Sx,Sy,a_length)
            if self.root.angle_unit == '°':
                alpha = alpha/np.pi*180
            else:
                alpha = alpha
            self.result10.config(text="Főmásodrendű nyomatékok:")
            self.result11.config(text="I₁ = " + str(round(i1,4)) + " " + self.root.unit + "\u2074")
            self.result12.config(text="I₂ = " + str(round(i2,4)) + " " + self.root.unit + "\u2074")
            self.result13.config(text="\u03B1 = " + str(round(alpha,4)) + " " + self.root.angle_unit)
        
    def overwrite(self):
        ok = True
        if len(self.selected)==1:
            object = self.selected[0]
            try:
                h = float(self.height_entry.get().replace(',','.'))*self.scale
                if h <=0:
                    raise ValueError
                self.height_entry.config({"background": self.root.colors['secondary_color']})
            except:
                print("Hiba, az egyik mező nem olvashó be")
                self.height_entry.config({"background": self.root.colors['error_color']})
                ok=False
            if object.type == "Rectangle":
                try:
                    w=float(self.width_entry.get().replace(',','.'))*self.scale
                    if w <=0:
                        raise ValueError
                    self.width_entry.config({"background": self.root.colors['secondary_color']})
                except:
                    print("Hiba, az egyik mező nem olvashó be")
                    self.width_entry.config({"background": self.root.colors['error_color']})
                    ok = False
                if not ok: return -1

                object.refresh(object.x1,object.y1,object.x1+w,object.y1+h)
            elif object.type == "rightTriangle":
                try:
                    w=float(self.width_entry.get().replace(',','.'))*self.scale
                    if w <=0:
                        raise ValueError
                    self.width_entry.config({"background": self.root.colors['secondary_color']})
                except:
                    print("Hiba, az egyik mező nem olvashó be")
                    self.width_entry.config({"background": self.root.colors['error_color']})
                    ok = False
                if not ok: return -1
                object.refresh(object.center[0],object.center[1],w,h)
            elif object.type == "Semicircle":
                if not ok: return -1

                object.refresh(object.center[0],object.center[1],h,angle=180)
            elif object.type == "quarter_circle":
                if not ok: return -1

                object.refresh(object.center[0],object.center[1],h,angle=90)
            self.auto_scale()
        else:
            try:
                h = float(self.height_entry.get().replace(',','.'))*self.scale
                if h <=0:
                    raise ValueError
                self.height_entry.config({"background": self.root.colors['secondary_color']})
            except:
                print("Hiba, az egyik mező nem olvashó be")
                self.height_entry.config({"background": self.root.colors['error_color']})
                ok=False
            if self.active_shape == "Rectangle":
                try:
                    w=float(self.width_entry.get().replace(',','.'))*self.scale
                    if w <=0:
                        raise ValueError
                    self.width1 = w
                    self.height1 = h
                    self.width_entry.config({"background": self.root.colors['secondary_color']})
                except:
                    print("Hiba, az egyik mező nem olvashó be")
                    self.width_entry.config({"background": self.root.colors['error_color']})
                    ok = False
                if not ok: return -1
                self.coords(self.alap_negyzet.canvas_repr, 30,10,30+self.width1,10+self.height1)
            elif self.active_shape == "rightTriangle":
                try:
                    w=float(self.width_entry.get().replace(',','.'))*self.scale
                    if w <=0:
                        raise ValueError
                    self.width2 = w
                    self.height2 = h
                    self.width_entry.config({"background": self.root.colors['secondary_color']})
                except:
                    print("Hiba, az egyik mező nem olvashó be")
                    self.width_entry.config({"background": self.root.colors['error_color']})
                    ok = False
                if not ok: return -1
                # self.coords(self.alap_triangle.canvas_repr, 30,10,30+self.width2,10+self.height2, 30, 10+self.height2)
                l,r,t,b = self.alap_triangle.get_bounding_box()
                self.alap_triangle.refresh(self.alap_triangle.center[0],self.alap_triangle.center[1], self.width2, self.height2)
                l2,r2,t2,b2 = self.alap_triangle.get_bounding_box()
                self.alap_triangle.translate(l-l2,t-t2)
            elif self.active_shape == "Semicircle":
                if not ok: return -1
                self.r1 = h
                self.coords(self.alap_semicircle, 30,10,30+self.r1*2,10+self.r1*2)
                print(self.r1)
            elif self.active_shape == "quarter_circle":
                if not ok: return -1
                self.r2 = h
                self.coords(self.alap_quarter_circle, 30,10,30+self.r2*2,10+self.r2*2)
            self.auto_scale_default()
        self.move_entry()
    def clear_all(self): #? Could be better
        self.rectangles = []
        self.arcs = []
        self.rightTriangles = []
        self.negatives = []
        self.delete("shape") 
        self.delete("principal_axis")
        self.delete("s_axis")
        del self.shapes
        self.shapes = Shapes(self,self.rectangles,self.arcs,self.rightTriangles)
        self.negativ_in_wrong_position = False
    def plot_principal_axis(self, Ix, Iy, Ixy, Sx, Sy, a_length):
        I1 = (Ix+Iy)/2 + 0.5*sqrt((Ix-Iy)**2 + 4* Ixy**2)
        I2 = (Ix+Iy)/2 - 0.5*sqrt((Ix-Iy)**2 + 4* Ixy**2)
        if abs(Ixy) > 10**(-12):
            alfa = atan((Ix-I1)/Ixy)
        else:
            alfa = 0
        if self.root.sb_ha_vis:
            phi = alfa
            alfa = -alfa
            a_length = a_length-20
            self.p1 = self.create_line(Sx-a_length*cos(alfa),Sy-a_length*sin(alfa),Sx+a_length*cos(alfa),Sy+a_length*sin(alfa), arrow=tk.LAST, fill=self.root.colors['draw_principal'],tags=("principal_axis"))
            self.p2 = self.create_line(Sx-a_length*cos(alfa+pi/2),Sy-a_length*sin(alfa+pi/2),Sx+a_length*cos(alfa+pi/2),Sy+a_length*sin(alfa+pi/2), arrow=tk.FIRST, fill=self.root.colors['draw_principal'],tags=("principal_axis"))
            self.p1_label = self.create_text(Sx+a_length*cos(alfa)+10,Sy+a_length*sin(alfa)-10,text="I1",tags=("principal_axis"),fill=self.root.colors['draw_principal']) # p1 lavel
            self.p2_label = self.create_text(Sx-a_length*cos(alfa+pi/2)+10,Sy-a_length*sin(alfa+pi/2)-10,text="I2",tags=("principal_axis"),fill=self.root.colors['draw_principal']) # p2 lavel
        return I1, I2, phi
    def rescale(self,scale, button = False): #!? Could be better
        self.scale *= scale
        self.alap_negyzet.refresh(30,10,30+self.width1*scale,10+self.height1*scale)
        self.coords(self.alap_semicircle, 30,10,30+2*self.r1*scale,10+2*self.r1*scale)
        self.coords(self.alap_quarter_circle, 30,10,30+2*self.r2*scale,10+2*self.r2*scale) 
        l,r,t,b = self.alap_triangle.get_bounding_box()
        self.alap_triangle.refresh(self.alap_triangle.center[0],self.alap_triangle.center[1], self.width2*scale, self.height2*scale)
        l2,r2,t2,b2 = self.alap_triangle.get_bounding_box()
        self.alap_triangle.translate(l-l2,t-t2)
        self.width1 *= scale
        self.height1 *= scale
        self.width2 *= scale
        self.height2 *= scale
        self.r1 *= scale
        self.r2 *= scale
        print(self.r1)
        for i in self.rectangles: #?Esetleg álltalánosítani bármilyen alakzatra
            i.refresh(self.Xcenter-(self.Xcenter-i.x1)*scale, self.Ycenter-(self.Ycenter-i.y1)*scale, self.Xcenter-(self.Xcenter - i.x2)*scale, self.Ycenter-(self.Ycenter-i.y2)*scale)
        for i in self.arcs:
            i.refresh(self.Xcenter-(self.Xcenter-i.center[0])*scale,self.Ycenter-(self.Ycenter-i.center[1])*scale, i.r*scale, i.angle, i.start)
        for i in self.rightTriangles:
            i.refresh(self.Xcenter-(self.Xcenter-i.center[0])*scale,self.Ycenter-(self.Ycenter-i.center[1])*scale, i.width*scale, i.height*scale)
        self.auto_scale_default_shape(button)
        self.move_entry()
        # self.visual_grid.rescale_grid(self.Xcenter, self.Ycenter, scale)
        self.visual_grid.create_grid(self.scale, self.Xcenter, self.Ycenter, self.scale_factor)
    def resize_canvas(self,e):
        self.coords(self.minus, e.width-45, e.height-50)
        self.coords(self.plus, e.width-80, e.height-50)
        self.coords(self.expand, e.width-45, e.height-85)
        self.coords(self.pos_lbl, e.width-50, 30)
        self.canvas_width = e.width
        self.canvas_height = e.height
        self.translation(e.width/2-self.Xcenter, e.height/2-self.Ycenter)
        self.delete("s_axis")
        self.delete("principal_axis")
        self.coords(self.clear, 10, e.height-50)
        self.move_entry()
    def translation(self, dx, dy):
        self.Xcenter += dx
        self.Ycenter += dy
        # Basic coord system
        self.coords(self.x_axis,10,self.Ycenter,self.canvas_width-10,self.Ycenter)
        self.coords(self.y_axis,self.Xcenter,10,self.Xcenter,self.canvas_height-10)
        x_axis = self.coords(self.x_axis)
        y_axis = self.coords(self.y_axis)
        self.coords(self.x_label,x_axis[2], x_axis[3]+15)
        self.coords(self.y_label,y_axis[0]+15, y_axis[1])
        #Rectangles
        for i in self.shapes:
            i.translate(dx,dy)
        self.visual_grid.create_grid(self.scale, self.Xcenter, self.Ycenter, self.scale_factor)
    def place_object(self):
        print('good')
        ok = True
        try:
            x=float(self.e1.get().replace(',','.'))*self.scale
            self.e1.config({"background": self.root.colors['secondary_color']})
        except:
            print("Hiba, az egyik mező nem olvashó be")
            self.e1.config({"background": self.root.colors['error_color']})
            ok = False
        try:
            y = float(self.e2.get().replace(',','.'))*self.scale
            self.e2.config({"background": self.root.colors['secondary_color']})
        except:
            print("Hiba, az egyik mező nem olvashó be")
            self.e2.config({"background": self.root.colors['error_color']})
            ok=False
        if not ok: return -1
        x_coord = (x+self.Xcenter)
        y_coord = (-y+self.Ycenter)
        if len(self.selected)==1:
            object = self.selected[0]
            if object.type == "Rectangle":
                object.refresh(x_coord,y_coord,x_coord+object.width,y_coord+object.height)
            elif object.type == "rightTriangle":
                object.refresh(x_coord,y_coord,object.width,object.height)
            else:
                object.refresh(x_coord,y_coord,object.r,angle=object.angle, start = object.start)
        elif len(self.selected)==0:
            if self.active_shape == "Rectangle":
                place_rect = Rectangle(self,self.root,x_coord,y_coord,x_coord+self.width1,y_coord+self.height1,self.create_rectangle(x_coord,y_coord,x_coord+self.width1,y_coord+self.height1,fill=self.root.colors["sb_draw"], tags=("rect","shape")))#self.create_rectangle(x_coord,y_coord,x_coord+self.width,y_coord+self.height,fill=self.root.colors["sb_draw"], tags=("rect","shape"))
                self.shapes.append(place_rect)
            elif self.active_shape == "rightTriangle":
                place_triang = RightTriangle(self, self.root, x_coord,y_coord,self.width2,self.height2,orientation=self.alap_triangle.orientation)
                self.shapes.append(place_triang)
            elif self.active_shape == "Semicircle":
                place_semicircle = Arc(self,self.root,x_coord,y_coord,self.r1,angle=180, start = self.start)
                self.shapes.append(place_semicircle)
            elif self.active_shape == "quarter_circle":
                place_quarter_circle = Arc(self,self.root,x_coord,y_coord,self.r2,angle=90, start = self.start)
                self.shapes.append(place_quarter_circle)
        else:
            None
        self.check_for_negatives()
        self.move_entry()
        self.auto_scale()
    def add_to_clp(self,e=None):
        self.clipboard = self.selected #! deepcopy???
    def insert_from_clp(self,e=None):
        print(f"{len(self.rectangles)=}")
        print(f"{len(self.selected)=}")
        for i in self.clipboard:
            print((i.center[0]-self.Xcenter)/self.scale)
            self.rectangles.append(Rectangle(self,i.x1+5,i.y1+5,i.x2+5,i.y2+5,self.create_rectangle(i.x1+5,i.y1+5,i.x2+5,i.y2+5,fill="blue", tags=("rect"))))
            print((self.rectangles[-1].center[0]-self.Xcenter)/self.scale)
        print(f"{len(self.rectangles)=}")
        print(f"{len(self.selected)=}")
    def clear_results(self):
        for i in self.results_block:
            i.config(text="")
    def change_active_shape(self, direction="up"):
        print(direction)
        if direction == "up":
            self.active_shape = next(self.possible_shapes)
        elif direction == "down":
            for i in range(len(self.possible_shape_list)-2): next(self.possible_shapes)
            self.active_shape = next(self.possible_shapes)
        else: 
            print("Error: Invalid command by changing shape.")
            raise ValueError
        print(self.active_shape)
        # Set icon for active_shape:
        if self.active_shape == "Rectangle":
            self.itemconfigure("alap_rectangle",state="normal")
            self.itemconfigure("alap_semicircle",state="hidden")
            self.itemconfigure("alap_quarter_circle",state="hidden")
            self.itemconfigure("alap_triangle",state="hidden")

        elif self.active_shape == "Semicircle":
            self.itemconfigure("alap_semicircle",state="normal")
            self.itemconfigure("alap_rectangle",state="hidden")
            self.itemconfigure("alap_triangle",state="hidden")
            self.itemconfigure("alap_quarter_circle",state="hidden")
            self.start = 0
            self.angle = 180
            # a,b,c,d = self.coords(self.alap_semicircle)
            self.delete(self.alap_semicircle)
            self.alap_semicircle = self.create_arc(30,10,30+2*self.r1,10+2*self.r1,extent=180, start = 0, fill=self.root.colors["sb_draw_2nd"], tags=("alap_semicircle"))
            print(self.r1)

        elif self.active_shape == "quarter_circle":
            self.itemconfigure("alap_quarter_circle",state="normal")
            self.itemconfigure("alap_rectangle",state="hidden")
            self.itemconfigure("alap_triangle",state="hidden")
            self.itemconfigure("alap_semicircle",state="hidden")
            self.start = 0
            self.angle = 90
            # a,b,c,d = self.coords(self.alap_quarter_circle)
            self.delete(self.alap_quarter_circle)
            self.alap_quarter_circle = self.create_arc(30,10,30+2*self.r2,10+2*self.r2,extent=90, start = 0, fill=self.root.colors["sb_draw_2nd"], tags=("alap_quarter_circle"))

        elif self.active_shape == "rightTriangle":
            self.itemconfigure("alap_rectangle", state="hidden")
            self.itemconfigure("alap_semicircle",state="hidden")
            self.itemconfigure("alap_quarter_circle",state="hidden")
            self.itemconfigure("alap_triangle",state="normal")
        else: raise ValueError
        self.auto_scale_default_shape()
        self.move_entry()
    def rotate(self, direction = 90, object = None):
        if len(self.selected)==0:
            if self.active_shape == "Rectangle":
                self.width1, self.height1 = self.height1, self.width1
                self.alap_negyzet.refresh(self.alap_negyzet.x1, self.alap_negyzet.y1, self.alap_negyzet.x1 + self.width1, self.alap_negyzet.y1 + self.height1)
            elif self.active_shape == "Semicircle":
                self.delete(self.alap_semicircle)
                self.start = (self.start+direction)%360
                self.alap_semicircle = self.create_arc(30,10,30+2*self.r1,10+2*self.r1,extent=self.angle, start = self.start , fill=self.root.colors["sb_draw_2nd"], tags=("alap_semicircle"))
            elif self.active_shape == "quarter_circle":
                self.delete(self.alap_quarter_circle)
                self.start = (self.start+direction)%360
                self.alap_quarter_circle = self.create_arc(30,10,30+2*self.r2,10+2*self.r2,extent=self.angle, start = self.start , fill=self.root.colors["sb_draw_2nd"], tags=("alap_quarter_circle"))
            elif self.active_shape == "rightTriangle":
                #self.delete(self.alap_triangle.canvas_repr)
                self.start = (self.start+direction)%360
                #self.alap_triangle.canvas_repr = self.create_polygon())
                self.alap_triangle.rotate(direction)
                self.delete(self.alap_triangle.canvas_repr)
                self.alap_triangle.canvas_repr = self.create_polygon(self.alap_triangle.points[0][0],self.alap_triangle.points[0][1],self.alap_triangle.points[1][0],self.alap_triangle.points[1][1],self.alap_triangle.points[2][0],self.alap_triangle.points[2][1], fill=self.root.colors["sb_draw_2nd"],outline="#000000", tags=("alap_triangle"))
            else: raise TypeError
        else:
            tmp = []
            for i in self.selected:
                #if i.negative: continue
                if i.type == "Rectangle":
                    i.width, i.height = i.height, i.width
                    i.refresh(i.x1, i.y1, i.x1 + i.width, i.y1 + i.height)
                    tmp.append(i)
                    if i.negative:
                        self.negatives.remove(i)
                        self.negatives.append(i)
                        self.check_for_negatives()
                elif i.type == "Semicircle" or i.type == "quarter_circle":
                    self.delete(i.canvas_repr)
                    self.shapes.remove(i)
                    if i.start == 0 and i.start+direction == -90:
                        i.start = 270
                    elif i.start == 270 and i.start+direction == 360:
                        i.start = 0
                    else:
                        i.start = i.start+direction
                    print(i.start, i.angle)
                    rotate_semicircle = Arc(self,self.root,i.center[0],i.center[1],i.r,angle=i.angle, start = i.start, Negative=i.negative)
                    self.itemconfig(rotate_semicircle.canvas_repr,fill="pink")

                    self.shapes.append(rotate_semicircle)
                    tmp.append(rotate_semicircle)
                    if i.negative:
                        self.negatives.remove(i)
                        self.negatives.append(rotate_semicircle)
                        self.check_for_negatives()
                    #self.selected.append(rotate_semicircle)
                elif i.type == "rightTriangle":
                    self.delete(i.canvas_repr)
                    self.shapes.remove(i)
                    i.orientation = i.orientation-direction#! itt ez a - jel ez nem biztos, de így működik jól...
                    rotate_rt = RightTriangle(self,self.root,i.center[0],i.center[1],i.width,i.height, orientation= i.orientation, Negative=i.negative)
                    self.itemconfig(rotate_rt.canvas_repr,fill="pink")
                    self.shapes.append(rotate_rt)
                    tmp.append(rotate_rt)
                    if i.negative:
                        self.negatives.remove(i)
                        self.negatives.append(rotate_rt)
                        self.check_for_negatives()
                    #self.selected.append(rotate_rt)
                    #print(len(self.shapes.rightTriangles))
                else:
                    raise TypeError
            self.selected = tmp
            self.rotation_happend = True
            self.move_entry()
    def move_entry(self):
        if len(self.selected) == 1:
            object = self.selected[0]
            if object.type == "Rectangle":
                self.width_entry.place_forget()
                self.height_entry.place_forget()
                self.width_entry.place(x = object.center[0]-6, y = object.y1 + 2 + object.height)
                self.height_entry.place(x = object.x1 + 2 + object.width , y = object.center[1] -8)
                self.width_entry.delete(0, tk.END)
                self.height_entry.delete(0, tk.END)
                self.width_entry.insert(tk.END, str(round(object.width/self.scale,4)))
                self.height_entry.insert(tk.END, str(round(object.height/self.scale,4)))
            elif object.type == "rightTriangle":
                self.width_entry.place_forget()
                self.height_entry.place_forget()
                if object.orientation <= 0:
                    if object.orientation%360 == 0:
                        self.width_entry.place(x = object.center[0] + object.width/2 - 6, y = object.center[1]+4)
                        self.height_entry.place(x = object.center[0] + 6 + object.width , y = object.center[1]-object.height/2-4)
                    elif object.orientation%270 == 0:
                        self.width_entry.place(x = object.center[0] + object.height + 6 , y = object.center[1]+object.width/2-4)
                        self.height_entry.place(x = object.center[0] + object.height/2 - 6, y = object.center[1]-18)
                    elif object.orientation%180 == 0:
                        self.width_entry.place(x = object.center[0] - object.width/2 - 6, y = object.center[1]-18)
                        self.height_entry.place(x = object.center[0] +6 , y = object.center[1]+object.height/2-4)
                    elif object.orientation%90 == 0:
                        self.width_entry.place(x = object.center[0] + 2 , y = object.center[1]-object.width/2-4)
                        self.height_entry.place(x = object.center[0] - object.height/2 - 6, y = object.center[1]+4)
                else:
                    if object.orientation%360 == 0:
                        self.width_entry.place(x = object.center[0] + object.width/2 - 6, y = object.center[1]+4)
                        self.height_entry.place(x = object.center[0] + 6 + object.width , y = object.center[1]-object.height/2-4)
                    elif object.orientation%270 == 0:
                        self.width_entry.place(x = object.center[0] + 2 , y = object.center[1]-object.width/2-4)
                        self.height_entry.place(x = object.center[0] - object.height/2 - 6, y = object.center[1]+4)
                    elif object.orientation%180 == 0:
                        self.width_entry.place(x = object.center[0] - object.width/2 - 6, y = object.center[1]-18)
                        self.height_entry.place(x = object.center[0] +6 , y = object.center[1]+object.height/2-4)
                    elif object.orientation%90 == 0:
                        self.width_entry.place(x = object.center[0] + object.height + 6 , y = object.center[1]+object.width/2-4)
                        self.height_entry.place(x = object.center[0] + object.height/2 - 6, y = object.center[1]-18)
                self.width_entry.delete(0, tk.END)
                self.height_entry.delete(0, tk.END)
                self.width_entry.insert(tk.END, str(round(object.width/self.scale,4)))
                self.height_entry.insert(tk.END, str(round(object.height/self.scale,4)))
            elif object.type == "Semicircle":
                self.width_entry.place_forget()
                self.height_entry.place_forget()
                if object.start == 0:
                    self.height_entry.place(x = object.center[0] + 2 + object.r , y = object.center[1] -12)
                elif object.start == 90:
                    self.height_entry.place(x = object.center[0] + 2 , y = object.center[1] -12)
                elif object.start == 180:
                    self.height_entry.place(x = object.center[0] + 2 + object.r , y = object.center[1] -12)
                elif object.start == 270:
                    self.height_entry.place(x = object.center[0] + 2 + object.r , y = object.center[1] -12)
                self.height_entry.delete(0, tk.END)
                self.height_entry.insert(tk.END, str(round(object.r/self.scale,4)))
            elif object.type == "quarter_circle":
                self.width_entry.place_forget()
                self.height_entry.place_forget()
                if object.start == 0:
                    self.height_entry.place(x = object.center[0] + 2 + object.r , y = object.center[1] -12)
                elif object.start == 90:
                    self.height_entry.place(x = object.center[0] + 2 , y = object.center[1] -12)
                elif object.start == 180:
                    self.height_entry.place(x = object.center[0] + 2 , y = object.center[1] -12)
                elif object.start == 270:
                    self.height_entry.place(x = object.center[0] + 2 + object.r , y = object.center[1] -12)
                self.height_entry.delete(0, tk.END)
                self.height_entry.insert(tk.END, str(round(object.r/self.scale,4)))
        else:
            #### move the size entry boxes to the deafult place
            if self.active_shape == "Rectangle":
                self.width_entry.place_forget()
                self.height_entry.place_forget()
                self.width_entry.place(x = 24 + self.width1/2, y = 12 + self.height1)
                self.height_entry.place(x = 32 + self.width1, y = 2 + self.height1/2)
                self.width_entry.delete(0, tk.END)
                self.height_entry.delete(0, tk.END)
                self.width_entry.insert(tk.END, str(round(self.width1/self.scale,4)))
                self.height_entry.insert(tk.END, str(round(self.height1/self.scale,4)))
            elif self.active_shape == "rightTriangle":
                self.width_entry.place_forget()
                self.height_entry.place_forget()
                if self.start == 0:
                    self.width_entry.place(x = 32 + self.width2/2, y = 12 + self.height2)
                    self.height_entry.place(x = 42 + self.width2, y = 2 + self.height2/2)
                elif self.start == 90:
                    self.width_entry.place(x = 42 + self.height2, y = 2 + self.width2/2)
                    self.height_entry.place(x = 32 + self.height2/2, y = 12 + self.width2)
                elif self.start == 180:
                    self.width_entry.place(x = 32 + self.width2/2, y = 12 + self.height2)
                    self.height_entry.place(x = 42 + self.width2, y = 2 + self.height2/2)
                elif self.start == 270:
                    self.width_entry.place(x = 42 + self.height2, y = 2 + self.width2/2)
                    self.height_entry.place(x = 32 + self.height2/2, y = 12 + self.width2) 
                self.width_entry.delete(0, tk.END)
                self.height_entry.delete(0, tk.END)
                self.width_entry.insert(tk.END, str(round(self.width2/self.scale,4)))
                self.height_entry.insert(tk.END, str(round(self.height2/self.scale,4)))
            elif self.active_shape == "Semicircle":
                self.width_entry.place_forget()
                self.height_entry.place_forget()
                if self.start == 0:
                    self.height_entry.place(x = 32 + self.r1*2, y = 2 + self.r1)
                elif self.start == 90:
                    self.height_entry.place(x = 32 + self.r1, y = 2 + self.r1)
                elif self.start == 180:
                    self.height_entry.place(x = 32 + self.r1*2, y = 2 + self.r1)
                elif self.start == 270:
                    self.height_entry.place(x = 32 + self.r1*2, y = 2 + self.r1)
                self.height_entry.delete(0, tk.END)
                self.height_entry.insert(tk.END, str(round(self.r1/self.scale,4)))
            elif self.active_shape == "quarter_circle":
                self.width_entry.place_forget()
                self.height_entry.place_forget()
                if self.start == 0:
                    self.height_entry.place(x = 32 + self.r2*2, y = 2 + self.r2)
                elif self.start == 90:
                    self.height_entry.place(x = 32 + self.r2, y = 2 + self.r2)
                elif self.start == 180:
                    self.height_entry.place(x = 32 + self.r2, y = 2 + self.r2)
                elif self.start == 270:
                    self.height_entry.place(x = 32 + self.r2*2, y = 2 + self.r2)
                self.height_entry.delete(0, tk.END)
                self.height_entry.insert(tk.END, str(round(self.r2/self.scale,4)))
    def focus_height(self):
        self.height_entry.focus_set()
        self.height_entry.select_range(0, 'end')
    def focus_width(self):
        self.width_entry.focus_set()
        self.width_entry.select_range(0, 'end')
    def check_for_negatives(self):
        self.negativ_in_wrong_position = False
        if len(self.negatives)== 0: return 0
        positives = [i for i in self.shapes if i.negative == False]
        geom = []
        for i in positives:
            if type(i) == Rectangle:
                geom.append(Polygon(i.get_charachteristic_points()))
            elif type(i) == RightTriangle:
                geom.append(Polygon(i.points))
            elif type(i) == Arc:
                geom.append(Polygon(i.simplify()))
            else: raise TypeError    
        union = unary_union(geom)
        for i in self.negatives:
            if type(i) == Rectangle:
                a = (Polygon(i.get_charachteristic_points()))
            elif type(i) == RightTriangle:
                a = (Polygon(i.points))
            elif type(i) == Arc:
                a = (Polygon(i.simplify()))
            else: raise TypeError
            if union.contains(a):
                self.itemconfig(i.canvas_repr,fill="grey")
            else:
                self.itemconfig(i.canvas_repr,fill="#8B0000")
                self.negativ_in_wrong_position = True
            if i in self.selected: self.itemconfig(i.canvas_repr,fill="#e75480")
    def auto_scale(self):
        x_coords = [0]
        y_coords = [0]
        width = [0]
        height = [0]
        for i in self.shapes:
            if i.type == "Rectangle" or i.type == "rightTriangle":
                x_val = abs(i.center[0]-self.Xcenter)+i.width
                x_coords.append(x_val)
                y_val = abs(self.Ycenter-i.center[1])+i.height
                y_coords.append(y_val)
                w_val = i.width
                width.append(w_val)
                h_val = i.height
                height.append(h_val)
            else:
                x_val = abs(i.center[0]-self.Xcenter)+i.r
                x_coords.append(x_val)
                y_val = abs(self.Ycenter-i.center[1])+i.r
                y_coords.append(y_val)
                h_val = i.r
                height.append(h_val)
        max_x = max(x_coords)
        max_y = max(y_coords)
        max_width = max(x_coords)
        max_height = max(y_coords)
        if max_width < self.canvas_width/80 or max_height < self.canvas_height/60:
            difference = max(max_width/self.canvas_width*26, max_height/self.canvas_height*20)
            scale_factor = round(np.log(difference)/np.log(self.scale_factor))-1
            self.rescale(self.scale_factor**(-scale_factor))
            print("zoom_in", scale_factor)
        if max_x > self.canvas_width/2 or max_y > self.canvas_height/2:
            difference = max(max_x/self.canvas_width*2, max_y/self.canvas_height*2)
            scale_factor = round(np.log(difference)/np.log(self.scale_factor))+1
            self.rescale(self.scale_factor**(-scale_factor))
            # TODO: zoom in in case of too small object
        self.auto_scale_default_shape()
    def auto_scale_default(self):
        if self.active_shape == "Rectangle":
            if self.width1 < self.canvas_width/80 or self.height1 < self.canvas_height/60:
                difference = min(self.width1/self.canvas_width*26, self.height1/self.canvas_height*20)
                scale_factor = round(np.log(difference)/np.log(self.scale_factor))-1
                self.rescale(self.scale_factor**(-scale_factor), True)
            if self.width1 > self.canvas_width/4 or self.height1 > self.canvas_height/4:
                difference = max(self.width1/self.canvas_width*4, self.height1/self.canvas_height*4)
                scale_factor = round(np.log(difference)/np.log(self.scale_factor))+1
                self.rescale(self.scale_factor**(-scale_factor), True)
        elif self.active_shape == "rightTriangle":
            if self.width2 < self.canvas_width/80 or self.height2 < self.canvas_height/60:
                difference = min(self.width2/self.canvas_width*26, self.height2/self.canvas_height*20)
                scale_factor = round(np.log(difference)/np.log(self.scale_factor))-1
                self.rescale(self.scale_factor**(-scale_factor), True)
            if self.width2 > self.canvas_width/4 or self.height2 > self.canvas_height/4:
                difference = max(self.width2/self.canvas_width*4, self.height2/self.canvas_height*4)
                scale_factor = round(np.log(difference)/np.log(self.scale_factor))+1
                self.rescale(self.scale_factor**(-scale_factor), True)
        elif self.active_shape == "Semicircle":
            if self.r1 < self.canvas_width/80 or self.r1 < self.canvas_height/60:
                difference = min(self.r1/self.canvas_width*26, self.r1/self.canvas_height*20)
                scale_factor = round(np.log(difference)/np.log(self.scale_factor))-1
                self.rescale(self.scale_factor**(-scale_factor), True)
            if self.r1 > self.canvas_width/4 or self.r1 > self.canvas_height/4:
                difference = max(self.r1/self.canvas_width*4, self.r1/self.canvas_height*4)
                scale_factor = round(np.log(difference)/np.log(self.scale_factor))+1
                self.rescale(self.scale_factor**(-scale_factor), True)
        elif self.active_shape == "quarter_circle":
            if self.r2 < self.canvas_width/80 or self.r2 < self.canvas_height/60:
                difference = min(self.r2/self.canvas_width*26, self.r2/self.canvas_height*20)
                scale_factor = round(np.log(difference)/np.log(self.scale_factor))-1
                self.rescale(self.scale_factor**(-scale_factor), True)
            if self.r2 > self.canvas_width/4 or self.r2 > self.canvas_height/4:
                difference = max(self.r2/self.canvas_width*4, self.r2/self.canvas_height*4)
                scale_factor = round(np.log(difference)/np.log(self.scale_factor))+1
                self.rescale(self.scale_factor**(-scale_factor), True)
    def auto_scale_default_shape(self, button = False):
        if button == False:
            if self.active_shape == "Rectangle":
                if self.width1 < self.canvas_width/80 or self.height1 < self.canvas_height/60:
                    difference = min(self.width1/self.canvas_width*26, self.height1/self.canvas_height*20)
                    scale_factor = round(np.log(difference)/np.log(self.scale_factor))-1
                    self.width1 = self.width1*self.scale_factor**(-scale_factor)
                    self.height1 = self.height1*self.scale_factor**(-scale_factor)
                    self.width2 = self.width2*self.scale_factor**(-scale_factor)
                    self.height2 = self.height2*self.scale_factor**(-scale_factor)
                    self.r1 = self.r1*self.scale_factor**(-scale_factor)
                    self.r2 = self.r2*self.scale_factor**(-scale_factor)
                    self.coords(self.alap_negyzet.canvas_repr, 30,10,30+self.width1,10+self.height1)
                if self.width1 > self.canvas_width/4 or self.height1 > self.canvas_height/4:
                    difference = max(self.width1/self.canvas_width*4, self.height1/self.canvas_height*4)
                    scale_factor = round(np.log(difference)/np.log(self.scale_factor))+1
                    self.width1 = self.width1*self.scale_factor**(-scale_factor)
                    self.height1 = self.height1*self.scale_factor**(-scale_factor)
                    self.width2 = self.width2*self.scale_factor**(-scale_factor)
                    self.height2 = self.height2*self.scale_factor**(-scale_factor)
                    self.r1 = self.r1*self.scale_factor**(-scale_factor)
                    self.r2 = self.r2*self.scale_factor**(-scale_factor)
                    self.coords(self.alap_negyzet.canvas_repr, 30,10,30+self.width1,10+self.height1)
            elif self.active_shape == "rightTriangle":
                if self.width2 < self.canvas_width/80 or self.height2 < self.canvas_height/60:
                    difference = min(self.width2/self.canvas_width*26, self.height2/self.canvas_height*20)
                    scale_factor = round(np.log(difference)/np.log(self.scale_factor))-1
                    self.width1 = self.width1*self.scale_factor**(-scale_factor)
                    self.height1 = self.height1*self.scale_factor**(-scale_factor)
                    self.width2 = self.width2*self.scale_factor**(-scale_factor)
                    self.height2 = self.height2*self.scale_factor**(-scale_factor)
                    self.r1 = self.r1*self.scale_factor**(-scale_factor)
                    self.r2 = self.r2*self.scale_factor**(-scale_factor)
                    l,r,t,b = self.alap_triangle.get_bounding_box()
                    self.alap_triangle.refresh(self.alap_triangle.center[0],self.alap_triangle.center[1], self.width2, self.height2)
                    l2,r2,t2,b2 = self.alap_triangle.get_bounding_box()
                    self.alap_triangle.translate(l-l2,t-t2)
                if self.width2 > self.canvas_width/4 or self.height2 > self.canvas_height/4:
                    difference = max(self.width2/self.canvas_width*4, self.height2/self.canvas_height*4)
                    scale_factor = round(np.log(difference)/np.log(self.scale_factor))+1
                    self.width1 = self.width1*self.scale_factor**(-scale_factor)
                    self.height1 = self.height1*self.scale_factor**(-scale_factor)
                    self.width2 = self.width2*self.scale_factor**(-scale_factor)
                    self.height2 = self.height2*self.scale_factor**(-scale_factor)
                    self.r1 = self.r1*self.scale_factor**(-scale_factor)
                    self.r2 = self.r2*self.scale_factor**(-scale_factor)
                    l,r,t,b = self.alap_triangle.get_bounding_box()
                    self.alap_triangle.refresh(self.alap_triangle.center[0],self.alap_triangle.center[1], self.width2, self.height2)
                    l2,r2,t2,b2 = self.alap_triangle.get_bounding_box()
                    self.alap_triangle.translate(l-l2,t-t2)
            elif self.active_shape == "Semicircle":
                if self.r1 < self.canvas_width/80 or self.r1 < self.canvas_height/60:
                    difference = min(self.r1/self.canvas_width*26, self.r1/self.canvas_height*20)
                    scale_factor = round(np.log(difference)/np.log(self.scale_factor))-1
                    self.width1 = self.width1*self.scale_factor**(-scale_factor)
                    self.height1 = self.height1*self.scale_factor**(-scale_factor)
                    self.width2 = self.width2*self.scale_factor**(-scale_factor)
                    self.height2 = self.height2*self.scale_factor**(-scale_factor)
                    self.r1 = self.r1*self.scale_factor**(-scale_factor)
                    self.r2 = self.r2*self.scale_factor**(-scale_factor)
                    self.coords(self.alap_semicircle, 40,10,40+self.r1*2,10+self.r1*2)
                if self.r1*2 > self.canvas_width/4 or self.r1*2 > self.canvas_height/4:
                    difference = max(self.r1*2/self.canvas_width*4, self.r1*2/self.canvas_height*4)
                    scale_factor = round(np.log(difference)/np.log(self.scale_factor))+1
                    self.width1 = self.width1*self.scale_factor**(-scale_factor)
                    self.height1 = self.height1*self.scale_factor**(-scale_factor)
                    self.width2 = self.width2*self.scale_factor**(-scale_factor)
                    self.height2 = self.height2*self.scale_factor**(-scale_factor)
                    self.r1 = self.r1*self.scale_factor**(-scale_factor)
                    self.r2 = self.r2*self.scale_factor**(-scale_factor)
                    self.coords(self.alap_semicircle, 40,10,40+self.r1*2,10+self.r1*2)
            elif self.active_shape == "quarter_circle":
                if self.r2 < self.canvas_width/80 or self.r2 < self.canvas_height/60:
                    difference = min(self.r2/self.canvas_width*26, self.r2/self.canvas_height*20)
                    scale_factor = round(np.log(difference)/np.log(self.scale_factor))-1
                    self.width1 = self.width1*self.scale_factor**(-scale_factor)
                    self.height1 = self.height1*self.scale_factor**(-scale_factor)
                    self.width2 = self.width2*self.scale_factor**(-scale_factor)
                    self.height2 = self.height2*self.scale_factor**(-scale_factor)
                    self.r1 = self.r1*self.scale_factor**(-scale_factor)
                    self.r2 = self.r2*self.scale_factor**(-scale_factor)
                    self.coords(self.alap_quarter_circle, 40,10,40+self.r2*2,10+self.r2*2)
                if self.r2*2 > self.canvas_width/4 or self.r2*2 > self.canvas_height/4:
                    difference = max(self.r2*2/self.canvas_width*4, self.r2*2/self.canvas_height*4)
                    scale_factor = round(np.log(difference)/np.log(self.scale_factor))+1
                    self.width1 = self.width1*self.scale_factor**(-scale_factor)
                    self.height1 = self.height1*self.scale_factor**(-scale_factor)
                    self.width2 = self.width2*self.scale_factor**(-scale_factor)
                    self.height2 = self.height2*self.scale_factor**(-scale_factor)
                    self.r1 = self.r1*self.scale_factor**(-scale_factor)
                    self.r2 = self.r2*self.scale_factor**(-scale_factor)
                    self.coords(self.alap_quarter_circle, 40,10,40+self.r2*2,10+self.r2*2)

class sb_side_menu(tk.Frame):
    def __init__(self,root):
        super().__init__(root,width=30, bg=root.colors['secondary_color'])
        self.root = root
