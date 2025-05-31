"""02_questions_02 adds a frame to display questions, accept user input,
and submit answers."""

# Import tkinter for GUI and PIL for image handling
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk


# Class to display NZ map with region buttons and quiz interface
class AotearoaQuiz(object):
    def __init__(self, roots):
        self.root = roots
        self.root.title("Aotearoa Names Quiz")

        # Dictionary mapping English region names to Maori names
        self.regions = {
            "Northland": ["Te Tai Tokerau"],
            "Auckland": ["Tamaki Makaurau"],
            "Waikato": ["Waikato"],
            "Bay of Plenty": ["Te Moana-a-Toitehuatahi"],
            "Gisborne": ["Tūranganui-a-Kiwa"],
            "Hawke's Bay": ["Te Matau-a-Māui"],
            "Taranaki": ["Taranaki"],
            "Manawatu-Whanganui": ["Manawatu-Whanganui"],
            "Wellington": ["Te Whanganui-a-Tara"],
            "Marlborough": ["Te Tauihu-o-te-waka"],
            "West Coast": ["Te Tai Poutini"],
            "Canterbury": ["Rakahuri"],
            "Otago": ["Ōtākou"],
            "Southland": ["Murihiku"]
        }

        # Initialize correct/incorrect answer counters
        self.correct_answers = 0
        self.incorrect_answers = 0

        # Frame to display score counters
        self.score_frame = tk.Frame(self.root)
        self.score_frame.pack(fill=tk.X)

        # Load NZ map image
        try:
            self.nz_image = Image.open("Design 2 Trans.png")
            self.nz_photo = ImageTk.PhotoImage(self.nz_image)

            # Set window size based on image dimensions plus extra space
            image_width = self.nz_image.width
            image_height = self.nz_image.height
            extra_width = max(150, 350)
            window_width = max(image_width, extra_width + 100)
            window_height = image_height + 300
            self.root.geometry(f"{window_width}x{window_height}")

        except FileNotFoundError:
            # Show error if image is missing, then close app
            messagebox.showerror("Error",
                                 "New Zealand map image not found!")
            self.root.destroy()
            return

        # Canvas to display the NZ map
        self.map_canvas = tk.Canvas(roots, width=self.nz_image.width,
                                    height=self.nz_image.height)
        self.map_canvas.create_image(0, 0,
                                     image=self.nz_photo, anchor=tk.NW)
        self.map_canvas.pack()

        # Load logo image and place at bottom-right corner
        try:
            self.logo_image = Image.open("HenyDice Logo Trans.png")
            self.logo_photo = ImageTk.PhotoImage(self.logo_image)
            self.logo_label = tk.Label(self.root, image=self.logo_photo)
            self.logo_label.place(relx=1.0, rely=1.0, x=-10, anchor='se')

        except FileNotFoundError:
            # Warn if logo image not found, but continue running app
            messagebox.showwarning("Warning",
                                   "Logo image not found!")

        # Create region buttons on map
        self.create_region_buttons_on_map()

        # Frame for question display, answer entry, and submit button
        self.question_frame = tk.Frame(self.root)
        self.question_frame.pack(pady=10)

        self.question_label = tk.Label(self.question_frame,
                                       text="", font=("Arial", 16))
        self.question_label.pack()

        self.answer_entry = tk.Entry(self.question_frame, font=("Arial", 14))
        self.answer_entry.pack(pady=5)

        self.submit_button = tk.Button(self.question_frame,
                                       text="Submit Answer",
                                       font=("Arial", 14))
        self.submit_button.pack(pady=10)
        self.submit_button.config(state=tk.DISABLED)  # Disabled initially

        # Correct answers label
        self.correct_label = tk.Label(self.score_frame,
                                      text=f"Correct: {self.correct_answers}",
                                      font=("Arial", 10))
        self.correct_label.pack(side=tk.LEFT, padx=10, pady=5)

        # Separator label
        separator = tk.Label(self.score_frame, text=" | ", font=("Arial", 10))
        separator.pack(side=tk.LEFT)

        # Incorrect answers label
        self.incorrect_label = tk.Label(self.score_frame,
                                        text=f"Incorrect: "
                                             f"{self.incorrect_answers}",
                                        font=("Arial", 10))
        self.incorrect_label.pack(side=tk.LEFT)

    # Update score display based on correctness of answer
    def update_score(self, correct=True):
        if correct:
            self.correct_answers += 1
            self.correct_label.config(text=f"Correct: {self.correct_answers}")
        else:
            self.incorrect_answers += 1
            self.incorrect_label.config(text=f"Incorrect: "
                                             f"{self.incorrect_answers}")

    # Create buttons positioned over the map for each region
    def create_region_buttons_on_map(self):
        button_configuration = {"width": 10, "height": 1, "font": ("Arial", 8)}

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

    # Helper method to create and place a button for a region
    def create_map_button(self, region_name, x, y, **kwargs):
        button = tk.Button(self.root, text=region_name, **kwargs)
        button.place(x=x - kwargs.get("width", 8) * 6, y=y, anchor=tk.CENTER)


# Run application if this script is executed directly
if __name__ == '__main__':
    root = tk.Tk()
    quiz = AotearoaQuiz(root)
    root.mainloop()
