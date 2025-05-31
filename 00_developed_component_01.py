"""Adding Component 1 to the final developed outcome."""

# Import tkinter for GUI and PIL for image processing
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk


# Class to show NZ map with region buttons and track quiz scores
class AotearoaQuiz(object):
    def __init__(self, roots):
        self.root = roots
        self.root.title("Aotearoa Names Quiz")

        # Initialize counters for correct/incorrect answers
        self.correct_answers = 0
        self.incorrect_answers = 0

        # Frame to hold score labels at the top
        self.score_frame = tk.Frame(self.root)
        self.score_frame.pack(fill=tk.X)

        # Label showing number of correct answers
        self.correct_label = tk.Label(self.score_frame,
                                      text=f"Correct: {self.correct_answers}",
                                      font=("Arial", 10))
        self.correct_label.pack(side=tk.LEFT, padx=10, pady=5)

        # Separator label between correct and incorrect
        separator = tk.Label(self.score_frame, text=" | ", font=("Arial", 10))
        separator.pack(side=tk.LEFT)

        # Label showing number of incorrect answers
        self.incorrect_label = tk.Label(
            self.score_frame, text=f"Incorrect: {self.incorrect_answers}",
            font=("Arial", 10))
        self.incorrect_label.pack(side=tk.LEFT)

        # Load NZ map image for background
        try:
            self.nz_image = Image.open("Design 2 Trans.png")
            self.nz_photo = ImageTk.PhotoImage(self.nz_image)

            image_width = self.nz_image.width
            image_height = self.nz_image.height
            extra_width = max(150, 350)
            window_width = max(image_width, extra_width + 100)
            window_height = image_height + 50

            # Set window size based on image and UI elements
            self.root.geometry(f"{window_width}x{window_height}")

        except FileNotFoundError:
            # Show error and exit if map image not found
            messagebox.showerror("Error",
                                 "New Zealand map image not found!")
            self.root.destroy()
            return

        # Create canvas and place map image on it
        self.map_canvas = tk.Canvas(roots, width=self.nz_image.width,
                                    height=self.nz_image.height)
        self.map_canvas.create_image(0, 0, image=self.nz_photo,
                                     anchor=tk.NW)
        self.map_canvas.pack()

        # Load and place logo image in bottom-right corner
        try:
            self.logo_image = Image.open(
                "HenyDice Logo Trans.png")
            self.logo_photo = ImageTk.PhotoImage(self.logo_image)
            self.logo_label = tk.Label(self.root, image=self.logo_photo)
            self.logo_label.place(relx=1.0, rely=1.0, x=-10, anchor='se')

        except FileNotFoundError:
            # Warn if logo image missing
            messagebox.showwarning("Warning",
                                   "Logo image not found!")

        # Add clickable region buttons on the map
        self.create_region_buttons_on_map()

    # Update the score labels after answer is given
    def update_score(self, correct=True):
        if correct:
            self.correct_answers += 1
            self.correct_label.config(text=f"Correct:{self.correct_answers}")
        else:
            self.incorrect_answers += 1
            self.incorrect_label.config(text=f"Incorrect:"
                                             f"{self.incorrect_answers}")

    # Add buttons representing regions positioned on the map
    def create_region_buttons_on_map(self):
        button_configuration = {"width": 10, "height": 1, "font": ("Arial", 8)}

        # Create each region button with approximate map coords
        self.create_map_button("Northland",
                               240, 80, **button_configuration)
        self.create_map_button("Auckland",
                               265, 115, **button_configuration)
        self.create_map_button("Waikato",
                               270, 150, **button_configuration)
        self.create_map_button("Bay of Plenty",
                               400, 115, **button_configuration)
        self.create_map_button("Gisborne",
                               450, 165, **button_configuration)
        self.create_map_button("Hawke's Bay",
                               420, 210, **button_configuration)
        self.create_map_button("Taranaki",
                               260, 185, **button_configuration)
        self.create_map_button("Manawatu",
                               400, 240, **button_configuration)
        self.create_map_button("Wellington",
                               380, 270, **button_configuration)
        self.create_map_button("Marlborough",
                               220, 230, **button_configuration)
        self.create_map_button("West Coast",
                               190, 280, **button_configuration)
        self.create_map_button("Canterbury",
                               325, 310, **button_configuration)
        self.create_map_button("Otago",
                               280, 380, **button_configuration)
        self.create_map_button("Southland",
                               125, 340, **button_configuration)

    # Create and place a single region button on the map canvas
    def create_map_button(self, region_name, x, y, **kwargs):
        button = tk.Button(self.root, text=region_name, **kwargs)
        button.place(x=x - kwargs.get("width", 8) * 6, y=y, anchor=tk.CENTER)


# Start the tkinter main event loop when script runs
if __name__ == '__main__':
    root = tk.Tk()
    quiz = AotearoaQuiz(root)
    root.mainloop()
