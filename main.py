from tkinter import *
from tkinter import messagebox
from tkinter.colorchooser import askcolor
from brain import Image, ImageDraw, Predict, modelfit

class Paint(object):
    DEFAULT_PEN_SIZE = 5.0
    DEFAULT_COLOR = 'black'

    def __init__(self):
        self.root = Tk()

        self.image1 = Image.new("RGB", (500, 500), (255,255,255))
        self.draw = ImageDraw.Draw(self.image1)

        self.pen_button = Button(self.root, text='Pen', command=self.use_pen)
        self.pen_button.grid(row=0, column=0)

        self.brush_button = Button(self.root, text='Brush', command=self.use_brush)
        self.brush_button.grid(row=0, column=1)

        self.color_button = Button(self.root, text='Color', command=self.choose_color)
        self.color_button.grid(row=0, column=2)

        self.eraser_button = Button(self.root, text='Eraser', command=self.use_eraser)
        self.eraser_button.grid(row=0, column=3)

        self.choose_size_button = Scale(self.root, from_=15, to=30, orient=HORIZONTAL)
        self.choose_size_button.grid(row=0, column=4)
    

        self.predict_button = Button(self.root, text='Clean', command=self.clear)
        self.predict_button.grid(row=10, column=3)

        self.predict_button = Button(self.root, text='Predict', command=self.predict)
        self.predict_button.grid(row=10, column=2)

        self.save_button = Button(self.root, text='Save', command=self.saveimg)
        self.save_button.grid(row=10, column=1)

        self.c = Canvas(self.root, bg='white', width=500, height=500)
        self.c.grid(row=1, columnspan=5)
    

        self.setup()
        self.root.mainloop()
    def clear(self):
        self.draw.rectangle((0, 0, 500, 500), fill=(255,255,255, 0))
        self.c.delete("all")
    def saveimg(self):
        self.image1.save('just_drawed.jpg')

    def asktoclose(self, title, prompt):
        if messagebox.askquestion (title, prompt) == 'yes':
            return
        else:
            self.root.destroy()

    def predict(self):
        self.image1.save('just_drawed.jpg')
        pred, im = Predict('just_drawed.jpg')
        MsgBox = messagebox.askquestion ('Prediction',f"Is that a {pred}?")
        if MsgBox == 'yes':
            self.asktoclose('Prediction', 'Great! Want to continue?')
        else:
            num = int(input("Correct number: "))
            modelfit(im,  num)
            self.asktoclose('Prediction', 'Sorry. A brain never stops learning\n\nTry again?')

    def setup(self):
        self.old_x = None
        self.old_y = None
        self.line_width = self.choose_size_button.get()
        self.color = self.DEFAULT_COLOR
        self.eraser_on = False
        self.active_button = self.pen_button
        self.c.bind('<B1-Motion>', self.paint)
        self.c.bind('<ButtonRelease-1>', self.reset)

    def use_pen(self):
        self.activate_button(self.pen_button)

    def use_brush(self):
        self.activate_button(self.brush_button)

    def choose_color(self):
        self.eraser_on = False
        self.color = askcolor(color=self.color)[1]

    def use_eraser(self):
        self.activate_button(self.eraser_button, eraser_mode=True)

    def activate_button(self, some_button, eraser_mode=False):
        self.active_button.config(relief=RAISED)
        some_button.config(relief=SUNKEN)
        self.active_button = some_button
        self.eraser_on = eraser_mode

    def paint(self, event):
        self.line_width = self.choose_size_button.get() * 3
        paint_color = 'white' if self.eraser_on else self.color
        if self.old_x and self.old_y:
            self.c.create_line(self.old_x, self.old_y, event.x, event.y,
                               width=self.line_width, fill=paint_color,
                               capstyle=ROUND, smooth=TRUE, splinesteps=36)


            self.draw.line([self.old_x, self.old_y, event.x, event.y],
                    fill=paint_color, width=self.line_width)

        self.old_x = event.x
        self.old_y = event.y

    def reset(self, event):
        self.old_x, self.old_y = None, None


if __name__ == '__main__':
    Paint()
