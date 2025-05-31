"""02_questions_04_v2 modifies the question submission process by replacing
the text box with multiple-choice options. Each question will present one
correct answer and two randomly generated, unique incorrect options."""

# Import tkinter for GUI, PIL for images, and random for answer options
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random


# Quiz app showing NZ map with region buttons and multiple-choice answers
class AotearoaQuiz(object):
    def __init__(self, roots):
        self.root = roots
        self.root.title("Aotearoa Names Quiz")

        # Regions dictionary mapping English names to lists of Maori names
        self.regions = {
            "Northland": ["Te Tai Tokerau"],
            "Auckland": ["Tāmaki Makaurau"],
            "Waikato": ["Waikato"],
            "Bay of Plenty": ["Te Moana-a-Toitehuatahi"],
            "Gisborne": ["Tūranganui-a-Kiwa"],
            "Hawke's Bay": ["Te Matau-a-Māui"],
            "Taranaki": ["Taranaki"],
            "Manawatu": ["Manawatū-Whanganui"],
            "Wellington": ["Te Whanganui-a-Tara"],
            "Marlborough": ["Te Tauihu-o-te-waka"],
            "West Coast": ["Te Tai Poutini"],
            "Canterbury": ["Waitaha"],
            "Otago": ["Ōtākou"],
            "Southland": ["Murihiku"]}

        self.region_buttons = {}  # Holds map buttons by region name
        self.current_region = None  # Selected region for current question
        self.correct_answer = None  # Correct Maori name for current region
        self.answer_buttons = []  # List of answer choice buttons displayed

        # Load the NZ map image, set window size accordingly
        try:
            self.nz_image = Image.open("Design 2 Trans.png")
            self.nz_photo = ImageTk.PhotoImage(self.nz_image)

            image_width = self.nz_image.width
            image_height = self.nz_image.height
            extra_width = max(150, 350)
            window_width = max(image_width, extra_width + 100)
            window_height = image_height + 300

            self.root.geometry(f"{window_width}x{window_height}")

        except FileNotFoundError:
            messagebox.showerror("Error",
                                 "New Zealand map image not found!")
            self.root.destroy()
            return

        self.correct_answers = 0  # Number of correct answers so far
        self.incorrect_answers = 0  # Number of incorrect answers so far

        # Frame to hold the score counters
        self.score_frame = tk.Frame(self.root)
        self.score_frame.pack(fill=tk.X)

        # Canvas displaying the NZ map image
        self.map_canvas = tk.Canvas(roots, width=self.nz_image.width,
                                    height=self.nz_image.height)
        self.map_canvas.create_image(0, 0, image=self.nz_photo,
                                     anchor=tk.NW)
        self.map_canvas.pack()

        # Frame to hold question text and answer buttons
        self.question_frame = tk.Frame(self.root)
        self.question_frame.pack(pady=10)

        # Label to show the current quiz question
        self.question_label = tk.Label(self.question_frame, text="",
                                       font=("Arial", 16))
        self.question_label.pack()

        # Frame to hold answer option buttons
        self.options_frame = tk.Frame(self.question_frame)
        self.options_frame.pack()

        # Labels for correct and incorrect score counters
        self.correct_label = tk.Label(self.score_frame,
                                      text=f"Correct: {self.correct_answers}",
                                      font=("Arial", 10))
        self.correct_label.pack(side=tk.LEFT, padx=10, pady=5)

        separator = tk.Label(self.score_frame, text=" | ", font=("Arial", 10))
        separator.pack(side=tk.LEFT)

        self.incorrect_label = tk.Label(
            self.score_frame, text=f"Incorrect: {self.incorrect_answers}",
            font=("Arial", 10))
        self.incorrect_label.pack(side=tk.LEFT)

        # Load and display the logo image at bottom-right corner
        try:
            self.logo_image = Image.open(
                "HenyDice Logo Trans.png")
            self.logo_photo = ImageTk.PhotoImage(self.logo_image)
            self.logo_label = tk.Label(self.root, image=self.logo_photo)
            self.logo_label.place(relx=1.0, rely=1.0, x=-10, anchor='se')

        except FileNotFoundError:
            messagebox.showwarning("Warning",
                                   "Logo image not found!")

        # Create clickable buttons on the map for each region
        self.create_region_buttons_on_map()

    # Update score display after each answer (correct or incorrect)
    def update_score(self, correct=True):
        if correct:
            self.correct_answers += 1
            self.correct_label.config(text=f"Correct: {self.correct_answers}")
        else:
            self.incorrect_answers += 1
            self.incorrect_label.config(
                text=f"Incorrect: {self.incorrect_answers}")

    # Create buttons for each region placed approximately on the map
    def create_region_buttons_on_map(self):
        button_configuration = {"width": 10, "height": 1, "font": ("Arial", 8)}

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

    # Create an individual map button with a callback to show question
    def create_map_button(self, region_name, x, y, **kwargs):
        button = tk.Button(self.root, text=region_name, **kwargs,
                           command=lambda r=region_name:
                           self.show_question(r))
        button.place(x=x - kwargs.get("width", 8) * 6, y=y, anchor=tk.CENTER)
        self.region_buttons[region_name] = button

    def _handle_answer_selection(self, user_answer):
        self.check_answer(user_answer)

    # Display a multiple-choice question for the selected region
    def show_question(self, region):
        self.current_region = region
        correct_maori_names = self.regions[region]
        self.correct_answer = random.choice(correct_maori_names)

        incorrect_options = set()
        all_maori_names = [name for sublist in self.regions.values() for name
                           in sublist]

        # Pick 2 unique incorrect options different from correct answer
        while len(incorrect_options) < 2:
            wrong_answer = random.choice(all_maori_names)
            if wrong_answer not in correct_maori_names:
                incorrect_options.add(wrong_answer)

        options = list(incorrect_options) + [self.correct_answer]
        random.shuffle(options)  # Shuffle options randomly

        question_text = f"What is the Maori name for {region}?"
        self.question_label.config(text=question_text)

        # Remove any old answer buttons before creating new ones
        for button in self.answer_buttons:
            button.destroy()
        self.answer_buttons = []

        # Create buttons for each answer option
        for option in options:
            answer_button = tk.Button(self.options_frame, text=option,
                                      font=("Arial", 12),
                                      command=lambda ans=option:
                                      self.check_answer(ans))
            answer_button.pack(pady=5)
            self.answer_buttons.append(answer_button)

        # Disable region buttons while answering
        for name, button in self.region_buttons.items():
            button.config(state=tk.DISABLED)

    # Check if user's selected answer matches the correct one
    def check_answer(self, user_answer):
        if self.current_region:
            if user_answer == self.correct_answer:
                self.update_score(True)
            else:
                self.update_score(False)

            self.question_label.config(text="")
            # Remove answer buttons after selection
            for button in self.answer_buttons:
                button.destroy()
            self.answer_buttons = []

            # Re-enable region buttons for next question
            for name, button in self.region_buttons.items():
                button.config(state=tk.NORMAL)

            self.current_region = None
            self.correct_answer = None


# Run the application
if __name__ == '__main__':
    root = tk.Tk()
    quiz = AotearoaQuiz(root)
    root.mainloop()
