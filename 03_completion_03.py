"""03_questions_03 adds a feature to export quiz results as a PDF using the
ReportLab library, enabling users to download their results."""

# Import necessary modules for GUI, images, random choices, and PDF export
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch


# Main quiz class for Aotearoa map and quiz functionality
class AotearoaQuiz(object):
    def __init__(self, roots):
        self.last_user_answer = None
        self.root = roots
        self.root.title("Aotearoa Names Quiz")

        # Regions mapped to correct Maori names
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

        # Initialize variables and UI elements
        self.region_buttons = {}
        self.current_region = None
        self.correct_answer = None
        self.answer_buttons = []
        self.answered_regions = set()
        self.current_options = []
        self.quiz_history = []

        # Load New Zealand map image, set window size accordingly
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

        # Score tracking variables
        self.correct_answers = 0
        self.incorrect_answers = 0
        self.total_questions = len(self.regions)

        # Frame for displaying score counters
        self.score_frame = tk.Frame(self.root)
        self.score_frame.pack(fill=tk.X)

        # Canvas to show map image
        self.map_canvas = tk.Canvas(roots, width=self.nz_image.width,
                                    height=self.nz_image.height)
        self.map_canvas.create_image(0, 0, image=self.nz_photo,
                                     anchor=tk.NW)
        self.map_canvas.pack()

        # Frame to hold question text and answers
        self.question_frame = tk.Frame(self.root)
        self.question_frame.pack(pady=10)

        self.question_label = tk.Label(self.question_frame, text="",
                                       font=("Arial", 16))
        self.question_label.pack()

        # Frame for multiple choice answer buttons
        self.options_frame = tk.Frame(self.question_frame)
        self.options_frame.pack()

        # Frame for close question button
        self.close_button_frame = tk.Frame(self.question_frame)
        self.close_button_frame.pack(pady=5)

        self.close_button = tk.Button(self.close_button_frame,
                                      text="Close Question",
                                      font=("Arial", 13), bg="red",
                                      fg="white",
                                      command=self.close_current_question)
        self.close_button.pack()
        self.close_button.pack_forget()  # Hide close button initially

        # Labels for correct and incorrect counts
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

        # Load logo image and place at bottom-right corner
        try:
            self.logo_image = Image.open("HenyDice Logo Trans.png")
            self.logo_photo = ImageTk.PhotoImage(self.logo_image)
            self.logo_label = tk.Label(self.root, image=self.logo_photo)
            self.logo_label.place(relx=1.0, rely=1.0, x=-10, anchor='se')

        except FileNotFoundError:
            messagebox.showwarning("Warning",
                                   "Logo image not found!")

        # Create clickable buttons for each region on the map
        self.create_region_buttons_on_map()

        self.end_screen = None

    # Hide current question and re-enable region buttons
    def close_current_question(self):
        if self.current_region:
            self.question_label.config(text="")
            for button in self.answer_buttons:
                button.destroy()
            self.answer_buttons = []
            self.close_button.pack_forget()

            for name, button in self.region_buttons.items():
                if name not in self.answered_regions:
                    button.config(state=tk.NORMAL)

            self.current_region = None
            self.correct_answer = None
            self.current_options = []

    # Update the score and show popup messages for correctness
    def update_score(self, correct=True):
        if self.current_region and self.correct_answer:
            self.quiz_history.append({
                "region": self.current_region,
                "correct_answer": self.correct_answer,
                "user_answer": self.last_user_answer,
                "correct": correct
            })
        if correct:
            self.correct_answers += 1
            messagebox.showinfo(message=f"{self.correct_answer} "
                                        f"was the correct answer for "
                                        f"{self.current_region}",
                                title="Correct!")
            self.correct_label.config(text=f"Correct: {self.correct_answers}")
        else:
            messagebox.showerror(
                message=f"That was not the correct answer for "
                        f"{self.current_region}. The correct "
                        f"answer was {self.correct_answer}",
                title="Incorrect!")
            self.incorrect_label.config(
                text=f"Incorrect: {self.incorrect_answers}")

    # Place buttons on the map at approximate coordinates
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

    # Create a button for a region on the map, bind to show_question
    def create_map_button(self, region_name, x, y, **kwargs):
        button = tk.Button(self.root, text=region_name, **kwargs,
                           command=lambda r=region_name:
                           self.show_question(r))
        button.place(x=x - kwargs.get("width", 8) * 6, y=y, anchor=tk.CENTER)
        self.region_buttons[region_name] = button

    def _handle_answer_selection(self, user_answer):
        self.check_answer(user_answer)

    # Show question with randomized answer options for the selected region
    def show_question(self, region):
        self.current_region = region
        correct_maori_names = self.regions[region]
        self.correct_answer = random.choice(correct_maori_names)
        incorrect_options = set()
        all_maori_names = [name for sublist in self.regions.values() for name
                           in sublist]

        # Select two incorrect options
        while len(incorrect_options) < 2:
            wrong_answer = random.choice(all_maori_names)
            if wrong_answer not in correct_maori_names:
                incorrect_options.add(wrong_answer)

        options = list(incorrect_options) + [self.correct_answer]
        random.shuffle(options)

        question_text = f"What is the Maori name for {region}?"
        self.question_label.config(text=question_text)

        # Remove old answer buttons and add new ones
        for button in self.answer_buttons:
            button.destroy()
        self.answer_buttons = []

        for option in options:
            answer_button = tk.Button(self.options_frame, text=option,
                                      font=("Arial", 12),
                                      command=lambda ans=option:
                                      self.check_answer(ans))
            answer_button.pack(pady=5)
            self.answer_buttons.append(answer_button)

        self.close_button.pack()

        # Disable all region buttons while question is active
        for name, button in self.region_buttons.items():
            button.config(state=tk.DISABLED)

    # Check if user answer is correct, update buttons and score
    def check_answer(self, user_answer):
        self.last_user_answer = user_answer
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

            self.answered_regions.add(self.current_region)
            if len(self.answered_regions) == self.total_questions:
                self.finish_quiz()
            elif region_button:
                region_button.config(state=tk.DISABLED)

            # Re-enable buttons for unanswered regions
            for name, button in self.region_buttons.items():
                if name not in self.answered_regions:
                    button.config(state=tk.NORMAL)

            self.current_region = None
            self.correct_answer = None

    # Show end screen with score summary and export options
    def finish_quiz(self):
        accuracy = (self.correct_answers / self.total_questions) * 100
        final_score_message = (f"The Quiz Is Finished!\n"
                               f"Correct Answers: {self.correct_answers}\n"
                               f"Incorrect Answers: {self.incorrect_answers}\n"
                               f"Percentage: {accuracy:.2f}%")

        if self.end_screen is None:
            self.end_screen = tk.Toplevel(self.root)
            self.end_screen.title("Quiz Finished")

            message_label = tk.Label(self.end_screen, text=final_score_message,
                                     font=("Arial", 10))
            message_label.pack(padx=25, pady=25)

            export_button_end = tk.Button(self.end_screen,
                                          text="Export Results to PDF",
                                          font=("Arial", 10), bg="blue",
                                          fg='white',
                                          command=self.export_results_pdf)
            export_button_end.pack(pady=5)

            play_again_button = tk.Button(self.end_screen, text="Play Again",
                                          font=("Arial", 10), bg="green",
                                          fg='white',
                                          command=self.reset_quiz)
            play_again_button.pack(pady=10)
        else:
            # Update message if end screen already exists
            for widget in self.end_screen.winfo_children():
                if isinstance(widget, tk.Label):
                    widget.config(text=final_score_message)
            self.end_screen.lift()

    # Reset quiz to initial state for replay
    def reset_quiz(self):
        self.correct_answers = 0
        self.incorrect_answers = 0
        self.answered_regions = set()
        self.quiz_history = []
        self.correct_label.config(text=f"Correct: {self.correct_answers}")
        self.incorrect_label.config(
            text=f"Incorrect: {self.incorrect_answers}")

        for name, button in self.region_buttons.items():
            button.config(state=tk.NORMAL, bg=self.root.cget('bg'),
                          disabledforeground='white')

        if self.end_screen:
            self.end_screen.destroy()
            self.end_screen = None

    # Export quiz results with details to a PDF file
    def export_results_pdf(self):
        filename = "quiz_results.pdf"
        doc = SimpleDocTemplate(filename, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []

        title = Paragraph("Aotearoa Names Quiz Results", styles['h1'])
        story.append(title)
        story.append(Spacer(1, 0.2 * inch))

        summary = Paragraph(
            f"Final Score: Correct Answers: {self.correct_answers}, "
            f"Incorrect Answers: {self.incorrect_answers}, "
            f"Percentage: "
            f"{(self.correct_answers / self.total_questions) * 100:.2f}%",
            styles['Normal'])
        story.append(summary)
        story.append(Spacer(1, 0.2 * inch))

        story.append(Paragraph("Detailed Results:", styles['h2']))
        story.append(Spacer(1, 0.1 * inch))

        # Add each question's result as bullet points
        for result in self.quiz_history:
            region = result['region']
            correct = result['correct']
            result_text = (f"Region: {region},"
                           f" Your Answer was "
                           f"{'Correct' if correct else 'Incorrect'}")
            p = Paragraph(result_text, styles['Bullet'])
            story.append(p)

        doc.build(story)
        messagebox.showinfo("Export Successful",
                            f"Quiz results exported to {filename}")


# Run the quiz app
if __name__ == '__main__':
    root = tk.Tk()
    quiz = AotearoaQuiz(root)
    root.mainloop()
