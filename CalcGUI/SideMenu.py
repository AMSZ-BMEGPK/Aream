import tkinter as tk
from tkinter import ttk
from tkinter.constants import FLAT
from PlotFunctions import plot
class SideMenu(tk.Frame):
    def __init__(self, root):
        super().__init__(root,width=40, bg=root.colors['secondary_color'])
        self.root = root
        self.shape = None

# DEFINE SIDEMENU OBJECTS --------------------------------------------------------------------------------------------------------------
        self.canvas = tk.Canvas(self, bg=root.colors['secondary_color'], highlightthickness=0)
        # self.canvas.grid(row=0, column=0, sticky="NSEW")
        self.canvas.pack(fill=tk.BOTH, expand = True)

        # result label font
        result_font = "Roboto", 11
        # input labels font
        input_font = "Roboto", 11
        
        ## Custom combobox ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        self.combo_open = tk.BooleanVar(False)

        self.combo_default_img = tk.PhotoImage(file=f"{root.colors['path']}combobox/combo_default.png")
        self.combo_default = tk.Label(self.canvas, image=self.combo_default_img, bg=self["background"], activebackground=self["background"])
        self.combo_default.bind('<Button-1>', func=lambda e:self.combo_click())
        self.combo_default.grid(row=1, column=0, columnspan=5)
        self.combo_default["border"] = "0"

        self.combo_rectangle_img = tk.PhotoImage(file=f"{root.colors['path']}combobox/combo_rectangle.png")
        self.combo_rectangle = tk.Label(self.canvas, image=self.combo_rectangle_img, bg=self["background"], activebackground=self["background"])
        self.combo_rectangle.bind('<Button-1>', func=lambda e:self.rectangle_click())
        self.combo_rectangle["border"] = "0"

        self.combo_circle_img = tk.PhotoImage(file=f"{root.colors['path']}combobox/combo_circle.png")
        self.combo_circle = tk.Label(self.canvas, image=self.combo_circle_img, bg=self["background"], activebackground=self["background"])
        self.combo_circle.bind('<Button-1>', func=lambda e:self.circle_click())
        self.combo_circle["border"] = "0"

        self.combo_ellipse_img = tk.PhotoImage(file=f"{root.colors['path']}combobox/combo_ellipse.png")
        self.combo_ellipse = tk.Label(self.canvas, image=self.combo_ellipse_img, bg=self["background"], activebackground=self["background"])
        self.combo_ellipse.bind('<Button-1>', func=lambda e:self.ellipse_click())
        self.combo_ellipse["border"] = "0"

        self.combo_isosceles_img = tk.PhotoImage(file=f"{root.colors['path']}combobox/combo_isosceles.png")
        self.combo_isosceles = tk.Label(self.canvas, image=self.combo_isosceles_img, bg=self["background"], activebackground=self["background"])
        self.combo_isosceles.bind('<Button-1>', func=lambda e:self.isosceles_click())
        self.combo_isosceles["border"] = "0"

        self.combo_right_img = tk.PhotoImage(file=f"{root.colors['path']}combobox/combo_right.png")
        self.combo_right = tk.Label(self.canvas, image=self.combo_right_img, bg=self["background"], activebackground=self["background"])
        self.combo_right.bind('<Button-1>', func=lambda e:self.right_click())
        self.combo_right["border"] = "0"

        self.combo_rectangle_hover_img = tk.PhotoImage(file=f"{root.colors['path']}combobox/combo_rectangle_hover.png")
        self.combo_rectangle.bind("<Enter>", func=lambda e: self.combo_rectangle.config(image=self.combo_rectangle_hover_img))
        self.combo_rectangle.bind("<Leave>", func=lambda e: self.combo_rectangle.config(image=self.combo_rectangle_img))
        
        self.combo_circle_hover_img = tk.PhotoImage(file=f"{root.colors['path']}combobox/combo_circle_hover.png")
        self.combo_circle.bind("<Enter>", func=lambda e: self.combo_circle.config(image=self.combo_circle_hover_img))
        self.combo_circle.bind("<Leave>", func=lambda e: self.combo_circle.config(image=self.combo_circle_img))

        self.combo_ellipse_hover_img = tk.PhotoImage(file=f"{root.colors['path']}combobox/combo_ellipse_hover.png")
        self.combo_ellipse.bind("<Enter>", func=lambda e: self.combo_ellipse.config(image=self.combo_ellipse_hover_img))
        self.combo_ellipse.bind("<Leave>", func=lambda e: self.combo_ellipse.config(image=self.combo_ellipse_img))

        self.combo_isosceles_hover_img = tk.PhotoImage(file=f"{root.colors['path']}combobox/combo_isosceles_hover.png")
        self.combo_isosceles.bind("<Enter>", func=lambda e: self.combo_isosceles.config(image=self.combo_isosceles_hover_img))
        self.combo_isosceles.bind("<Leave>", func=lambda e: self.combo_isosceles.config(image=self.combo_isosceles_img))

        self.combo_right_hover_img = tk.PhotoImage(file=f"{root.colors['path']}combobox/combo_right_hover.png")
        self.combo_right.bind("<Enter>", func=lambda e: self.combo_right.config(image=self.combo_right_hover_img))
        self.combo_right.bind("<Leave>", func=lambda e: self.combo_right.config(image=self.combo_right_img))


        # place holder label
        self.lbl = tk.Label(self.canvas, width = 40, bg = self["background"] , fg=root.colors['text_color'])
        self.lbl.grid(row=0, column=1)

        self.lbl2 = tk.Label(self.canvas, height = 300, bg = self["background"] , fg=root.colors['text_color'])
        # self.lbl2.grid(row=200, column=1)


        # dimension input labels
        self.l1 = tk.Label(self.canvas, text="Width", bg=self["background"], fg=root.colors['text_color'], font=input_font)
        self.m1 = tk.Label(self.canvas, text=self.root.unit, bg=self["background"], fg=root.colors['text_color'], font=input_font)
        self.l2 = tk.Label(self.canvas, text="Heigth", bg=self["background"], fg=root.colors['text_color'], font=input_font)
        self.m2 = tk.Label(self.canvas, text=self.root.unit, bg=self["background"], fg=root.colors['text_color'], font=input_font)

        # dimension input entries
        self.e1 = tk.Entry(self.canvas, width = 10, bg=root.colors['entry_color'], fg=root.colors['text_color'],insertbackground=root.colors['text_color'])
        self.e2 = tk.Entry(self.canvas, width = 10, bg=root.colors['entry_color'], fg=root.colors['text_color'],insertbackground=root.colors['text_color'])

        # transformed coordinate system input labels
        self.tl1 = tk.Label(self.canvas, text="x", bg=self["background"], fg=root.colors['text_color'], font=input_font)
        self.tm1 = tk.Label(self.canvas, text=self.root.unit, bg=self["background"], fg=root.colors['text_color'], font=input_font)
        self.tl2 = tk.Label(self.canvas, text="y", bg=self["background"], fg=root.colors['text_color'], font=input_font)
        self.tm2 = tk.Label(self.canvas, text=self.root.unit, bg=self["background"], fg=root.colors['text_color'], font=input_font)
        self.tl3 = tk.Label(self.canvas, text="phi", bg=self["background"], fg=root.colors['text_color'], font=input_font)
        self.tm3 = tk.Label(self.canvas, text=self.root.angle_unit, bg=self["background"], fg=root.colors['text_color'], font=input_font)

        # transformed coordinate system input entries
        self.te1 = tk.Entry(self.canvas, width = 10, bg=root.colors['entry_color'], fg=root.colors['text_color'], state='disabled', disabledbackground=root.colors['disabled_color'],insertbackground=root.colors['text_color'])
        self.te2 = tk.Entry(self.canvas, width = 10, bg=root.colors['entry_color'], fg=root.colors['text_color'], state='disabled', disabledbackground=root.colors['disabled_color'],insertbackground=root.colors['text_color'])
        self.te3 = tk.Entry(self.canvas, width = 10, bg=root.colors['entry_color'], fg=root.colors['text_color'], state='disabled', disabledbackground=root.colors['disabled_color'],insertbackground=root.colors['text_color'])

        # thickness input labels
        self.thl1 = tk.Label(self.canvas, text="t", bg=self["background"], fg=root.colors['text_color'], font=input_font)
        self.thm1 = tk.Label(self.canvas, text=self.root.unit, bg=self["background"], fg=root.colors['text_color'], font=input_font)

        # thickness input entry
        self.the1 = tk.Entry(self.canvas, width = 10, bg=root.colors['entry_color'], fg=root.colors['text_color'], state='disabled', disabledbackground=root.colors['disabled_color'],insertbackground=root.colors['text_color'])

        # calculate button
        self.buttonimage = tk.PhotoImage(file=f"{root.colors['path']}/calculate_button.png")
        self.calc = tk.Label(self.canvas, image=self.buttonimage, activebackground=self["background"], border = 0, bg =self["background"])
        self.calc.bind('<Button-1>', func=lambda e: self.root.calculate())

        # result labels
        self.result0 = tk.Label(self.canvas, text="", bg=self["background"], fg=root.colors['text_color'], font=result_font)
        self.result1 = tk.Label(self.canvas, text="", bg=self["background"], fg=root.colors['text_color'], font=result_font)
        self.result2 = tk.Label(self.canvas, text="", bg=self["background"], fg=root.colors['text_color'], font=result_font)
        self.result3 = tk.Label(self.canvas, text="", bg=self["background"], fg=root.colors['text_color'], font=result_font)
        self.result4 = tk.Label(self.canvas, text="", bg=self["background"], fg=root.colors['text_color'], font=result_font)
        self.result5 = tk.Label(self.canvas, text="", bg=self["background"], fg=root.colors['text_color'], font=result_font)
        self.result6 = tk.Label(self.canvas, text="", bg=self["background"], fg=root.colors['text_color'], font=result_font)
        self.result7 = tk.Label(self.canvas, text="", bg=self["background"], fg=root.colors['text_color'], font=result_font)
        self.result8 = tk.Label(self.canvas, text="", bg=self["background"], fg=root.colors['text_color'], font=result_font)
        self.result9 = tk.Label(self.canvas, text="", bg=self["background"], fg=root.colors['text_color'], font=result_font)
        self.result10 = tk.Label(self.canvas, text="", bg=self["background"], fg=root.colors['text_color'], font=result_font)
        self.result11 = tk.Label(self.canvas, text="", bg=self["background"], fg=root.colors['text_color'], font=result_font)
        self.result12 = tk.Label(self.canvas, text="", bg=self["background"], fg=root.colors['text_color'], font=result_font)
        self.result0.grid(row=12, column = 0, columnspan=4, padx=15, pady=2, sticky=tk.W)
        self.result1.grid(row=13, column = 0, columnspan=4, padx=30, pady=2, sticky=tk.W)
        self.result2.grid(row=14, column = 0, columnspan=4, padx=30, pady=2, sticky=tk.W)
        self.result3.grid(row=15, column = 0, columnspan=4, padx=30, pady=2, sticky=tk.W)
        self.result4.grid(row=16, column = 0, columnspan=4, padx=30, pady=2, sticky=tk.W)
        self.result5.grid(row=17, column = 0, columnspan=4, padx=30, pady=2, sticky=tk.W) # Ip
        self.result6.grid(row=18, column = 0, columnspan=4, padx=15, pady=2, sticky=tk.W)
        self.result7.grid(row=19, column = 0, columnspan=4, padx=30, pady=2, sticky=tk.W)
        self.result8.grid(row=20, column = 0, columnspan=4, padx=30, pady=2, sticky=tk.W)
        self.result9.grid(row=21, column = 0, columnspan=4, padx=30, pady=2, sticky=tk.W)
        self.result10.grid(row=22, column = 0, columnspan=4, padx=15, pady=2, sticky=tk.W)
        self.result11.grid(row=23, column = 0, columnspan=4, padx=30, pady=2, sticky=tk.W)
        self.result12.grid(row=24, column = 0, columnspan=4, padx=30, pady=2, sticky=tk.W)

        # Checkbox: set thickness
        self.thickness = tk.Checkbutton(
            self.canvas, text = "Falvastagság hozzáadása",
            variable = self.root.thickness_on, onvalue=True, offvalue=False, font=input_font, 
            bg = self["background"], fg=root.colors['text_color'], selectcolor=self["background"],
            command = lambda: [plot(root, self.shape, self.root.coordinate_on.get(), self.root.dimension_lines_on.get(), self.root.transformed_coordinate_on.get(), self.root.thickness_on.get(), root.colors, root.angle_unit),
            entry_enable(self.the1, self.root.thickness_on)])

        # Checkbox: transformed coordinate system
        self.transformed_coordinate_system = tk.Checkbutton(
            self.canvas, text = "Transzformált koordináta rendszer", font=input_font, 
            variable = self.root.transformed_coordinate_on, onvalue=True, offvalue=False,
            bg = self["background"], fg=root.colors['text_color'], selectcolor=self["background"],
            command = lambda: [plot(root, self.shape, self.root.coordinate_on.get(), self.root.dimension_lines_on.get(), self.root.transformed_coordinate_on.get(), self.root.thickness_on.get(), root.colors, root.angle_unit),
            entry_enable(self.te1, self.root.transformed_coordinate_on),
            entry_enable(self.te2, self.root.transformed_coordinate_on),
            entry_enable(self.te3, self.root.transformed_coordinate_on)])

        # append entry objects to controls array
        self.controls = []
        self.controls.append({"name":self.l1, "entry":self.e1, "unit":self.m1, "unit_type": "length"})
        self.controls.append({"name":self.l2, "entry":self.e2, "unit":self.m2, "unit_type": "length"})
        self.controls.append({"name":self.tl1, "entry":self.te1, "unit":self.tm1, "unit_type": "length"})
        self.controls.append({"name":self.tl2, "entry":self.te2, "unit":self.tm2, "unit_type": "length"})
        self.controls.append({"name":self.tl3, "entry":self.te3, "unit":self.tm3, "unit_type": "degree"})
        self.controls.append({"name":self.thl1, "entry":self.the1, "unit":self.thm1, "unit_type": "length"})

        # append result label to indicators
        self.indicators = []
        self.indicators.append(self.result0)
        self.indicators.append(self.result1)
        self.indicators.append(self.result2)
        self.indicators.append(self.result3)
        self.indicators.append(self.result4)
        self.indicators.append(self.result5)
        self.indicators.append(self.result6)
        self.indicators.append(self.result7)
        self.indicators.append(self.result8)
        self.indicators.append(self.result9)
        self.indicators.append(self.result10)
        self.indicators.append(self.result11)
        self.indicators.append(self.result12)
        self.indicators.append(self.lbl)
        self.indicators.append(self.lbl2)
        self.indicators.append(self.calc)

        self.checkbox_indicators = []
        self.checkbox_indicators.append(self.transformed_coordinate_system)
        self.checkbox_indicators.append(self.thickness)

        def entry_enable(entry, var):
            if var.get() == False:
                entry.configure(state='disabled')
            elif var.get() == True:
                entry.configure(state='normal')

        ### VARIABLES-------------------------------------------------------------------------------
        # y-paddign between input widgets
        self.pady_val = 1
