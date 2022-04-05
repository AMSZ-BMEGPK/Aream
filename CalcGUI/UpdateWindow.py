import tkinter as tk
import webbrowser

## Settings window -----------------------------------------------------------------------------------------------------------------------------------------------------------
def update_window(self):
    if self.window_open.get() == False:
        self.window_open.set(True)

        win_width = 322
        win_height = 220
        # Position the window in the center of the page.
        positionRight = int(self.winfo_screenwidth()/2 - win_width/2)
        positionDown = int(self.winfo_screenheight()/2 - win_height/2)

        self.update_window = tk.Toplevel(self, takefocus = True, bg=self.colors['main_color'])
        self.update_window.grab_set()
        self.update_window.bind('<Destroy>', func=lambda e: [self.window_open.set(False), self.update_window.grab_release()])
        self.update_window.geometry("+{}+{}".format(positionRight, positionDown))
        self.update_window.lift()
        self.update_window.wm_attributes('-topmost',True)
        self.update_window.title("Frissítés elérhető")
        self.update_window.geometry(f"{win_width}x{win_height}")
        self.update_window.resizable(0, 0)
        self.update_window.tk.call('wm', 'iconphoto', self.update_window._w, tk.PhotoImage(file='logo_A.png'))

        self.update_window_canvas= tk.Canvas(self.update_window, bg=self.colors['main_color'], highlightthickness=0)
        self.update_window_canvas.pack(fill = tk.BOTH)

        def update():
            webbrowser.open("https://www.mm.bme.hu/amsz/index.php/python-masodrendu-nyomatek-szamito-felulet/")
            self.update_window.destroy()
        
        self.updatetext_img = tk.PhotoImage(file=f"{self.colors['path']}errors/updatewindow_text.png")
        self.updatetext = self.update_window_canvas.create_image(0,0,anchor=tk.NW,image=self.updatetext_img)

        self.update_img = tk.PhotoImage(file=f"{self.colors['path']}settings/update.png")
        self.update_hover_img = tk.PhotoImage(file=f"{self.colors['path']}settings/update_hover.png")
        self.update = self.update_window_canvas.create_image(200,170,anchor=tk.NW,image=self.update_img)

        self.update_window_canvas.tag_bind(self.update, '<Enter>', lambda e:self.update_window_canvas.itemconfig(self.update, image=self.update_hover_img))
        self.update_window_canvas.tag_bind(self.update, '<Leave>', lambda e:self.update_window_canvas.itemconfig(self.update, image=self.update_img))
        self.update_window_canvas.tag_bind(self.update, '<Button-1>', lambda e:update())
