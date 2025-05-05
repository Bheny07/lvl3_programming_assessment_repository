"""01_start_quiz_01 will load and render a visual representation of the
New Zealand map"""

import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk


class AotearoaQuiz(object):
    def __init__(self, roots):
        # Store the main window object
        self.root = roots
        # Set the window title
        self.root.title("Aotearoa Names Quiz")
        try:
            # Open the image file
            self.nz_image = Image.open("Design 2.jpg")
            self.nz_photo = ImageTk.PhotoImage(self.nz_image)

        except FileNotFoundError:
            messagebox.showerror("Error",
                                 "New Zealand map image not found!")
            self.root.destroy()
            return

        # Create a canvas for the map
        self.map_canvas = tk.Canvas(roots, width=self.nz_image.width,
                                    height=self.nz_image.height)
        # Display the image on the canvas
        self.map_canvas.create_image(0, 0, image=self.nz_photo,
                                     anchor=tk.NW)
        # Make the canvas visible
        self.map_canvas.pack()


if __name__ == '__main__':
    # Create the main Tkinter window
    root = tk.Tk()
    quiz = AotearoaQuiz(root)
    root.mainloop()

