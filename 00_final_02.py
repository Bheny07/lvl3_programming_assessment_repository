"""03_questions will display and end screen for user. It will let the user
know the percentage of correct answers. It will also contain an export results
button, play again button and a close button. In this version, 03_04, will
add a close button for the user to close the quiz"""

# Import tkinter and PIL
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch


# Class to display map and region buttons
class AotearoaQuiz(object):
    def __init__(self, roots):
        self.last_user_answer = None
        self.root = roots
        self.root.title("Aotearoa Names Quiz")

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

        self.region_buttons = {}
        self.original_button_colors = {}
        self.current_region = None
        self.correct_answer = None
        self.answer_buttons = []
        self.answered_regions = set()
        self.current_options = []
        self.quiz_history = []

        try:
            self.nz_image = Image.open("Background Colour Trans.png")
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

        self.correct_answers = 0
        self.incorrect_answers = 0
        self.total_questions = len(self.regions)

        # Create a frame for the score counter
        self.score_frame = tk.Frame(self.root)
        self.score_frame.pack(fill=tk.X)

        self.map_canvas = tk.Canvas(roots, width=self.nz_image.width,
                                    height=self.nz_image.height)
        self.map_canvas.create_image(0, 0, image=self.nz_photo,
                                     anchor=tk.NW)
        self.map_canvas.pack()

        # Frame to hold questions, enter answer and submit answers
        self.question_frame = tk.Frame(self.root)
        self.question_frame.pack(pady=10)

        self.question_label = tk.Label(self.question_frame, text="",
                                       font=("Arial", 16))
        self.question_label.pack()

        # Frame to hold the answer buttons
        self.options_frame = tk.Frame(self.question_frame)
        self.options_frame.pack()

        self.close_button_frame = tk.Frame(self.question_frame)
        self.options_frame.pack()

        self.close_button_frame = tk.Frame(self.question_frame)
        self.close_button_frame.pack(pady=5)

        self.close_button = tk.Button(self.close_button_frame,
                                      text="Close Question",
                                      font=("Arial", 13), bg="red",
                                      fg="white",
                                      command=self.close_current_question)
        self.close_button.pack()
        self.close_button.pack_forget()

        # Label to display correct answers
        self.correct_label = tk.Label(self.score_frame,
                                      text=f"Correct: {self.correct_answers}",
                                      font=("Arial", 10))
        self.correct_label.pack(side=tk.LEFT, padx=10, pady=5)

        # Separator
        separator = tk.Label(self.score_frame, text=" | ", font=("Arial", 10))
        separator.pack(side=tk.LEFT)

        # Label to display incorrect answers
        self.incorrect_label = tk.Label(
            self.score_frame, text=f"Incorrect: {self.incorrect_answers}",
            font=("Arial", 10))
        self.incorrect_label.pack(side=tk.LEFT)

        # Load the logo image
        try:
            self.logo_image = Image.open(
                "HenyDice Logo Trans.png")
            self.logo_photo = ImageTk.PhotoImage(self.logo_image)
            self.logo_label = tk.Label(self.root, image=self.logo_photo)
            self.logo_label.place(relx=1.0, rely=1.0, x=-10, anchor='se')

        except FileNotFoundError:
            messagebox.showwarning("Warning",
                                   "Logo image not found!")

        self.create_region_buttons_on_map()

        self.end_screen = None

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

    # Function to update the score counter
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
            self.incorrect_answers += 1
            messagebox.showerror(
                message=f"That was not the correct answer for "
                        f"{self.current_region}. The correct "
                        f"answer was {self.correct_answer}",
                title="Incorrect!")
            self.incorrect_label.config(
                text=f"Incorrect: {self.incorrect_answers}")

    # Function to put region buttons on the map
    def create_region_buttons_on_map(self):
        button_configuration = {"width": 10, "height": 1, "font": ("Arial", 8)}
        button_colors = {
            "Northland": 'tan1',
            "Auckland": 'lightgreen',
            "Waikato": 'gold1',
            "Bay of Plenty": 'royalblue1',
            "Gisborne": 'tan1',
            "Hawke's Bay": 'lightgreen',
            "Taranaki": 'royalblue1',
            "Manawatu": 'mediumpurple1',
            "Wellington": 'gold1',
            "Marlborough": 'lightgreen',
            "West Coast": 'gold1',
            "Canterbury": 'royalblue1',
            "Otago": 'lightgreen',
            "Southland": 'tan1'
        }

        # Approximate button positions relative to the image
        self.create_map_button("Northland", 240, 80,
                               **button_configuration,
                               bg=button_colors["Northland"])
        self.create_map_button("Auckland", 265, 115,
                               **button_configuration,
                               bg=button_colors["Auckland"])
        self.create_map_button("Waikato", 270, 150,
                               **button_configuration,
                               bg=button_colors["Waikato"])
        self.create_map_button("Bay of Plenty", 400, 115,
                               **button_configuration,
                               bg=button_colors["Bay of Plenty"])
        self.create_map_button("Gisborne", 450, 165,
                               **button_configuration,
                               bg=button_colors["Gisborne"])
        self.create_map_button("Hawke's Bay", 420, 210,
                               **button_configuration,
                               bg=button_colors["Hawke's Bay"])
        self.create_map_button("Taranaki", 260, 185,
                               **button_configuration,
                               bg=button_colors["Taranaki"])
        self.create_map_button("Manawatu", 405, 240,
                               **button_configuration,
                               bg=button_colors["Manawatu"])
        self.create_map_button("Wellington", 380, 270,
                               **button_configuration,
                               bg=button_colors["Wellington"])
        self.create_map_button("Marlborough", 220, 230,
                               **button_configuration,
                               bg=button_colors["Marlborough"])
        self.create_map_button("West Coast", 190, 280,
                               **button_configuration,
                               bg=button_colors["West Coast"])
        self.create_map_button("Canterbury", 330, 310,
                               **button_configuration,
                               bg=button_colors["Canterbury"])
        self.create_map_button("Otago", 280, 380,
                               **button_configuration,
                               bg=button_colors["Otago"])
        self.create_map_button("Southland", 125, 340,
                               **button_configuration,
                               bg=button_colors["Southland"])

    # Function to create buttons for different regions
    def create_map_button(self, region_name, x, y, **kwargs):
        button = tk.Button(self.root, text=region_name, **kwargs,
                           command=lambda r=region_name:
                           self.show_question(r))
        button.place(x=x - kwargs.get("width", 8) * 6, y=y, anchor=tk.CENTER)
        self.region_buttons[region_name] = button
        self.original_button_colors[region_name] = kwargs.get(
            'bg')  # Store original color

    def _handle_answer_selection(self, user_answer):
        self.check_answer(user_answer)

    def show_question(self, region):
        self.current_region = region
        correct_maori_names = self.regions[region]
        self.correct_answer = random.choice(correct_maori_names)
        incorrect_options = set()
        all_maori_names = [name for sublist in self.regions.values() for name
                           in sublist]

        while len(incorrect_options) < 2:
            wrong_answer = random.choice(all_maori_names)
            if wrong_answer not in correct_maori_names:
                incorrect_options.add(wrong_answer)

        options = list(incorrect_options) + [self.correct_answer]
        random.shuffle(options)

        question_text = f"What is the Maori name for {region}?"
        self.question_label.config(text=question_text)

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

        for name, button in self.region_buttons.items():
            button.config(state=tk.DISABLED)

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

            for name, button in self.region_buttons.items():
                if name not in self.answered_regions:
                    button.config(state=tk.NORMAL)

            self.current_region = None
            self.correct_answer = None
            self.close_button.pack_forget()

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

            close_button = tk.Button(self.end_screen, text="Close Quiz",
                                     font=("Arial", 10), bg='red',
                                     fg='white', command=self.close_end_screen)
            close_button.pack(pady=5)

        else:
            for widget in self.end_screen.winfo_children():
                if isinstance(widget, tk.Label):
                    widget.config(text=final_score_message)
            self.end_screen.lift()

    def reset_quiz(self):
        self.correct_answers = 0
        self.incorrect_answers = 0
        self.answered_regions = set()
        self.quiz_history = []
        self.correct_label.config(text=f"Correct: {self.correct_answers}")
        self.incorrect_label.config(
            text=f"Incorrect: {self.incorrect_answers}")

        for name, button in self.region_buttons.items():
            original_color = self.original_button_colors.get(name)
            if original_color:
                button.config(state=tk.NORMAL, bg=original_color)

        if self.end_screen:
            self.end_screen.destroy()
            self.end_screen = None

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

    def close_end_screen(self):
        if self.end_screen:
            self.end_screen.destroy()
            self.end_screen = None
        self.root.destroy()


# Main Loop
if __name__ == '__main__':
    root = tk.Tk()
    quiz = AotearoaQuiz(root)
    root.mainloop()