## COMBOBOX FUNCTIONS --------------------------------------------------------------------------------------------------------------------------------------------------------
    def combo_show(self):
        self.combo_open.set(True)
        self.combo_default.grid(row=1, column=0, columnspan=5)
        self.combo_rectangle.place(bordermode=tk.OUTSIDE, relx=0.5,y=55, anchor=tk.N)
        self.combo_rectangle.lift()
        self.combo_circle.place(bordermode=tk.OUTSIDE, relx=0.5,y=80, anchor=tk.N)
        self.combo_circle.lift()
        self.combo_ellipse.place(bordermode=tk.OUTSIDE, relx=0.5,y=105, anchor=tk.N)
        self.combo_ellipse.lift()
        self.combo_isosceles.place(bordermode=tk.OUTSIDE, relx=0.5,y=130, anchor=tk.N)
        self.combo_isosceles.lift()
        self.combo_right.place(bordermode=tk.OUTSIDE, relx=0.5,y=155, anchor=tk.N)
        self.combo_right.lift()
    def combo_clear(self):
        self.combo_open.set(False)
        self.combo_rectangle.place_forget()
        self.combo_circle.place_forget()
        self.combo_ellipse.place_forget()
        self.combo_isosceles.place_forget()
        self.combo_right.place_forget()
        self.canvas.update()

    def rectangle_click(self):
        if self.combo_open.get() == False:
            self.combo_rectangle.grid_forget()
            self.combo_show()
        
        else:
            self.combo_clear()
            # self.combo_rectangle.grid(row=1, column=0, columnspan=5)
            self.combo_default_img = tk.PhotoImage(file=f"{self.root.colors['path']}combobox/combo_rectangle_closed.png")
            self.combo_default = tk.Label(self.canvas, image=self.combo_default_img, bg=self["background"], activebackground=self["background"])
            self.combo_default.bind('<Button-1>', func=lambda e:self.combo_click())
            self.combo_default.grid(row=1, column=0, columnspan=5)
            self.combo_default["border"] = "0"
            self.root.choose_object("Rectangle")
    def circle_click(self):
        if self.combo_open.get() == False:
            self.combo_circle.grid_forget()
            self.combo_show()
        
        else:
            self.combo_clear()
            # self.combo_circle.grid(row=1, column=0, columnspan=5)
            self.combo_default_img = tk.PhotoImage(file=f"{self.root.colors['path']}combobox/combo_circle_closed.png")
            self.combo_default = tk.Label(self.canvas, image=self.combo_default_img, bg=self["background"], activebackground=self["background"])
            self.combo_default.bind('<Button-1>', func=lambda e:self.combo_click())
            self.combo_default.grid(row=1, column=0, columnspan=5)
            self.combo_default["border"] = "0"
            self.root.choose_object("Circle")
    def ellipse_click(self):
        if self.combo_open.get() == False:
            self.combo_ellipse.grid_forget()
            self.combo_show()
        
        else:
            self.combo_clear()
            # self.combo_ellipse.grid(row=1, column=0, columnspan=5)
            self.combo_default_img = tk.PhotoImage(file=f"{self.root.colors['path']}combobox/combo_ellipse_closed.png")
            self.combo_default = tk.Label(self.canvas, image=self.combo_default_img, bg=self["background"], activebackground=self["background"])
            self.combo_default.bind('<Button-1>', func=lambda e:self.combo_click())
            self.combo_default.grid(row=1, column=0, columnspan=5)
            self.combo_default["border"] = "0"
            self.root.choose_object("Ellipse")
    def isosceles_click(self):
        if self.combo_open.get() == False:
            self.combo_isosceles.grid_forget()
            self.combo_show()
        
        else:
            self.combo_clear()
            # self.combo_isosceles.grid(row=1, column=0, columnspan=5)
            self.combo_default_img = tk.PhotoImage(file=f"{self.root.colors['path']}combobox/combo_isosceles_closed.png")
            self.combo_default = tk.Label(self.canvas, image=self.combo_default_img, bg=self["background"], activebackground=self["background"])
            self.combo_default.bind('<Button-1>', func=lambda e:self.combo_click())
            self.combo_default.grid(row=1, column=0, columnspan=5)
            self.combo_default["border"] = "0"
            self.root.choose_object("Isosceles_triangle")
    def right_click(self):
            if self.combo_open.get() == False:
                self.combo_right.grid_forget()
                self.combo_show()

            else:
                self.combo_clear()
                self.combo_right.grid(row=1, column=0, columnspan=5)
                self.combo_default_img = tk.PhotoImage(file=f"{self.root.colors['path']}combobox/combo_right_closed.png")
                self.combo_default = tk.Label(self.canvas, image=self.combo_default_img, bg=self["background"], activebackground=self["background"])
                self.combo_default.bind('<Button-1>', func=lambda e:self.combo_click())
                self.combo_default.grid(row=1, column=0, columnspan=5)
                self.combo_default["border"] = "0"
                self.root.choose_object("Right_triangle")
    def combo_click(self):
        if self.combo_open.get() == False:
            self.combo_default.grid_forget()
            self.combo_show()
        else:
            self.combo_clear()
            self.combo_default.grid(row=1, column=0, columnspan=5)




    def change_color(self, color):
        self["background"] = color["secondary_color"]
        self.canvas["bg"] = self["background"]
        for i in self.controls:
            i["entry"].config({"background": color["entry_color"]})
            i["entry"].config({"fg": color["text_color"]})
            i["name"].config({"fg": color["text_color"]})
            i["name"].config({"background": color["secondary_color"]})
            i["unit"].config({"fg": color["text_color"]})
            i["unit"].config({"background": color["secondary_color"]})
        for i in self.indicators:
            i.config({"fg": color["text_color"]})
            i.config({"background": color["secondary_color"]})
        for i in self.checkbox_indicators:
            i.config({"fg": color["text_color"]})
            i.config({"background": color["secondary_color"]})


