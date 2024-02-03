from tkinter import *
import tkinter as tk
import win32gui
from ttkthemes import ThemedTk

class App(ThemedTk):
    def __init__(self):
        ThemedTk.__init__(self, theme="arc")
        self.title('Handwritten Code Detector')
        self.configure(background='#2b2c3b')

        self.dark_mode = True  # Default to dark mode

        window = ThemedTk(theme="arc")
        window.title("Output")
        window.geometry("400x300")
        window.config(bg="grey")

        self.x = self.y = 0

        # Define colors for dark mode
        self.dark_mode_bg = '#2b2c3b'
        self.dark_mode_fg = 'white'

        # Define colors for light mode
        self.light_mode_bg = 'white'
        self.light_mode_fg = 'black'

        # Creating elements
        self.canvas = tk.Canvas(self, width=500, height=500, bg="grey", cursor="cross")
        self.classify_btn = tk.Button(self, text="Recognise", command=self.classify_handwriting, background=self.dark_mode_bg, foreground=self.dark_mode_fg)
        self.button_clear = tk.Button(self, text="Clear", command=self.clear_all, background=self.dark_mode_bg, foreground=self.dark_mode_fg)

        # Theme menu
        self.menu_bar = Menu(self)
        self.theme_menu = Menu(self.menu_bar, tearoff=0)
        self.theme_menu.add_command(label="Toggle Dark Mode", command=self.toggle_theme)
        self.menu_bar.add_cascade(label="Settings", menu=self.theme_menu)
        self.config(menu=self.menu_bar)

        # Grid structure
        self.canvas.grid(row=0, column=1, pady=2, sticky=W)
        self.classify_btn.grid(row=1, column=2, pady=2, padx=2)
        self.button_clear.grid(row=1, column=0, pady=2)

        # self.canvas.bind("<Motion>", self.start_pos)
        self.canvas.bind("<B1-Motion>", self.draw_lines)

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self.update_theme()

    def update_theme(self):
        if self.dark_mode:
            self.configure(background=self.dark_mode_bg)
            self.canvas.config(bg="grey")
            self.classify_btn.config(background=self.dark_mode_bg, foreground=self.dark_mode_fg)
            self.button_clear.config(background=self.dark_mode_bg, foreground=self.dark_mode_fg)
        else:
            self.configure(background=self.light_mode_bg)
            self.canvas.config(bg=self.light_mode_bg)
            self.classify_btn.config(background=self.light_mode_bg, foreground=self.light_mode_fg)
            self.button_clear.config(background=self.light_mode_bg, foreground=self.light_mode_fg)

    def clear_all(self):
        self.canvas.delete("all")

    def classify_handwriting(self):
        HWND = self.canvas.winfo_id()
        rect = win32gui.GetWindowRect(HWND)

        # Replace this line with the appropriate logic
        # self.label.configure(text=str(digit) + ', ' + str(int(acc * 100)) + '%')

    def draw_lines(self, event):
        self.x = event.x
        self.y = event.y
        r = 10
        self.canvas.create_oval(self.x - r, self.y - r, self.x + r, self.y + r, fill='black')

app = App()
app.mainloop()
