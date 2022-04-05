import tkinter as tk

## Settings window -----------------------------------------------------------------------------------------------------------------------------------------------------------
def error_window(self):
    if self.window_open.get() == False:
        self.window_open.set(True)

        win_width = 322
        win_height = 220
        # Position the window in the center of the page.
        positionRight = int(self.winfo_screenwidth()/2 - win_width/2)
        positionDown = int(self.winfo_screenheight()/2 - win_height/2)

        self.error_window = tk.Toplevel(self, takefocus = True, bg=self.colors['main_color'])
        self.error_window.grab_set()
        self.error_window.bind('<Destroy>', func=lambda e: [self.window_open.set(False), self.error_window.grab_release()])
        self.error_window.geometry("+{}+{}".format(positionRight, positionDown))
        self.error_window.lift()
        self.error_window.wm_attributes('-topmost',True)
        self.error_window.title("Hiba a mentés közben")
        self.error_window.geometry(f"{win_width}x{win_height}")
        self.error_window.resizable(0, 0)
        self.error_window.tk.call('wm', 'iconphoto', self.error_window._w, tk.PhotoImage(file='logo_A.png'))

        self.error_window_canvas= tk.Canvas(self.error_window, bg=self.colors['main_color'], highlightthickness=0)
        self.error_window_canvas.pack(fill = tk.BOTH)

        def ok():
            self.error_window.destroy()
        
        self.errortext_img = tk.PhotoImage(file=f"{self.colors['path']}errors/errorwindow_text.png")
        self.errortext = self.error_window_canvas.create_image(0,0,anchor=tk.NW,image=self.errortext_img)

        self.ok_img = tk.PhotoImage(file=f"{self.colors['path']}settings/ok.png")
        self.ok_hover_img = tk.PhotoImage(file=f"{self.colors['path']}settings/ok_hover.png")
        self.ok = self.error_window_canvas.create_image(200,170,anchor=tk.NW,image=self.ok_img)

        self.error_window_canvas.tag_bind(self.ok, '<Enter>', lambda e:self.error_window_canvas.itemconfig(self.ok, image=self.ok_hover_img))
        self.error_window_canvas.tag_bind(self.ok, '<Leave>', lambda e:self.error_window_canvas.itemconfig(self.ok, image=self.ok_img))
        self.error_window_canvas.tag_bind(self.ok, '<Button-1>', lambda e:ok())
