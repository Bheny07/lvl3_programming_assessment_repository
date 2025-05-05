"""01_start_quiz_01 will load and render a visual representation of the
New Zealand map"""

# Import tkinter and PIL
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk


# Class to display NZ map
class AotearoaQuiz(object):
    def __init__(self, roots):
        self.root = roots
        self.root.title("Aotearoa Names Quiz")
        try:
            self.nz_image = Image.open("Design 2.jpg")
            self.nz_photo = ImageTk.PhotoImage(self.nz_image)

        except FileNotFoundError:
            messagebox.showerror("Error",
                                 "New Zealand map image not found!")
            self.root.destroy()
            return

        self.map_canvas = tk.Canvas(roots, width=self.nz_image.width,
                                    height=self.nz_image.height)
        self.map_canvas.create_image(0, 0, image=self.nz_photo,
                                     anchor=tk.NW)
        self.map_canvas.pack()


# Main Loop
if __name__ == '__main__':
    root = tk.Tk()
    quiz = AotearoaQuiz(root)
    root.mainloop()
