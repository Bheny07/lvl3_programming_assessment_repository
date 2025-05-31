"""02_questions_03 adds a function to display a question based on the
selected region."""

# Import tkinter for GUI and PIL for image handling
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk


# Class to display NZ map, region buttons, and quiz interface
class AotearoaQuiz(object):
    def __init__(self, roots):
        # Initialize main window
        self.current_maori_names = None
        self.root = roots
        self.root.title("Aotearoa Names Quiz")

        # Dictionary: English region names to Māori names
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

        # Store buttons to access them later if needed
        self.region_buttons = {}

        # Load NZ map image and configure window size
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

        # Initialize score counters
        self.correct_answers = 0
        self.incorrect_answers = 0

        # Frame for score display
        self.score_frame = tk.Frame(self.root)
        self.score_frame.pack(fill=tk.X)

        # Canvas to display the NZ map
        self.map_canvas = tk.Canvas(roots, width=self.nz_image.width,
                                    height=self.nz_image.height)
        self.map_canvas.create_image(0, 0, image=self.nz_photo,
                                     anchor=tk.NW)
        self.map_canvas.pack()

        # Load and place logo image
        try:
            self.logo_image = Image.open("HenyDice Logo Trans.png")
            self.logo_photo = ImageTk.PhotoImage(self.logo_image)
            self.logo_label = tk.Label(self.root, image=self.logo_photo)
            self.logo_label.place(relx=1.0, rely=1.0, x=-10, anchor='se')

        except FileNotFoundError:
            messagebox.showwarning("Warning",
                                   "Logo image not found!")

        # Create buttons for each region on the map
        self.create_region_buttons_on_map()

        # Frame for question, answer input, and submit button
        self.question_frame = tk.Frame(self.root)
        self.question_frame.pack(pady=10)

        self.question_label = tk.Label(self.question_frame, text="",
                                       font=("Arial", 16))
        self.question_label.pack()

        self.answer_entry = tk.Entry(self.question_frame, font=("Arial", 14))
        self.answer_entry.pack(pady=5)

        self.submit_button = tk.Button(self.question_frame,
                                       text="Submit Answer",
                                       font=("Arial", 14))
        self.submit_button.pack(pady=10)
        self.submit_button.config(state=tk.DISABLED)  # Disabled initially

        # Labels for correct and incorrect answer counts
        self.correct_label = tk.Label(self.score_frame,
                                      text=f"Correct: {self.correct_answers}",
                                      font=("Arial", 10))
        self.correct_label.pack(side=tk.LEFT, padx=10, pady=5)

        separator = tk.Label(self.score_frame, text=" | ", font=("Arial", 10))
        separator.pack(side=tk.LEFT)

        self.incorrect_label = tk.Label(self.score_frame,
                                        text=f"Incorrect: "
                                             f"{self.incorrect_answers}",
                                        font=("Arial", 10))
        self.incorrect_label.pack(side=tk.LEFT)

    # Update score labels when answer is submitted
    def update_score(self, correct=True):
        if correct:
            self.correct_answers += 1
            self.correct_label.config(text=f"Correct: "
                                           f"{self.correct_answers}")
        else:
            self.incorrect_answers += 1
            self.incorrect_label.config(text=f"Incorrect: "
                                             f"{self.incorrect_answers}")

    # Create and place buttons for each region
    def create_region_buttons_on_map(self):
        button_config = {"width": 10, "height": 1, "font": ("Arial", 8)}

        # Positions approximate locations on the map image
        self.create_map_button("Northland",
                               240, 80, **button_config)
        self.create_map_button("Auckland",
                               265, 115, **button_config)
        self.create_map_button("Waikato",
                               270, 150, **button_config)
        self.create_map_button("Bay of Plenty",
                               400, 115, **button_config)
        self.create_map_button("Gisborne",
                               450, 165, **button_config)
        self.create_map_button("Hawke's Bay",
                               420, 210, **button_config)
        self.create_map_button("Taranaki",
                               260, 185, **button_config)
        self.create_map_button("Manawatu",
                               400, 240, **button_config)
        self.create_map_button("Wellington",
                               380, 270, **button_config)
        self.create_map_button("Marlborough",
                               220, 230, **button_config)
        self.create_map_button("West Coast",
                               190, 280, **button_config)
        self.create_map_button("Canterbury",
                               325, 310, **button_config)
        self.create_map_button("Otago",
                               280, 380, **button_config)
        self.create_map_button("Southland",
                               125, 340, **button_config)

    # Create individual button with command bound to show_question
    def create_map_button(self, region_name, x, y, **kwargs):
        button = tk.Button(self.root, text=region_name, **kwargs,
                           command=lambda r=region_name: self.show_question(r))
        button.place(x=x - kwargs.get("width", 8) * 6, y=y, anchor=tk.CENTER)
        self.region_buttons[region_name] = button

    # Display the question for the selected region
    def show_question(self, region):
        self.current_maori_names = self.regions[region]  # Store for later use
        question_text = f"What is the Māori name for {region}?"
        self.question_label.config(text=question_text)
        self.submit_button.config(state=tk.NORMAL)
        self.answer_entry.delete(0, tk.END)


# Main program execution
if __name__ == '__main__':
    root = tk.Tk()
    quiz = AotearoaQuiz(root)
    root.mainloop()
