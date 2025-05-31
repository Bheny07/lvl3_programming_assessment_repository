"""01_start_quiz_02 builds on 01_start_quiz_01 by adding interactive buttons
for each region, positioned over their areas on the map. 02_v2 focuses on
creating and placing these buttons."""

# Import tkinter for GUI and PIL for image handling
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk


# Class to display map and region buttons
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
            window_height = image_height + 50  # Add space for buttons

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

        # Add region buttons on the map
        self.create_region_buttons_on_map()

    # Function to place region buttons on specific coordinates
    def create_region_buttons_on_map(self):
        button_configuration = {"width": 10, "height": 1, "font": ("Arial", 8)}

        # Create a button for each region with approximate map coordinates
        self.create_map_button("Northland",
                               240, 50, **button_configuration)
        self.create_map_button("Auckland",
                               265, 85, **button_configuration)
        self.create_map_button("Waikato",
                               270, 120, **button_configuration)
        self.create_map_button("Bay of Plenty",
                               400, 85, **button_configuration)
        self.create_map_button("Gisborne",
                               450, 135, **button_configuration)
        self.create_map_button("Hawke's Bay",
                               420, 180, **button_configuration)
        self.create_map_button("Taranaki",
                               260, 155, **button_configuration)
        self.create_map_button("Manawatu",
                               400, 210, **button_configuration)
        self.create_map_button("Wellington",
                               380, 240, **button_configuration)
        self.create_map_button("Marlborough",
                               220, 200, **button_configuration)
        self.create_map_button("West Coast",
                               190, 250, **button_configuration)
        self.create_map_button("Canterbury",
                               325, 280, **button_configuration)
        self.create_map_button("Otago",
                               280, 350, **button_configuration)
        self.create_map_button("Southland",
                               125, 310, **button_configuration)

    # Function to create a button and place it at (x, y) on the window
    def create_map_button(self, region_name, x, y, **kwargs):
        button = tk.Button(self.root, text=region_name, **kwargs)
        button.place(x=x - kwargs.get("width", 8) * 6, y=y, anchor=tk.CENTER)


# Start the GUI application
if __name__ == '__main__':
    root = tk.Tk()
    quiz = AotearoaQuiz(root)
    root.mainloop()