## USEFUL FUNCTIONS -----------------------------------------------------------------------------------------------------------------------------------------------------------
    def clear(self):
        for i in self.controls:
            i["name"].grid_forget()
            i["entry"].grid_forget()
            i["entry"].delete(0,"end")
            i["unit"].grid_forget()
        for i in self.indicators:
            i.config(text="")
            #i.grid_forget()
        for i in self.checkbox_indicators:
            i.grid_forget()
        self.calc.grid_forget()
        self.thickness.grid_forget()
        self.transformed_coordinate_system.grid_forget()
    
    def change_to_recrangle(self):
        self.lbl.grid(row=0, column=0, columnspan=5)
        # size a
        self.controls[0]["name"].config(text="a")
        self.controls[0]["name"].grid(row=2,column=1, sticky='e', pady=self.pady_val)
        self.controls[0]["entry"].grid(row=2,column=2, pady=self.pady_val)
        self.controls[0]["unit"].grid(row=2,column=3, sticky='w', pady=self.pady_val)
        # size b
        self.controls[1]["name"].config(text="b")
        self.controls[1]["name"].grid(row=3,column=1, sticky='e', pady=self.pady_val)
        self.controls[1]["entry"].grid(row=3,column=2, pady=self.pady_val)
        self.controls[1]["unit"].grid(row=3,column=3, sticky='w', pady=self.pady_val)
        # transformed checkbox
        self.transformed_coordinate_system.grid(row=4, column=0, columnspan=4, pady=self.pady_val, padx=(5,0), sticky=tk.W)
        # transformed x
        self.controls[2]["name"].config(text="u")
        self.controls[2]["name"].grid(row=5,column=1, sticky='e', pady=self.pady_val)
        self.controls[2]["entry"].grid(row=5,column=2, pady=self.pady_val)
        self.controls[2]["unit"].grid(row=5,column=3, sticky='w', pady=self.pady_val)
        # transformed y
        self.controls[3]["name"].config(text="v")
        self.controls[3]["name"].grid(row=6,column=1, sticky='e', pady=self.pady_val)
        self.controls[3]["entry"].grid(row=6,column=2, pady=self.pady_val)
        self.controls[3]["unit"].grid(row=6,column=3, sticky='w', pady=self.pady_val)
        # transformed phi
        self.controls[4]["name"].config(text="φ")
        self.controls[4]["name"].grid(row=7,column=1, sticky='e', pady=self.pady_val)
        self.controls[4]["entry"].grid(row=7,column=2, pady=self.pady_val)
        self.controls[4]["unit"].grid(row=7,column=3, sticky='w', pady=self.pady_val)
        # thickness checkbox
        self.thickness.grid(row=8, column=0, columnspan=4, pady=self.pady_val, padx=(5,0), sticky=tk.W)
        # thickness t
        self.controls[5]["name"].config(text="t")
        self.controls[5]["name"].grid(row=9,column=1, sticky='e', pady=self.pady_val)
        self.controls[5]["entry"].grid(row=9,column=2, pady=self.pady_val)
        self.controls[5]["unit"].grid(row=9,column=3, sticky='w', pady=self.pady_val)
        # calculate button
        self.calc.grid(row=10,column=0, columnspan=5, pady=15)
    def change_to_circle(self):
        self.lbl.grid(row=0, column=0, columnspan=5)
        # diameter d
        self.controls[0]["name"].config(text="d")
        self.controls[0]["name"].grid(row=2,column=1, sticky='e', pady=self.pady_val)
        self.controls[0]["entry"].grid(row=2,column=2, pady=self.pady_val)
        self.controls[0]["unit"].grid(row=2,column=3, sticky='w', pady=self.pady_val)
        # transformed checkbox
        self.transformed_coordinate_system.grid(row=3, column=0, columnspan=4, pady=self.pady_val, padx=(5,0), sticky=tk.W)
        # transformed x
        self.controls[2]["name"].config(text="u")
        self.controls[2]["name"].grid(row=4,column=1, sticky='e', pady=self.pady_val)
        self.controls[2]["entry"].grid(row=4,column=2, pady=self.pady_val)
        self.controls[2]["unit"].grid(row=4,column=3, sticky='w', pady=self.pady_val)
        # transformed y
        self.controls[3]["name"].config(text="v")
        self.controls[3]["name"].grid(row=5,column=1, sticky='e', pady=self.pady_val)
        self.controls[3]["entry"].grid(row=5,column=2, pady=self.pady_val)
        self.controls[3]["unit"].grid(row=5,column=3, sticky='w', pady=self.pady_val)
        # transformed phi
        self.controls[4]["name"].config(text="φ")
        self.controls[4]["name"].grid(row=6,column=1, sticky='e', pady=self.pady_val)
        self.controls[4]["entry"].grid(row=6,column=2, pady=self.pady_val)
        self.controls[4]["unit"].grid(row=6,column=3, sticky='w', pady=self.pady_val)
        # thickness checkbox
        self.thickness.grid(row=7, column=0, columnspan=4, pady=self.pady_val, padx=(5,0), sticky=tk.W)
        # thickness t
        self.controls[5]["name"].config(text="t")
        self.controls[5]["name"].grid(row=8,column=1, sticky='e', pady=self.pady_val)
        self.controls[5]["entry"].grid(row=8,column=2, pady=self.pady_val)
        self.controls[5]["unit"].grid(row=8,column=3, sticky='w', pady=self.pady_val)
        # calculate button
        self.calc.grid(row=10,column=0, columnspan=5, pady=15)
    def change_to_ellipse(self):
        self.lbl.grid(row=0, column=0, columnspan=5)
        # size a
        self.controls[0]["name"].config(text="a")
        self.controls[0]["name"].grid(row=2,column=1, sticky='e', pady=self.pady_val)
        self.controls[0]["entry"].grid(row=2,column=2, pady=self.pady_val)
        self.controls[0]["unit"].grid(row=2,column=3, sticky='w', pady=self.pady_val)
        # size b
        self.controls[1]["name"].config(text="b")
        self.controls[1]["name"].grid(row=3,column=1, sticky='e', pady=self.pady_val)
        self.controls[1]["entry"].grid(row=3,column=2, pady=self.pady_val)
        self.controls[1]["unit"].grid(row=3,column=3, sticky='w', pady=self.pady_val)
        # transformed checkbox
        self.transformed_coordinate_system.grid(row=4, column=0, columnspan=4, pady=self.pady_val, padx=(5,0), sticky=tk.W)
        # transformed x
        self.controls[2]["name"].config(text="u")
        self.controls[2]["name"].grid(row=5,column=1, sticky='e', pady=self.pady_val)
        self.controls[2]["entry"].grid(row=5,column=2, pady=self.pady_val)
        self.controls[2]["unit"].grid(row=5,column=3, sticky='w', pady=self.pady_val)
        # transformed y
        self.controls[3]["name"].config(text="v")
        self.controls[3]["name"].grid(row=6,column=1, sticky='e', pady=self.pady_val)
        self.controls[3]["entry"].grid(row=6,column=2, pady=self.pady_val)
        self.controls[3]["unit"].grid(row=6,column=3, sticky='w', pady=self.pady_val)
        # transformed phi
        self.controls[4]["name"].config(text="φ")
        self.controls[4]["name"].grid(row=7,column=1, sticky='e', pady=self.pady_val)
        self.controls[4]["entry"].grid(row=7,column=2, pady=self.pady_val)
        self.controls[4]["unit"].grid(row=7,column=3, sticky='w', pady=self.pady_val)
        # thickness checkbox
        self.thickness.grid(row=8, column=0, columnspan=4, pady=self.pady_val, padx=(5,0), sticky=tk.W)
        # thickness t
        self.controls[5]["name"].config(text="t")
        self.controls[5]["name"].grid(row=9,column=1, sticky='e', pady=self.pady_val)
        self.controls[5]["entry"].grid(row=9,column=2, pady=self.pady_val)
        self.controls[5]["unit"].grid(row=9,column=3, sticky='w', pady=self.pady_val)
        # calculate button
        self.calc.grid(row=10,column=0, columnspan=5, pady=15)
    def change_to_isosceles_triangle(self):
        self.lbl.grid(row=0, column=0, columnspan=5)
        # size a
        self.controls[0]["name"].config(text="a")
        self.controls[0]["name"].grid(row=2,column=1, sticky='e', pady=self.pady_val)
        self.controls[0]["entry"].grid(row=2,column=2, pady=self.pady_val)
        self.controls[0]["unit"].grid(row=2,column=3, sticky='w', pady=self.pady_val)
        # size b
        self.controls[1]["name"].config(text="b")
        self.controls[1]["name"].grid(row=3,column=1, sticky='e', pady=self.pady_val)
        self.controls[1]["entry"].grid(row=3,column=2, pady=self.pady_val)
        self.controls[1]["unit"].grid(row=3,column=3, sticky='w', pady=self.pady_val)
        # transformed checkbox
        self.transformed_coordinate_system.grid(row=4, column=0, columnspan=4, pady=self.pady_val, padx=(5,0), sticky=tk.W)
        # transformed x
        self.controls[2]["name"].config(text="u")
        self.controls[2]["name"].grid(row=5,column=1, sticky='e', pady=self.pady_val)
        self.controls[2]["entry"].grid(row=5,column=2, pady=self.pady_val)
        self.controls[2]["unit"].grid(row=5,column=3, sticky='w', pady=self.pady_val)
        # transformed y
        self.controls[3]["name"].config(text="v")
        self.controls[3]["name"].grid(row=6,column=1, sticky='e', pady=self.pady_val)
        self.controls[3]["entry"].grid(row=6,column=2, pady=self.pady_val)
        self.controls[3]["unit"].grid(row=6,column=3, sticky='w', pady=self.pady_val)
        # transformed phi
        self.controls[4]["name"].config(text="φ")
        self.controls[4]["name"].grid(row=7,column=1, sticky='e', pady=self.pady_val)
        self.controls[4]["entry"].grid(row=7,column=2, pady=self.pady_val)
        self.controls[4]["unit"].grid(row=7,column=3, sticky='w', pady=self.pady_val)
        # thickness checkbox
        self.thickness.grid(row=8, column=0, columnspan=4, pady=self.pady_val, padx=(5,0), sticky=tk.W)
        # thickness t
        self.controls[5]["name"].config(text="t")
        self.controls[5]["name"].grid(row=9,column=1, sticky='e', pady=self.pady_val)
        self.controls[5]["entry"].grid(row=9,column=2, pady=self.pady_val)
        self.controls[5]["unit"].grid(row=9,column=3, sticky='w', pady=self.pady_val)
        # calculate button
        self.calc.grid(row=10,column=0, columnspan=6, pady=15)

    def change_to_right_triangle(self):
        self.lbl.grid(row=0, column=0, columnspan=5)
        # size a
        self.controls[0]["name"].config(text="a")
        self.controls[0]["name"].grid(row=2,column=1, sticky='e', pady=self.pady_val)
        self.controls[0]["entry"].grid(row=2,column=2, pady=self.pady_val)
        self.controls[0]["unit"].grid(row=2,column=3, sticky='w', pady=self.pady_val)
        # size b
        self.controls[1]["name"].config(text="b")
        self.controls[1]["name"].grid(row=3,column=1, sticky='e', pady=self.pady_val)
        self.controls[1]["entry"].grid(row=3,column=2, pady=self.pady_val)
        self.controls[1]["unit"].grid(row=3,column=3, sticky='w', pady=self.pady_val)
        # transformed checkbox
        self.transformed_coordinate_system.grid(row=4, column=0, columnspan=4, pady=self.pady_val, padx=(5,0), sticky=tk.W)
        # transformed x
        self.controls[2]["name"].config(text="u")
        self.controls[2]["name"].grid(row=5,column=1, sticky='e', pady=self.pady_val)
        self.controls[2]["entry"].grid(row=5,column=2, pady=self.pady_val)
        self.controls[2]["unit"].grid(row=5,column=3, sticky='w', pady=self.pady_val)
        # transformed y
        self.controls[3]["name"].config(text="v")
        self.controls[3]["name"].grid(row=6,column=1, sticky='e', pady=self.pady_val)
        self.controls[3]["entry"].grid(row=6,column=2, pady=self.pady_val)
        self.controls[3]["unit"].grid(row=6,column=3, sticky='w', pady=self.pady_val)
        # transformed phi
        self.controls[4]["name"].config(text="φ")
        self.controls[4]["name"].grid(row=7,column=1, sticky='e', pady=self.pady_val)
        self.controls[4]["entry"].grid(row=7,column=2, pady=self.pady_val)
        self.controls[4]["unit"].grid(row=7,column=3, sticky='w', pady=self.pady_val)
        # thickness checkbox
        self.thickness.grid(row=8, column=0, columnspan=4, pady=self.pady_val, padx=(5,0), sticky=tk.W)
        # thickness t
        self.controls[5]["name"].config(text="t")
        self.controls[5]["name"].grid(row=9,column=1, sticky='e', pady=self.pady_val)
        self.controls[5]["entry"].grid(row=9,column=2, pady=self.pady_val)
        self.controls[5]["unit"].grid(row=9,column=3, sticky='w', pady=self.pady_val)
        # calculate button
        self.calc.grid(row=10,column=0, columnspan=6, pady=15)
