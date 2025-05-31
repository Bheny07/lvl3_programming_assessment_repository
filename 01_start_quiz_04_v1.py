"""01_start_quiz_04 builds on 01_start_quiz_03 by adding a score counter.
04_v1 introduces a frame and labels to display the number of correct and
incorrect answers."""

# Import tkinter for GUI and PIL for image handling
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk


# Class to display NZ map and clickable region buttons
class AotearoaQuiz(object):
    def __init__(self, roots):
        self.root = roots
        self.root.title("Aotearoa Names Quiz")

        self.correct_answers = 0  # Track number of correct answers
        self.incorrect_answers = 0  # Track number of incorrect answers

        # Create a top frame for showing the score counters
        self.score_frame = tk.Frame(self.root)
        self.score_frame.pack(fill=tk.X)

        # Show number of correct answers
        self.correct_label = tk.Label(self.score_frame,
                                      text=f"Correct: {self.correct_answers}",
                                      font=("Arial", 10))
        self.correct_label.pack(side=tk.LEFT, padx=10, pady=5)

        # A separator between correct and incorrect labels
        separator = tk.Label(self.score_frame, text=" | ", font=("Arial", 10))
        separator.pack(side=tk.LEFT)

        # Show number of incorrect answers
        self.incorrect_label = tk.Label(
            self.score_frame, text=f"Incorrect: {self.incorrect_answers}",
            font=("Arial", 10))
        self.incorrect_label.pack(side=tk.LEFT)

        # Try to load the NZ map image
        try:
            self.nz_image = Image.open("Design 2 Trans.png")
            self.nz_photo = ImageTk.PhotoImage(self.nz_image)

            # Set window size based on image dimensions
            image_width = self.nz_image.width
            image_height = self.nz_image.height
            extra_width = max(150, 350)
            window_width = max(image_width, extra_width + 100)
            window_height = image_height + 50

            self.root.geometry(f"{window_width}x{window_height}")

        except FileNotFoundError:
            # Show error if image is missing and close the app
            messagebox.showerror("Error",
                                 "New Zealand map image not found!")
            self.root.destroy()
            return

        # Create canvas and place NZ map on it
        self.map_canvas = tk.Canvas(roots, width=self.nz_image.width,
                                    height=self.nz_image.height)
        self.map_canvas.create_image(0, 0, image=self.nz_photo,
                                     anchor=tk.NW)
        self.map_canvas.pack()

        # Try to load and place logo image at bottom-right
        try:
            self.logo_image = Image.open(
                "HenyDice Logo Trans.png")
            self.logo_photo = ImageTk.PhotoImage(self.logo_image)
            self.logo_label = tk.Label(self.root, image=self.logo_photo)
            self.logo_label.place(relx=1.0, rely=1.0, x=-10,  anchor='se')

        except FileNotFoundError:
            # Show warning if logo image is not found
            messagebox.showwarning("Warning",
                                   "Logo image not found!")

        # Call method to add region buttons on the map
        self.create_region_buttons_on_map()

    # Create buttons positioned on the map for each region
    def create_region_buttons_on_map(self):
        button_configuration = {"width": 10, "height": 1, "font": ("Arial", 8)}

        # Manually place region buttons using approximate coordinates
        self.create_map_button("Northland", 240, 80,
                               **button_configuration)
        self.create_map_button("Auckland", 265, 115,
                               **button_configuration)
        self.create_map_button("Waikato", 270, 150,
                               **button_configuration)
        self.create_map_button("Bay of Plenty", 400, 115,
                               **button_configuration)
        self.create_map_button("Gisborne", 450, 165,
                               **button_configuration)
        self.create_map_button("Hawke's Bay", 420, 210,
                               **button_configuration)
        self.create_map_button("Taranaki", 260, 185,
                               **button_configuration)
        self.create_map_button("Manawatu", 400, 240,
                               **button_configuration)
        self.create_map_button("Wellington", 380, 270,
                               **button_configuration)
        self.create_map_button("Marlborough", 220, 230,
                               **button_configuration)
        self.create_map_button("West Coast", 190, 280,
                               **button_configuration)
        self.create_map_button("Canterbury", 325, 310,
                               **button_configuration)
        self.create_map_button("Otago", 280, 380,
                               **button_configuration)
        self.create_map_button("Southland", 125, 340,
                               **button_configuration)

    # Create a button and place it on the map at given coordinates
    def create_map_button(self, region_name, x, y, **kwargs):
        button = tk.Button(self.root, text=region_name, **kwargs)
        button.place(x=x - kwargs.get("width", 8) * 6, y=y, anchor=tk.CENTER)


# Start the GUI application if run directly
if __name__ == '__main__':
    root = tk.Tk()
    quiz = AotearoaQuiz(root)
    root.mainloop()
