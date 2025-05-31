"""03_questions_01 displays an end screen showing the user’s total correct
and incorrect answers along with their percentage score."""

# Import tkinter for GUI, PIL for image processing, and random for choices
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random


# Class to display NZ map, region buttons, and quiz questions
class AotearoaQuiz(object):
    def __init__(self, roots):
        self.root = roots
        self.root.title("Aotearoa Names Quiz")

        # Dictionary mapping regions to their Māori names
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
            "Southland": ["Murihiku"]
        }

        # Initialize variables to track buttons, current question, answers
        self.region_buttons = {}
        self.current_region = None
        self.correct_answer = None
        self.answer_buttons = []
        self.answered_regions = set()
        self.current_options = []

        # Load New Zealand map image for display
        try:
            self.nz_image = Image.open("Design 2 Trans.png")
            self.nz_photo = ImageTk.PhotoImage(self.nz_image)

            image_width = self.nz_image.width
            image_height = self.nz_image.height

            # Calculate window size with extra width for UI elements
            extra_width = max(150, 350)
            window_width = max(image_width, extra_width + 100)
            window_height = image_height + 300

            self.root.geometry(f"{window_width}x{window_height}")

        except FileNotFoundError:
            # Show error and exit if image file missing
            messagebox.showerror("Error",
                                 "New Zealand map image not found!")
            self.root.destroy()
            return

        # Counters for quiz progress
        self.correct_answers = 0
        self.incorrect_answers = 0
        self.total_questions = len(self.regions)

        # Frame to display score (correct and incorrect)
        self.score_frame = tk.Frame(self.root)
        self.score_frame.pack(fill=tk.X)

        # Canvas to display the map image
        self.map_canvas = tk.Canvas(roots, width=self.nz_image.width,
                                    height=self.nz_image.height)
        self.map_canvas.create_image(0, 0, image=self.nz_photo,
                                     anchor=tk.NW)
        self.map_canvas.pack()

        # Frame to hold question text and answer buttons
        self.question_frame = tk.Frame(self.root)
        self.question_frame.pack(pady=10)

        # Label showing the current question text
        self.question_label = tk.Label(self.question_frame, text="",
                                       font=("Arial", 16))
        self.question_label.pack()

        # Frame holding answer buttons
        self.options_frame = tk.Frame(self.question_frame)
        self.options_frame.pack()

        # Frame for the close question button
        self.close_button_frame = tk.Frame(self.question_frame)
        self.close_button_frame.pack(pady=5)

        # Button to close the current question
        self.close_button = tk.Button(self.close_button_frame,
                                      text="Close Question",
                                      font=("Arial", 13), bg="red",
                                      fg="white",
                                      command=self.close_current_question)
        self.close_button.pack()
        self.close_button.pack_forget()  # Hide initially

        # Label showing correct answer count
        self.correct_label = tk.Label(self.score_frame,
                                      text=f"Correct: {self.correct_answers}",
                                      font=("Arial", 10))
        self.correct_label.pack(side=tk.LEFT, padx=10, pady=5)

        # Separator label between correct and incorrect counts
        separator = tk.Label(self.score_frame, text=" | ", font=("Arial", 10))
        separator.pack(side=tk.LEFT)

        # Label showing incorrect answer count
        self.incorrect_label = tk.Label(
            self.score_frame, text=f"Incorrect: {self.incorrect_answers}",
            font=("Arial", 10))
        self.incorrect_label.pack(side=tk.LEFT)

        # Load logo image to display on the window
        try:
            self.logo_image = Image.open("HenyDice Logo Trans.png")
            self.logo_photo = ImageTk.PhotoImage(self.logo_image)
            self.logo_label = tk.Label(self.root, image=self.logo_photo)
            self.logo_label.place(relx=1.0, rely=1.0, x=-10, anchor='se')

        except FileNotFoundError:
            # Warn if logo image is missing, but continue
            messagebox.showwarning("Warning",
                                   "Logo image not found!")

        # Create interactive buttons for all regions on the map
        self.create_region_buttons_on_map()

    # Close current question UI and reset states
    def close_current_question(self):
        if self.current_region:
            self.question_label.config(text="")
            for button in self.answer_buttons:
                button.destroy()
            self.answer_buttons = []
            self.close_button.pack_forget()

            # Enable region buttons that haven't been answered yet
            for name, button in self.region_buttons.items():
                if name not in self.answered_regions:
                    button.config(state=tk.NORMAL)

            # Reset current question tracking variables
            self.current_region = None
            self.correct_answer = None
            self.current_options = []

    # Update score counters and show message boxes for answer feedback
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

    # Create buttons on the map for each region at approx coordinates
    def create_region_buttons_on_map(self):
        button_configuration = {"width": 10, "height": 1, "font": ("Arial", 8)}

        # Approximate locations for each region button on map image
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

    # Create a single map button for a region at given coords and bind click
    def create_map_button(self, region_name, x, y, **kwargs):
        button = tk.Button(self.root, text=region_name, **kwargs,
                           command=lambda r=region_name:
                           self.show_question(r))
        button.place(x=x - kwargs.get("width", 8) * 6, y=y, anchor=tk.CENTER)
        self.region_buttons[region_name] = button

    # Handle user's answer selection (calls check_answer)
    def _handle_answer_selection(self, user_answer):
        self.check_answer(user_answer)

    # Display question and multiple-choice answers for selected region
    def show_question(self, region):
        self.current_region = region
        correct_maori_names = self.regions[region]
        self.correct_answer = random.choice(correct_maori_names)

        incorrect_options = set()
        all_maori_names = [name for sublist in self.regions.values() for
                           name in sublist]

        # Pick 2 incorrect answers different from correct ones
        while len(incorrect_options) < 2:
            wrong_answer = random.choice(all_maori_names)
            if wrong_answer not in correct_maori_names:
                incorrect_options.add(wrong_answer)

        # Combine and shuffle options
        options = list(incorrect_options) + [self.correct_answer]
        random.shuffle(options)

        question_text = f"What is the Maori name for {region}?"
        self.question_label.config(text=question_text)

        # Clear previous answer buttons
        for button in self.answer_buttons:
            button.destroy()
        self.answer_buttons = []

        # Create buttons for answer options
        for option in options:
            answer_button = tk.Button(self.options_frame, text=option,
                                      font=("Arial", 12),
                                      command=lambda ans=option:
                                      self.check_answer(ans))
            answer_button.pack(pady=5)
            self.answer_buttons.append(answer_button)

        # Show close question button
        self.close_button.pack()

        # Disable all region buttons while answering
        for name, button in self.region_buttons.items():
            button.config(state=tk.DISABLED)

    # Check user's answer and update UI accordingly
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

            # Clear question text and answer buttons
            self.question_label.config(text="")
            for button in self.answer_buttons:
                button.destroy()
            self.answer_buttons = []

            # Mark region as answered
            self.answered_regions.add(self.current_region)

            # Disable answered region button
            if region_button:
                region_button.config(state=tk.DISABLED)

            # If all questions answered, finish quiz
            if len(self.answered_regions) == self.total_questions:
                self.finish_quiz()
            else:
                # Enable buttons for unanswered regions
                for name, button in self.region_buttons.items():
                    if name not in self.answered_regions:
                        button.config(state=tk.NORMAL)

            # Reset current question state
            self.current_region = None
            self.correct_answer = None

    # Show final quiz result summary
    def finish_quiz(self):
        accuracy = (self.correct_answers / self.total_questions) * 100
        final_score_message = (f"The Quiz Is Finished!\n"
                               f"Correct Answers: {self.correct_answers}\n"
                               f"Incorrect Answers: {self.incorrect_answers}\n"
                               f"Percentage: {accuracy:.2f}%")
        messagebox.showinfo("Quiz End", final_score_message)


# Run the quiz app
if __name__ == '__main__':
    root = tk.Tk()
    quiz = AotearoaQuiz(root)
    root.mainloop()
