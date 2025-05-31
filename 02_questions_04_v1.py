"""02_questions_04 enables users to submit answers, evaluates correctness,
 and updates the score counter accordingly."""

# Import tkinter and PIL for GUI and image handling
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk


# Quiz app class to display NZ map with region buttons and quiz questions
class AotearoaQuiz(object):
    def __init__(self, roots):
        self.current_maori_names = None
        self.root = roots
        self.root.title("Aotearoa Names Quiz")

        # Dictionary of regions with their Maori names (answers)
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

        self.region_buttons = {}  # Holds the buttons for each region
        self.current_region = None  # Currently selected region for quiz

        # Load the NZ map image, set window size based on image dimensions
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

        self.correct_answers = 0  # Count of correct answers so far
        self.incorrect_answers = 0  # Count of incorrect answers so far

        # Frame at top to display score counters
        self.score_frame = tk.Frame(self.root)
        self.score_frame.pack(fill=tk.X)

        # Canvas to display the NZ map image
        self.map_canvas = tk.Canvas(roots, width=self.nz_image.width,
                                    height=self.nz_image.height)
        self.map_canvas.create_image(0, 0, image=self.nz_photo,
                                     anchor=tk.NW)
        self.map_canvas.pack()

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

        # Frame to display the current question and input answer
        self.question_frame = tk.Frame(self.root)
        self.question_frame.pack(pady=10)

        self.question_label = tk.Label(self.question_frame, text="",
                                       font=("Arial", 16))
        self.question_label.pack()

        self.answer_entry = tk.Entry(self.question_frame, font=("Arial", 14))
        self.answer_entry.pack(pady=5)

        # Button to submit the answer, initially disabled
        self.submit_button = tk.Button(self.question_frame,
                                       text="Submit Answer",
                                       font=("Arial", 14),
                                       command=self.check_answer)
        self.submit_button.pack(pady=10)
        self.submit_button.config(state=tk.DISABLED)

        # Label to display count of correct answers
        self.correct_label = tk.Label(self.score_frame,
                                      text=f"Correct: {self.correct_answers}",
                                      font=("Arial", 10))
        self.correct_label.pack(side=tk.LEFT, padx=10, pady=5)

        # Visual separator between score counts
        separator = tk.Label(self.score_frame, text=" | ", font=("Arial", 10))
        separator.pack(side=tk.LEFT)

        # Label to display count of incorrect answers
        self.incorrect_label = tk.Label(
            self.score_frame, text=f"Incorrect: {self.incorrect_answers}",
            font=("Arial", 10))
        self.incorrect_label.pack(side=tk.LEFT)

    # Update score labels depending on whether answer is correct or not
    def update_score(self, correct=True):
        if correct:
            self.correct_answers += 1
            self.correct_label.config(text=f"Correct: {self.correct_answers}")
        else:
            self.incorrect_answers += 1
            self.incorrect_label.config(
                text=f"Incorrect: {self.incorrect_answers}")

    # Create all region buttons on the map at approximate coordinates
    def create_region_buttons_on_map(self):
        button_configuration = {"width": 10, "height": 1, "font": ("Arial", 8)}

        # Place buttons roughly positioned on the map image
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

    # Create an individual button on the map at given position
    def create_map_button(self, region_name, x, y, **kwargs):
        button = tk.Button(self.root, text=region_name, **kwargs,
                           command=lambda r=region_name:
                           self.show_question(r))
        # Adjust x position to roughly center button on given coords
        button.place(x=x - kwargs.get("width", 8) * 6, y=y, anchor=tk.CENTER)
        self.region_buttons[region_name] = button

    # Show question asking for Maori name of the selected region
    def show_question(self, region):
        self.current_region = region
        self.current_maori_names = self.regions[region]  # store for later use
        question_text = f"What is the Maori name for {region}?"
        self.question_label.config(text=question_text)
        self.answer_entry.delete(0, tk.END)
        self.submit_button.config(state=tk.NORMAL)
        for name, button in self.region_buttons.items():
            button.config(state=tk.DISABLED)

    # Check user's input answer against correct Maori names
    def check_answer(self):
        if self.current_region:
            user_answer = self.answer_entry.get().strip()
            correct_maori_names = self.regions[self.current_region]
            if user_answer in correct_maori_names:
                self.update_score(True)
            else:
                self.update_score(False)

            self.question_label.config(text="")
            self.answer_entry.delete(0, tk.END)
            self.submit_button.config(state=tk.DISABLED)
            # Re-enable region buttons after answer submitted
            for name, button in self.region_buttons.items():
                button.config(state=tk.NORMAL)
            self.current_region = None


# Start the tkinter GUI loop and launch the quiz app
if __name__ == '__main__':
    root = tk.Tk()
    quiz = AotearoaQuiz(root)
    root.mainloop()
