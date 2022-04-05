import tkinter as tk

## Settings window -----------------------------------------------------------------------------------------------------------------------------------------------------------
def settings_window(self):
    if self.window_open.get() == False:
        self.window_open.set(True)

        # Variables:
        unit_clicked = tk.BooleanVar(False)
        theme_clicked = tk.BooleanVar(False)
        other_clicked = tk.BooleanVar(False)

        self.temp_unit = self.unit
        self.temp_angle_unit = self.angle_unit
        self.temp_theme = self.theme

        win_width = 322
        win_height = 220
        # Position the window in the center of the page.
        positionRight = int(self.winfo_screenwidth()/2 - win_width/2)
        positionDown = int(self.winfo_screenheight()/2 - win_height/2)

        self.settings_window = tk.Toplevel(self, takefocus = True, bg=self.colors['main_color'])
        self.settings_window.grab_set()
        self.settings_window.bind('<Destroy>', func=lambda e: [self.window_open.set(False), self.settings_window.grab_release()])
        self.settings_window.geometry("+{}+{}".format(positionRight, positionDown))
        self.settings_window.lift()
        self.settings_window.wm_attributes('-topmost',True)
        self.settings_window.title("Beállítások")
        self.settings_window.geometry(f"{win_width}x{win_height}")
        self.settings_window.resizable(0, 0)
        self.settings_window.tk.call('wm', 'iconphoto', self.settings_window._w, tk.PhotoImage(file='logo_A.png'))

        # setting window menubar
        self.settings_menu = tk.Canvas(self.settings_window, bg=self.colors['secondary_color'], highlightthickness=0, height=26)
        self.settings_menu.pack(fill = tk.X)

        self.settings_menu_options = tk.Canvas(self.settings_window, bg=self.colors['main_color'], highlightthickness=0)
        self.settings_menu_options.pack(fill = tk.BOTH)

        # menubar objects
        self.unit_button_img = tk.PhotoImage(file=f"{self.colors['path']}settings/unit.png")
        self.unit_button_hover_img = tk.PhotoImage(file=f"{self.colors['path']}settings/unit_hover.png")
        self.unit_button_clicked_img = tk.PhotoImage(file=f"{self.colors['path']}settings/unit_clicked.png")
        self.unit_button = self.settings_menu.create_image(0,0,anchor=tk.NW,image=self.unit_button_img)
        self.settings_menu.tag_bind(self.unit_button, '<Button-1>', lambda e:unit_button_click())
        self.settings_menu.tag_bind(self.unit_button, '<Enter>', lambda e:hover_unit())
        self.settings_menu.tag_bind(self.unit_button, '<Leave>', lambda e:release_unit())

        self.mm_img = tk.PhotoImage(file=f"{self.colors['path']}settings/mm.png")
        self.cm_img = tk.PhotoImage(file=f"{self.colors['path']}settings/cm.png")
        self.m_img = tk.PhotoImage(file=f"{self.colors['path']}settings/m.png")
        self.deg_img = tk.PhotoImage(file=f"{self.colors['path']}settings/deg.png")
        self.rad_img = tk.PhotoImage(file=f"{self.colors['path']}settings/rad.png")
        self.mm_hover_img = tk.PhotoImage(file=f"{self.colors['path']}settings/mm_hover.png")
        self.cm_hover_img = tk.PhotoImage(file=f"{self.colors['path']}settings/cm_hover.png")
        self.m_hover_img = tk.PhotoImage(file=f"{self.colors['path']}settings/m_hover.png")
        self.deg_hover_img = tk.PhotoImage(file=f"{self.colors['path']}settings/deg_hover.png")
        self.rad_hover_img = tk.PhotoImage(file=f"{self.colors['path']}settings/rad_hover.png")
        self.mm_clicked_img = tk.PhotoImage(file=f"{self.colors['path']}settings/mm_clicked.png")
        self.cm_clicked_img = tk.PhotoImage(file=f"{self.colors['path']}settings/cm_clicked.png")
        self.m_clicked_img = tk.PhotoImage(file=f"{self.colors['path']}settings/m_clicked.png")
        self.deg_clicked_img = tk.PhotoImage(file=f"{self.colors['path']}settings/deg_clicked.png")
        self.rad_clicked_img = tk.PhotoImage(file=f"{self.colors['path']}settings/rad_clicked.png")

        self.theme_button_img = tk.PhotoImage(file=f"{self.colors['path']}settings/theme.png")
        self.theme_button_hover_img = tk.PhotoImage(file=f"{self.colors['path']}settings/theme_hover.png")
        self.theme_button_clicked_img = tk.PhotoImage(file=f"{self.colors['path']}settings/theme_clicked.png")
        self.theme_button = self.settings_menu.create_image(116,0,anchor=tk.NW,image=self.theme_button_img)
        self.settings_menu.tag_bind(self.theme_button, '<Button-1>', lambda e:theme_button_click())
        self.settings_menu.tag_bind(self.theme_button, '<Enter>', lambda e:hover_theme())
        self.settings_menu.tag_bind(self.theme_button, '<Leave>', lambda e:release_theme())

        self.light_img = tk.PhotoImage(file=f"{self.colors['path']}settings/light.png")
        self.dark_img = tk.PhotoImage(file=f"{self.colors['path']}settings/dark.png")
        self.light_hover_img = tk.PhotoImage(file=f"{self.colors['path']}settings/light_hover.png")
        self.dark_hover_img = tk.PhotoImage(file=f"{self.colors['path']}settings/dark_hover.png")
        self.light_clicked_img = tk.PhotoImage(file=f"{self.colors['path']}settings/light_clicked.png")
        self.dark_clicked_img = tk.PhotoImage(file=f"{self.colors['path']}settings/dark_clicked.png")

        self.other_button_img = tk.PhotoImage(file=f"{self.colors['path']}settings/other.png")
        self.other_button_hover_img = tk.PhotoImage(file=f"{self.colors['path']}settings/other_hover.png")
        self.other_button_clicked_img = tk.PhotoImage(file=f"{self.colors['path']}settings/other_clicked.png")
        self.other_button = self.settings_menu.create_image(172,0,anchor=tk.NW,image=self.other_button_img)
        self.settings_menu.tag_bind(self.other_button, '<Button-1>', lambda e:other_button_click())
        self.settings_menu.tag_bind(self.other_button, '<Enter>', lambda e:hover_other())
        self.settings_menu.tag_bind(self.other_button, '<Leave>', lambda e:release_other())

        self.logo_enabled_check = tk.Checkbutton(
        self.settings_menu_options, text = "AMSZ logo lejátszása induláskor",
        variable = self.play_logo, onvalue=True, offvalue=False, 
        bg = self["background"], fg=self.colors['text_color'], selectcolor=self["background"],
        command = lambda :enable_logo())
        
        #sb stuff --------------------------------------
        self.orig_axis_dissapier_check = tk.Checkbutton(
        self.settings_menu_options, text = "Segéd tengelyek (szürke) eltüntetése számolásnál",
        variable = self.orig_axis_dissapier_bool, onvalue=True, offvalue=False, 
        bg = self["background"], fg=self.colors['text_color'], selectcolor=self["background"],
        command = lambda :turn_on_fixed_axis_dissapier())
        
        self.show_orig_axis_check = tk.Checkbutton(
        self.settings_menu_options, text = "Segéd tengelyek (szürke) megjelenítése",
        variable = self.show_orig_axis_bool, onvalue=True, offvalue=False, 
        bg = self["background"], fg=self.colors['text_color'], selectcolor=self["background"],
        command = lambda :turn_on_show_fixed_axis())

        self.sb_ha_vis_check = tk.Checkbutton(
        self.settings_menu_options, text = "Főtengelyek megjelenítése az ábrán",
        variable = self.sb_ha_vis_bool, onvalue=True, offvalue=False, 
        bg = self["background"], fg=self.colors['text_color'], selectcolor=self["background"],
        command = lambda :turn_on_sb_ha_vis())

        self.calc_for_orig_axis_check = tk.Checkbutton(
        self.settings_menu_options, text = "Számolás a segéd koordináta-rendszerre vonatkozva",
        variable = self.calc_for_orig_axis_bool, onvalue=True, offvalue=False, 
        bg = self["background"], fg=self.colors['text_color'], selectcolor=self["background"],
        command = lambda :turn_on_calc_for_orig_axis())
        #--------------------------
        self.ok_img = tk.PhotoImage(file=f"{self.colors['path']}settings/ok.png")
        self.ok_hover_img = tk.PhotoImage(file=f"{self.colors['path']}settings/ok_hover.png")
        
        # Function for interractions in settings window --------------------------------------------------------------------------------------------------------------
        # Hover menubar buttons----------------------------------------------------------------------
        def release_unit():
            if unit_clicked.get() == True:
                self.settings_menu.itemconfig(self.unit_button, image=self.unit_button_clicked_img)
            else:
                self.settings_menu.itemconfig(self.unit_button, image=self.unit_button_img)
        def release_theme():
            if theme_clicked.get() == True:
                self.settings_menu.itemconfig(self.theme_button, image=self.theme_button_clicked_img)
            else:
                self.settings_menu.itemconfig(self.theme_button, image=self.theme_button_img)
        def release_other():
            if other_clicked.get() == True:
                self.settings_menu.itemconfig(self.other_button, image=self.other_button_clicked_img)
            else:
                self.settings_menu.itemconfig(self.other_button, image=self.other_button_img)
        def hover_unit():
            if unit_clicked.get() == True:
                self.settings_menu.itemconfig(self.unit_button, image=self.unit_button_clicked_img)
            else:
                self.settings_menu.itemconfig(self.unit_button, image=self.unit_button_hover_img)
        def hover_theme():
            if theme_clicked.get() == True:
                self.settings_menu.itemconfig(self.theme_button, image=self.theme_button_clicked_img)
            else:
                self.settings_menu.itemconfig(self.theme_button, image=self.theme_button_hover_img)
        def hover_other():
            if other_clicked.get() == True:
                self.settings_menu.itemconfig(self.other_button, image=self.other_button_clicked_img)
            else:
                self.settings_menu.itemconfig(self.other_button, image=self.other_button_hover_img)
        # Enable/disable logo ------------------------------------------------------------------------
        def enable_logo():
            if self.play_logo.get() == True:
                self.logo_enabled = 'True'
            else:
                self.logo_enabled = 'False'
        
        # Side menu settings ----------------------------
        def turn_on_fixed_axis_dissapier():
            self.orig_axis_dissapier = self.orig_axis_dissapier_bool.get()
        def turn_on_show_fixed_axis():
            self.show_orig_axis = self.show_orig_axis_bool.get()
            try:
                if not self.show_orig_axis: self.sb.itemconfigure("orig_axes",state="hidden")
            except:
                pass
        def turn_on_sb_ha_vis():
            self.sb_ha_vis = self.sb_ha_vis_bool.get()
            print(self.sb_ha_vis)
        def turn_on_calc_for_orig_axis():
            self.calc_for_orig_axis = self.calc_for_orig_axis_bool.get()
        
        # Unit hover ---------------------------------------------------------------------------------
        def mm_hover():
            if self.temp_unit == 'mm':
                self.settings_menu_options.itemconfig(self.mm, image=self.mm_clicked_img)
            else:
                self.settings_menu_options.itemconfig(self.mm, image=self.mm_hover_img)
        def cm_hover():
            if self.temp_unit == 'cm':
                self.settings_menu_options.itemconfig(self.cm, image=self.cm_clicked_img)
            else:
                self.settings_menu_options.itemconfig(self.cm, image=self.cm_hover_img)
        def m_hover():
            if self.temp_unit == 'm':
                self.settings_menu_options.itemconfig(self.m, image=self.m_clicked_img)
            else:
                self.settings_menu_options.itemconfig(self.m, image=self.m_hover_img)
        def deg_hover():
            if self.temp_angle_unit == '°':
                self.settings_menu_options.itemconfig(self.deg, image=self.deg_clicked_img)
            else:
                self.settings_menu_options.itemconfig(self.deg, image=self.deg_hover_img)
        def rad_hover():
            if self.temp_angle_unit == 'rad':
                self.settings_menu_options.itemconfig(self.rad, image=self.rad_clicked_img)
            else:
                self.settings_menu_options.itemconfig(self.rad, image=self.rad_hover_img)
        def mm_release():
            if self.temp_unit == 'mm':
                self.settings_menu_options.itemconfig(self.mm, image=self.mm_clicked_img)
            else:
                self.settings_menu_options.itemconfig(self.mm, image=self.mm_img)
        def cm_release():
            if self.temp_unit == 'cm':
                self.settings_menu_options.itemconfig(self.cm, image=self.cm_clicked_img)
            else:
                self.settings_menu_options.itemconfig(self.cm, image=self.cm_img)
        def m_release():
            if self.temp_unit == 'm':
                self.settings_menu_options.itemconfig(self.m, image=self.m_clicked_img)
            else:
                self.settings_menu_options.itemconfig(self.m, image=self.m_img)
        def deg_release():
            if self.temp_angle_unit == '°':
                self.settings_menu_options.itemconfig(self.deg, image=self.deg_clicked_img)
            else:
                self.settings_menu_options.itemconfig(self.deg, image=self.deg_img)
        def rad_release():
            if self.temp_angle_unit == 'rad':
                self.settings_menu_options.itemconfig(self.rad, image=self.rad_clicked_img)
            else:
                self.settings_menu_options.itemconfig(self.rad, image=self.rad_img)
        # Unit change --------------------------------------------------------------------------------
        def mm():
            if self.temp_unit != 'mm':
                self.temp_unit = 'mm'
                self.settings_menu_options.itemconfig(self.mm, image=self.mm_clicked_img)
                self.settings_menu_options.itemconfig(self.cm, image=self.cm_img)
                self.settings_menu_options.itemconfig(self.m, image=self.m_img)

        def cm():
            if self.temp_unit != 'cm':
                self.temp_unit = 'cm'
                self.settings_menu_options.itemconfig(self.mm, image=self.mm_img)
                self.settings_menu_options.itemconfig(self.cm, image=self.cm_clicked_img)
                self.settings_menu_options.itemconfig(self.m, image=self.m_img)
        def m():
            if self.temp_unit != 'm':
                self.temp_unit = 'm'
                self.settings_menu_options.itemconfig(self.mm, image=self.mm_img)
                self.settings_menu_options.itemconfig(self.cm, image=self.cm_img)
                self.settings_menu_options.itemconfig(self.m, image=self.m_clicked_img)
        def deg():
            if self.temp_angle_unit != '°':
                self.temp_angle_unit = '°'
                self.settings_menu_options.itemconfig(self.deg, image=self.deg_clicked_img)
                self.settings_menu_options.itemconfig(self.rad, image=self.rad_img)
        def rad():
            if self.temp_angle_unit != 'rad':
                self.temp_angle_unit = 'rad'
                self.settings_menu_options.itemconfig(self.deg, image=self.deg_img)
                self.settings_menu_options.itemconfig(self.rad, image=self.rad_clicked_img)
        # Theme change -------------------------------------------------------------------------------
        def light():
            if self.temp_theme != 'light':
                self.temp_theme = 'light'
                self.settings_menu_options.itemconfig(self.light, image=self.light_clicked_img)
                self.settings_menu_options.itemconfig(self.dark, image=self.dark_img)
        def dark():
            if self.temp_theme != 'dark':
                self.temp_theme = 'dark'
                self.settings_menu_options.itemconfig(self.light, image=self.light_img)
                self.settings_menu_options.itemconfig(self.dark, image=self.dark_clicked_img)
        # Hover theme buttons----------------------------------------------------------------------
        def light_release():
            if self.temp_theme == 'light':
                self.settings_menu_options.itemconfig(self.light, image=self.light_clicked_img)
            else:
                self.settings_menu_options.itemconfig(self.light, image=self.light_img)
        def dark_release():
            if self.temp_theme == 'dark':
                self.settings_menu_options.itemconfig(self.dark, image=self.dark_clicked_img)
            else:
                self.settings_menu_options.itemconfig(self.dark, image=self.dark_img)
        def light_hover():
            if self.temp_theme == 'light':
                self.settings_menu_options.itemconfig(self.light, image=self.light_clicked_img)
            else:
                self.settings_menu_options.itemconfig(self.light, image=self.light_hover_img)
        def dark_hover():
            if self.temp_theme == 'dark':
                self.settings_menu_options.itemconfig(self.dark, image=self.dark_clicked_img)
            else:
                self.settings_menu_options.itemconfig(self.dark, image=self.dark_hover_img)
        # ok button ----------------------------------------------------------------------------------
        def ok():
            self.unit_change('length', self.temp_unit)
            self.unit_change('degree', self.temp_angle_unit)
            self.settings_window.destroy()
            self.theme_change(self.temp_theme)
        # munobar button click ------------------------------------------------------------------------
        def unit_button_click():
            if unit_clicked.get() == False:
                unit_clicked.set(True)
                self.settings_menu.itemconfig(self.unit_button, image=self.unit_button_clicked_img)
                if theme_clicked.get() == True or other_clicked.get() == True:
                    self.settings_menu.itemconfig(self.other_button, image=self.other_button_img)
                    self.settings_menu.itemconfig(self.theme_button, image=self.theme_button_img)
                    try:
                        self.logo_enabled_check.place_forget()
                        self.orig_axis_dissapier_check.place_forget()
                        self.show_orig_axis_check.place_forget()
                        self.sb_ha_vis_check.place_forget()
                        self.calc_for_orig_axis_check.place_forget()
                        self.settings_menu_options.delete('all')
                    except:
                        self.settings_menu_options.delete('all')
                    theme_clicked.set(False)
                    other_clicked.set(False)
                # load button images
                self.mm = self.settings_menu_options.create_image(20,20,anchor=tk.NW,image=self.mm_img)
                self.cm = self.settings_menu_options.create_image(20,50,anchor=tk.NW,image=self.cm_img)
                self.m = self.settings_menu_options.create_image(20,80,anchor=tk.NW,image=self.m_img)
                # bind on hover
                self.settings_menu_options.tag_bind(self.mm, '<Enter>', lambda e:mm_hover())
                self.settings_menu_options.tag_bind(self.mm, '<Leave>', lambda e:mm_release())
                self.settings_menu_options.tag_bind(self.cm, '<Enter>', lambda e:cm_hover())
                self.settings_menu_options.tag_bind(self.cm, '<Leave>', lambda e:cm_release())
                self.settings_menu_options.tag_bind(self.m, '<Enter>', lambda e:m_hover())
                self.settings_menu_options.tag_bind(self.m, '<Leave>', lambda e:m_release())
                # # color selected buttton
                if self.temp_unit == 'mm':
                    self.settings_menu_options.itemconfig(self.mm, image=self.mm_clicked_img)
                elif self.temp_unit == 'cm':
                    self.settings_menu_options.itemconfig(self.cm, image=self.cm_clicked_img)
                else:
                    self.settings_menu_options.itemconfig(self.m, image=self.m_clicked_img)
                # load angle buttons
                self.deg = self.settings_menu_options.create_image(171,20,anchor=tk.NW,image=self.deg_img)
                self.rad = self.settings_menu_options.create_image(171,50,anchor=tk.NW,image=self.rad_img)
                # bind on hover
                self.settings_menu_options.tag_bind(self.deg, '<Enter>', lambda e:deg_hover())
                self.settings_menu_options.tag_bind(self.deg, '<Leave>', lambda e:deg_release())
                self.settings_menu_options.tag_bind(self.rad, '<Enter>', lambda e:rad_hover())
                self.settings_menu_options.tag_bind(self.rad, '<Leave>', lambda e:rad_release())
                # color selected button
                if self.temp_angle_unit == "°":
                    self.settings_menu_options.itemconfig(self.deg, image=self.deg_clicked_img)
                else:
                    self.settings_menu_options.itemconfig(self.rad, image=self.rad_clicked_img)
                self.ok = self.settings_menu_options.create_image(200,150,anchor=tk.NW,image=self.ok_img)
                # bind ok on hover
                self.settings_menu_options.tag_bind(self.ok, '<Enter>', lambda e:self.settings_menu_options.itemconfig(self.ok, image=self.ok_hover_img))
                self.settings_menu_options.tag_bind(self.ok, '<Leave>', lambda e:self.settings_menu_options.itemconfig(self.ok, image=self.ok_img))
                # bind clicking
                self.settings_menu_options.tag_bind(self.mm, '<Button-1>', lambda e:mm())
                self.settings_menu_options.tag_bind(self.cm, '<Button-1>', lambda e:cm())
                self.settings_menu_options.tag_bind(self.m, '<Button-1>', lambda e:m())
                self.settings_menu_options.tag_bind(self.deg, '<Button-1>', lambda e:deg())
                self.settings_menu_options.tag_bind(self.rad, '<Button-1>', lambda e:rad())
                self.settings_menu_options.tag_bind(self.ok, '<Button-1>', lambda e:ok())

        def theme_button_click():
            if theme_clicked.get() == False:
                theme_clicked.set(True)
                self.settings_menu.itemconfig(self.theme_button, image=self.theme_button_clicked_img)
                if unit_clicked.get() == True or other_clicked.get() == True:
                    self.settings_menu.itemconfig(self.other_button, image=self.other_button_img)
                    self.settings_menu.itemconfig(self.unit_button, image=self.unit_button_img)
                    try:
                        self.logo_enabled_check.place_forget()
                        self.orig_axis_dissapier_check.place_forget()
                        self.show_orig_axis_check.place_forget()
                        self.calc_for_orig_axis_check.place_forget()
                        self.sb_ha_vis_check.place_forget()
                        self.settings_menu_options.delete('all')
                    except:
                        self.settings_menu_options.delete('all')
                    unit_clicked.set(False)
                    other_clicked.set(False)
                self.light = self.settings_menu_options.create_image(20,20,anchor=tk.NW,image=self.light_img)
                self.dark = self.settings_menu_options.create_image(171,20,anchor=tk.NW,image=self.dark_img)
                # bind on hover
                self.settings_menu_options.tag_bind(self.dark, '<Enter>', lambda e:dark_hover())
                self.settings_menu_options.tag_bind(self.dark, '<Leave>', lambda e:dark_release())
                self.settings_menu_options.tag_bind(self.light, '<Enter>', lambda e:light_hover())
                self.settings_menu_options.tag_bind(self.light, '<Leave>', lambda e:light_release())
                # color selectes button
                if self.temp_theme == "dark":
                    self.settings_menu_options.itemconfig(self.dark, image=self.dark_clicked_img)
                else:
                    self.settings_menu_options.itemconfig(self.light, image=self.light_clicked_img)
                self.ok = self.settings_menu_options.create_image(200,150,anchor=tk.NW,image=self.ok_img)
                # bind ok on hover
                self.settings_menu_options.tag_bind(self.ok, '<Enter>', lambda e:self.settings_menu_options.itemconfig(self.ok, image=self.ok_hover_img))
                self.settings_menu_options.tag_bind(self.ok, '<Leave>', lambda e:self.settings_menu_options.itemconfig(self.ok, image=self.ok_img))

                self.settings_menu_options.tag_bind(self.light, '<Button-1>', lambda e:light())
                self.settings_menu_options.tag_bind(self.dark, '<Button-1>', lambda e:dark())
                self.settings_menu_options.tag_bind(self.ok, '<Button-1>', lambda e:ok())

        def other_button_click():
            if other_clicked.get() == False:
                other_clicked.set(True)
                self.settings_menu.itemconfig(self.other_button, image=self.other_button_clicked_img)
                if unit_clicked.get() == True or theme_clicked.get() == True:
                    self.settings_menu.itemconfig(self.unit_button, image=self.unit_button_img)
                    self.settings_menu.itemconfig(self.theme_button, image=self.theme_button_img)
                    self.settings_menu_options.delete('all')
                    unit_clicked.set(False)
                    theme_clicked.set(False)
                self.logo_enabled_check.place(bordermode=tk.OUTSIDE, x=20,y=20, anchor=tk.NW)
                self.orig_axis_dissapier_check.place(bordermode=tk.OUTSIDE, x=20,y=40, anchor=tk.NW)
                self.show_orig_axis_check.place(bordermode=tk.OUTSIDE, x=20,y=60, anchor=tk.NW)
                self.sb_ha_vis_check.place(bordermode=tk.OUTSIDE, x=20,y=80, anchor=tk.NW)
                self.calc_for_orig_axis_check.place(bordermode=tk.OUTSIDE, x=20,y=100, anchor=tk.NW)
                self.ok = self.settings_menu_options.create_image(200,150,anchor=tk.NW,image=self.ok_img)
                # bind ok on hover
                self.settings_menu_options.tag_bind(self.ok, '<Enter>', lambda e:self.settings_menu_options.itemconfig(self.ok, image=self.ok_hover_img))
                self.settings_menu_options.tag_bind(self.ok, '<Leave>', lambda e:self.settings_menu_options.itemconfig(self.ok, image=self.ok_img))

                self.settings_menu_options.tag_bind(self.ok, '<Button-1>', lambda e:ok())
