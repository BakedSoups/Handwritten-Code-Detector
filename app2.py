from keras.models import load_model
from tkinter import *
import tkinter as tk
import win32gui
from PIL import ImageGrab, Image, ImageOps
import numpy as np
import cv2
import os  
currentdir = os.getcwd()

model = load_model(f'{currentdir}\\models\\mnst\\mnist30.h5')

def predict_digit(img):
    #resize image to 28x28 pixels
    img = img.resize((28,28))
    img.save('trulyscaled.png')
    #convert rgb to grayscale
    img = img.convert('L')
    img = np.array(img)
    #reshaping to support our model input and normalizing
    img = img.reshape(1,28,28,1)
    img = img/255.0
    #predicting the class
    res = model.predict([img])[0]
    return np.argmax(res), max(res)

class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        self.x = self.y = 0

        # Creating elements
        self.canvas = tk.Canvas(self, width=500, height=500, bg = "white", cursor="cross")
        self.label = tk.Label(self, text="Thinking..", font=("Helvetica", 48))
        self.classify_btn = tk.Button(self, text = "Recognise", command = self.classify_handwriting) 
        self.button_clear = tk.Button(self, text = "Clear", command = self.clear_all)
        self.button_rundir = tk.Button(self, text = "Run Dir", command = self.run_dir)

        # Grid structure
        self.canvas.grid(row=0, column=0, pady=2, sticky=W, )
        self.label.grid(row=0, column=1,pady=2, padx=2)
        self.classify_btn.grid(row=1, column=1, pady=2, padx=2)
        self.button_clear.grid(row=1, column=0, pady=2)
        self.button_rundir.grid(row=1, column=2, pady=2)

        
        #self.canvas.bind("<Motion>", self.start_pos)
        self.canvas.bind("<B1-Motion>", self.draw_lines)

    def clear_all(self):
        self.canvas.delete("all")
        
    def run_dir(self): 
        index = 1
        for i in range(5): 
            im = Image.open(f'{currentdir}/Samples/{index}.png')
            im_cv = cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR)
            im_cv_inverted = cv2.bitwise_not(im_cv)
        
            im_inverted = Image.fromarray(cv2.cvtColor(im_cv_inverted, cv2.COLOR_BGR2RGB))
            im_inverted.save(f'scaled{index}.png')

            index += 1 
            digit, acc = predict_digit(im_inverted) 
            print(f"number is {index} and prediction is {digit, acc}")

    def classify_handwriting(self):
        HWND = self.canvas.winfo_id() # get the handle of the canvas
        rect = win32gui.GetWindowRect(HWND) # get the coordinate of the canvas
        im = ImageGrab.grab(rect)
        # downloand scaled image to dir
        #invert image
        im_cv = cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR)
        
        # Invert the colors using OpenCV
        im_cv_inverted = cv2.bitwise_not(im_cv)
        
        # Convert the inverted image back to PIL format (RGB)
        im_inverted = Image.fromarray(cv2.cvtColor(im_cv_inverted, cv2.COLOR_BGR2RGB))
        im_inverted.save('scaled.png')
        

        digit, acc = predict_digit(im_inverted)
        self.label.configure(text= str(digit)+', '+ str(int(acc*100))+'%')

    def draw_lines(self, event):
        self.x = event.x
        self.y = event.y
        r=2
        self.canvas.create_oval(self.x-r, self.y-r, self.x + r, self.y + r, fill='black')

app = App()
mainloop()