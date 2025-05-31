"""01_start_quiz_03 builds on 01_start_quiz_02 by adding a custom game logo to
enhance the quiz's visual appeal and theme."""

# Import tkinter for GUI and PIL for image handling
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk


# Class to display NZ map with clickable region buttons
class AotearoaQuiz(object):
    def __init__(self, roots):
        self.root = roots
        self.root.title("Aotearoa Names Quiz")

        # Try to load the NZ map image for display
        try:
            self.nz_image = Image.open("Design 2 Trans.png")
            self.nz_photo = ImageTk.PhotoImage(self.nz_image)

            image_width = self.nz_image.width
            image_height = self.nz_image.height
            extra_width = max(150, 350)
            window_width = max(image_width, extra_width + 100)
            window_height = image_height + 50

            # Set window size to fit image plus button area
            self.root.geometry(f"{window_width}x{window_height}")

        except FileNotFoundError:
            # Show error if map image missing and close app
            messagebox.showerror("Error",
                                 "New Zealand map image not found!")
            self.root.destroy()
            return

        # Create canvas and display map image on it
        self.map_canvas = tk.Canvas(roots, width=self.nz_image.width,
                                    height=self.nz_image.height)
        self.map_canvas.create_image(0, 0, image=self.nz_photo,
                                     anchor=tk.NW)
        self.map_canvas.pack()

        # Try to load logo image and place it bottom-right
        try:
            self.logo_image = Image.open(
                "HenyDice Logo Trans.png")
            self.logo_photo = ImageTk.PhotoImage(self.logo_image)
            self.logo_label = tk.Label(self.root, image=self.logo_photo)
            self.logo_label.place(relx=1.0, rely=1.0, x=-10,  anchor='se')

        except FileNotFoundError:
            # Warn if logo image not found (non-critical)
            messagebox.showwarning("Warning",
                                   "Logo image not found!")

        # Add region buttons on top of the map
        self.create_region_buttons_on_map()

    # Create buttons positioned on the map for each region
    def create_region_buttons_on_map(self):
        # Shared style for all region buttons
        button_configuration = {"width": 10, "height": 1, "font": ("Arial", 8)}

        # Place buttons using fixed x,y coordinates on the map
        self.create_map_button("Northland", 240, 50,
                               **button_configuration)
        self.create_map_button("Auckland", 265, 85,
                               **button_configuration)
        self.create_map_button("Waikato", 270, 120,
                               **button_configuration)
        self.create_map_button("Bay of Plenty", 400, 85,
                               **button_configuration)
        self.create_map_button("Gisborne", 450, 135,
                               **button_configuration)
        self.create_map_button("Hawke's Bay", 420, 180,
                               **button_configuration)
        self.create_map_button("Taranaki", 260, 155,
                               **button_configuration)
        self.create_map_button("Manawatu", 400, 210,
                               **button_configuration)
        self.create_map_button("Wellington", 380, 240,
                               **button_configuration)
        self.create_map_button("Marlborough", 220, 200,
                               **button_configuration)
        self.create_map_button("West Coast", 190, 250,
                               **button_configuration)
        self.create_map_button("Canterbury", 325, 280,
                               **button_configuration)
        self.create_map_button("Otago", 280, 350,
                               **button_configuration)
        self.create_map_button("Southland", 125, 310,
                               **button_configuration)

    # Create a button and place it on the map at given x,y coordinates
    def create_map_button(self, region_name, x, y, **kwargs):
        # Create button with given label and style
        button = tk.Button(self.root, text=region_name, **kwargs)
        # Adjust x to better center the button horizontally
        button.place(x=x - kwargs.get("width", 8) * 6, y=y, anchor=tk.CENTER)


# Run the application main loop when script is executed directly
if __name__ == '__main__':
    root = tk.Tk()
    quiz = AotearoaQuiz(root)
    root.mainloop()
