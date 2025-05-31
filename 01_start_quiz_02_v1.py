"""01_start_quiz_02 builds on 01_start_quiz_01 by adding interactive buttons
for each region over the map. 02_v1 improves tkinter messageboxes to better
display region names."""

# Import tkinter for GUI and PIL for image handling
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk


# Class to display NZ map in a quiz format
class AotearoaQuiz(object):
    def __init__(self, roots):
        self.root = roots
        self.root.title("Aotearoa Names Quiz")  # Set window title

        # Attempt to load the NZ map image
        try:
            self.nz_image = Image.open("Design 2.jpg")
            self.nz_photo = ImageTk.PhotoImage(self.nz_image)

            # Calculate and set window size based on image and extra space
            image_width = self.nz_image.width
            image_height = self.nz_image.height
            extra_width = max(150, 350)
            window_width = max(image_width, extra_width + 100)
            window_height = image_height + 50

            self.root.geometry(f"{window_width}x{window_height}")

        # Show error and close app if image not found
        except FileNotFoundError:
            messagebox.showerror("Error",
                                 "New Zealand map image not found!")
            self.root.destroy()
            return

        # Create a canvas and display the image on it
        self.map_canvas = tk.Canvas(roots, width=self.nz_image.width,
                                    height=self.nz_image.height)
        self.map_canvas.create_image(0, 0, image=self.nz_photo,
                                     anchor=tk.NW)
        self.map_canvas.pack()


# Start the GUI application
if __name__ == '__main__':
    root = tk.Tk()
    quiz = AotearoaQuiz(root)
    root.mainloop()
