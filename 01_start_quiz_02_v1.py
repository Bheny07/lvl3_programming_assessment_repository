"""01_start_quiz_02 will add on from 01_start_quiz_01 and will display buttons
for each region on the map, creating an interactive button overlaid on it
corresponding area on the map. 02_v1 will start by expanding out the tkinter
messagebox to display region names more easily"""

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

            image_width = self.nz_image.width
            image_height = self.nz_image.height
            extra_width = max(150, 350)
            window_width = max(image_width, extra_width + 100)
            window_height = image_height + 50

            self.root.geometry(f"{window_width}x{window_height}")

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
