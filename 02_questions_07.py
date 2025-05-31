"""02_questions_07 adds a close button to the question view, letting users
close the question without answering and keeping the region available to
answer later."""

# Import tkinter for GUI, PIL for image handling, and random for choices
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random


# Class for quiz app showing map, questions, and answer buttons
class AotearoaQuiz(object):
    def __init__(self, roots):
        self.root = roots
        self.root.title("Aotearoa Names Quiz")

        # Regions with their correct Māori names
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

        # Initialize variables to track buttons and quiz state
        self.region_buttons = {}
        self.current_region = None
        self.correct_answer = None
        self.answer_buttons = []
        self.answered_regions = set()
        self.current_options = []

        # Load NZ map image and set window size accordingly
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
            # Show error if image not found and close app
            messagebox.showerror("Error",
                                 "New Zealand map image not found!")
            self.root.destroy()
            return

        # Initialize correct/incorrect answer counters
        self.correct_answers = 0
        self.incorrect_answers = 0

        # Frame to display the score at the top of the window
        self.score_frame = tk.Frame(self.root)
        self.score_frame.pack(fill=tk.X)

        # Canvas to show the NZ map image
        self.map_canvas = tk.Canvas(roots, width=self.nz_image.width,
                                    height=self.nz_image.height)
        self.map_canvas.create_image(0, 0, image=self.nz_photo,
                                     anchor=tk.NW)
        self.map_canvas.pack()

        # Frame for question text and answer buttons
        self.question_frame = tk.Frame(self.root)
        self.question_frame.pack(pady=10)

        # Label to display the current question
        self.question_label = tk.Label(self.question_frame, text="",
                                       font=("Arial", 16))
        self.question_label.pack()

        # Frame to hold answer option buttons
        self.options_frame = tk.Frame(self.question_frame)
        self.options_frame.pack()

        # Frame and button to allow closing the current question early
        self.close_button_frame = tk.Frame(self.question_frame)
        self.close_button_frame.pack(pady=5)

        self.close_button = tk.Button(self.close_button_frame,
                                      text="Close Question",
                                      font=("Arial", 13), bg="red",
                                      fg="white",
                                      command=self.close_current_question)
        self.close_button.pack()
        self.close_button.pack_forget()  # Hide initially

        # Label to display number of correct answers
        self.correct_label = tk.Label(self.score_frame,
                                      text=f"Correct: {self.correct_answers}",
                                      font=("Arial", 10))
        self.correct_label.pack(side=tk.LEFT, padx=10, pady=5)

        # Separator label between correct and incorrect counts
        separator = tk.Label(self.score_frame, text=" | ", font=("Arial", 10))
        separator.pack(side=tk.LEFT)

        # Label to display number of incorrect answers
        self.incorrect_label = tk.Label(
            self.score_frame, text=f"Incorrect: {self.incorrect_answers}",
            font=("Arial", 10))
        self.incorrect_label.pack(side=tk.LEFT)

        # Try loading a logo image to display on window
        try:
            self.logo_image = Image.open(
                "HenyDice Logo Trans.png")
            self.logo_photo = ImageTk.PhotoImage(self.logo_image)
            self.logo_label = tk.Label(self.root, image=self.logo_photo)
            self.logo_label.place(relx=1.0, rely=1.0, x=-10, anchor='se')

        except FileNotFoundError:
            # Warn user if logo image missing but continue
            messagebox.showwarning("Warning",
                                   "Logo image not found!")

        # Create clickable region buttons on the map
        self.create_region_buttons_on_map()

    # Close the current question and reset interface
    def close_current_question(self):
        if self.current_region:
            self.question_label.config(text="")
            for button in self.answer_buttons:
                button.destroy()
            self.answer_buttons = []
            self.close_button.pack_forget()

            # Re-enable region buttons that haven't been answered
            for name, button in self.region_buttons.items():
                if name not in self.answered_regions:
                    button.config(state=tk.NORMAL)

            # Reset current question variables
            self.current_region = None
            self.correct_answer = None
            self.current_options = []

    # Update the score display and show popup for right/wrong answers
    def update_score(self, correct=True):
        if correct:
            self.correct_answers += 1
            messagebox.showinfo(message=f"{self.correct_answer} "
                                        f"was the correct answer for "
                                        f"{self.current_region}",
                                title="Correct!")
            self.correct_label.config(text=f"Correct: {self.correct_answers}")
        else:
            self.incorrect_answers += 1
            messagebox.showerror(
                message=f"That was not the correct answer for "
                        f"{self.current_region}. The correct "
                        f"answer was {self.correct_answer}",
                title="Incorrect!")
            self.incorrect_label.config(
                text=f"Incorrect: {self.incorrect_answers}")

    # Place region buttons on the map at approximate coordinates
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

    # Create an individual map button for a region with a command
    def create_map_button(self, region_name, x, y, **kwargs):
        button = tk.Button(self.root, text=region_name, **kwargs,
                           command=lambda r=region_name:
                           self.show_question(r))
        button.place(x=x - kwargs.get("width", 8) * 6, y=y, anchor=tk.CENTER)
        self.region_buttons[region_name] = button

    # Internal handler to check answer selection
    def _handle_answer_selection(self, user_answer):
        self.check_answer(user_answer)

    # Show question and multiple-choice options for selected region
    def show_question(self, region):
        self.current_region = region
        correct_maori_names = self.regions[region]
        self.correct_answer = random.choice(correct_maori_names)
        incorrect_options = set()
        all_maori_names = [name for sublist in self.regions.values() for name
                           in sublist]

        # Select 2 incorrect options different from the correct answer(s)
        while len(incorrect_options) < 2:
            wrong_answer = random.choice(all_maori_names)
            if wrong_answer not in correct_maori_names:
                incorrect_options.add(wrong_answer)

        # Combine correct and incorrect options and shuffle them
        options = list(incorrect_options) + [self.correct_answer]
        random.shuffle(options)

        question_text = f"What is the Maori name for {region}?"
        self.question_label.config(text=question_text)

        # Remove previous answer buttons before adding new ones
        for button in self.answer_buttons:
            button.destroy()
        self.answer_buttons = []

        # Create answer buttons for each option
        for option in options:
            answer_button = tk.Button(self.options_frame, text=option,
                                      font=("Arial", 12),
                                      command=lambda ans=option:
                                      self.check_answer(ans))
            answer_button.pack(pady=5)
            self.answer_buttons.append(answer_button)

        self.close_button.pack()  # Show the close question button

        # Disable all region buttons while answering
        for name, button in self.region_buttons.items():
            button.config(state=tk.DISABLED)

    # Check the user's answer and update the UI accordingly
    def check_answer(self, user_answer):
        if self.current_region:
            region_button = self.region_buttons.get(self.current_region)

            if user_answer == self.correct_answer:
                self.update_score(True)
                if region_button:
                    region_button.config(bg="green",
                                         disabledforeground="white")
            else:
                self.update_score(False)
                if region_button:
                    region_button.config(bg="red",
                                         disabledforeground="white")

            self.question_label.config(text="")

            for button in self.answer_buttons:
                button.destroy()
            self.answer_buttons = []

            # Mark this region as answered and disable its button
            self.answered_regions.add(self.current_region)
            if region_button:
                region_button.config(state=tk.DISABLED)

            # Enable buttons for unanswered regions
            for name, button in self.region_buttons.items():
                if name not in self.answered_regions:
                    button.config(state=tk.NORMAL)

            # Reset current question info
            self.current_region = None
            self.correct_answer = None


# Run the app
if __name__ == '__main__':
    root = tk.Tk()
    quiz = AotearoaQuiz(root)
    root.mainloop()
