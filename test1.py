from tkinter import *
import csv
import random
import re


class Converter:

    def __init__(self):
        # Initialise variables (such as the feedback variable)
        self.var_feedback = StringVar()
        self.var_feedback.set("")

        self.var_has_error = StringVar()
        self.var_has_error.set("no")

        self.all_calculations = []

        # Common format for all buttons
        button_font = ("Arial", "12", "bold")
        button_fg = "#FFFFFF"

        # Set up GUI Frame
        self.boundary_frame = Frame(padx=10, pady=10)
        self.boundary_frame.grid()

        self.boundary_heading = Label(self.boundary_frame,
                                      text="Choose User Rounds",
                                      font=("Arial", "16", "bold")
                                      )
        self.boundary_heading.grid(row=0)

        instructions = "This is a test about Movie Quotes, " \
                       "where you pick a movie that belongs to the " \
                       "character."
        self.boundary_instruction = Label(self.boundary_frame,
                                          text=instructions,
                                          wrap=250, width=40,
                                          justify="left")
        self.boundary_instruction.grid(row=1)

        self.boundary_entry = Entry(self.boundary_frame,
                                    font=("Arial", "14")
                                    )
        self.boundary_entry.grid(row=2, padx=10, pady=10)

        self.boundary_result_error = Label(self.boundary_frame, text="",
                                           fg="#9c0000")
        self.boundary_result_error.grid(row=3)

        # Conversion button
        self.button_frame = Frame(self.boundary_frame)
        self.button_frame.grid(row=4, pady=10)

        self.convert_button = Button(self.button_frame,
                                     text="Enter",
                                     bg="#0096FF",
                                     fg=button_fg,
                                     font=button_font, width=12,
                                     command=self.convert)
        self.convert_button.pack(side=LEFT, padx=10)

        # Help button
        self.help_button = Button(self.button_frame,
                                  text="Help",
                                  bg="#FF5733",
                                  fg=button_fg,
                                  font=button_font, width=12,
                                  command=self.show_help)
        self.help_button.pack(side=LEFT, padx=10)

        # Initialize variables for quiz
        self.quiz_window = None
        self.current_round = 0
        self.total_rounds = 0
        self.correct_answers = 0
        self.quiz_completed = False

    def check_boundary(self):

        has_error = "no"
        error = "Please enter a number between 1 and 10."

        # Check that user has entered a valid number
        response = self.boundary_entry.get()

        try:
            response = float(response)

            if response < 1 or response > 10:
                has_error = "yes"

        except ValueError:
            has_error = "yes"

        # Sets var_has_error so that entry box and labels can be correctly formatted
        if has_error == "yes":
            self.var_has_error.set("yes")
            self.var_feedback.set(error)
            return "invalid", None

        # If we have no errors...
        else:
            self.var_has_error.set("no")
            return "valid", response

    @staticmethod
    def round_ans(val):
        return "{:.0f}".format(round(val))

    def convert(self):
        status, response = self.check_boundary()
        if status == "invalid":
            self.output_answer()
            return

        response = self.round_ans(response)
        feedback = "Entered value: {}".format(response)
        self.var_feedback.set(feedback)
        self.all_calculations.append(feedback)
        print(self.all_calculations)

        self.output_answer()

        # Disable the "Submit" button after clicking once
        self.convert_button.config(state=DISABLED)

        # If the response is valid, launch the quiz GUI
        if status == "valid":
            self.load_quotes()
            self.launch_quiz(int(response))

    def load_quotes(self):
        self.all_quotes = []
        with open("movie_quotes.csv", "r") as file:
            reader = csv.reader(file, delimiter=",")
            next(reader)  # skip the header
            for row in reader:
                quote = row[0]
                answer = re.sub(r'\s*\(\d{4}\)$', '', row[1])  # Remove the year in parentheses
                self.all_quotes.append([quote, answer])

    def launch_quiz(self, rounds):
        self.current_round = 1
        self.total_rounds = rounds
        self.correct_answers = 0
        self.quiz_completed = False
        self.display_question()

    def display_question(self):
        if self.quiz_window:
            self.quiz_window.destroy()

        self.quiz_window = Toplevel()
        self.quiz_window.title("Movie Quotes Quiz")

        quiz_heading = Label(self.quiz_window,
                             text=f"Movie Quotes Quiz - Round {self.current_round}/{self.total_rounds}",
                             font=("Arial", "16", "bold"))
        quiz_heading.grid(row=0, columnspan=3, pady=10)

        if self.current_round <= self.total_rounds and self.current_round <= len(self.all_quotes):
            quote, answer = self.all_quotes[self.current_round - 1]

            self.quiz_question = Label(self.quiz_window, text=quote, font=("Arial", "14"))
            self.quiz_question.grid(row=1, columnspan=3, pady=10)

            # Generate three options including the correct answer
            options = [answer]
            while len(options) < 3:
                random_quote = random.choice(self.all_quotes)[1]
                if random_quote not in options:
                    options.append(random_quote)

            random.shuffle(options)

            self.var_option = StringVar()

            # Find the maximum length of options to set button width
            max_option_length = max(len(option) for option in options)
            button_width = min(max(20, max_option_length + 5), 30)  # Minimum width 20 characters, maximum 30

            for i, option in enumerate(options):
                answer_button = Button(self.quiz_window, text=option, command=lambda opt=option: self.check_answers(opt),
                                       font=("Arial", "12", "bold"), bg="#0096FF", fg="#FFFFFF", width=button_width)
                answer_button.grid(row=2, column=i, padx=5, pady=5)

            button_frame = Frame(self.quiz_window)
            button_frame.grid(row=3, columnspan=3, pady=20)

            next_button = Button(button_frame, text="Next", command=self.next_question, font=("Arial", "12", "bold"),
                                 bg="#0096FF", fg="#FFFFFF")
            next_button.pack(side=LEFT, padx=10)

            self.correct_answer = answer
        else:
            self.quiz_window.destroy()
            self.quiz_completed = True
            result_window = Toplevel()
            result_window.title("Quiz Completed")

            result_label = Label(result_window,
                                 text=f"Congratulations! You've completed the quiz. Correct answers: {self.correct_answers}/{self.total_rounds}",
                                 font=("Arial", "14"))
            result_label.pack(pady=10)

            play_again_button = Button(result_window, text="Play Again",
                                       command=lambda: self.play_again(result_window),
                                       font=("Arial", "12", "bold"),
                                       bg="#0096FF", fg="#FFFFFF")
            play_again_button.pack(pady=10)

    def check_answers(self, answer):
        correct_answer = self.correct_answer.strip().lower()
        if answer.strip().lower() == correct_answer:
            self.correct_answers += 1
            feedback = "Correct!"
        else:
            feedback = f"Wrong. The correct answer was '{self.correct_answer}'."

        feedback_label = Label(self.quiz_window, text=feedback, font=("Arial", "12"),
                               fg="red" if answer.strip().lower() != correct_answer else "green")
        feedback_label.grid(row=4, columnspan=3, pady=10)

    def next_question(self):
        self.current_round += 1
        self.display_question()

    def play_again(self, result_window):
        result_window.destroy()
        self.boundary_entry.delete(0, END)
        self.quiz_completed = False
        self.convert_button.config(state=NORMAL)
        self.var_feedback.set("")
        self.var_has_error.set("no")
        self.all_calculations = []
        self.correct_answers = 0

    def output_answer(self):
        output = self.var_feedback.get()
        has_error = self.var_has_error.get()

        if has_error == "yes":
            # Red text, pink entry box
            self.boundary_result_error.config(fg="#9C0000")
            self.boundary_entry.config(bg="#F8CECC")
        else:
            self.boundary_result_error.config(fg="#004C00")
            self.boundary_entry.config(bg="#FFFFFF")

        self.boundary_result_error.config(text=output)

    def show_help(self):
        self.help_button.config(state=DISABLED)  # Disable help button when pressed
        help_window = Toplevel()
        help_window.title("Help")

        help_text = "Welcome to the Movie Quotes Quiz!\n\n" \
                    "1. Enter the number of rounds (1-10) you want to play.\n" \
                    "2. Click 'Enter' to start the quiz.\n" \
                    "3. For each round, select the correct movie for the given quote.\n" \
                    "4. Click 'Next' to proceed to the next question.\n" \
                    "5. Your score will be displayed at the end of the quiz.\n" \
                    "6. Click 'Play Again' to play the quiz again.\n\n" \
                    "Good luck and have fun!"

        help_label = Label(help_window, text=help_text, font=("Arial", "12"), justify=LEFT)
        help_label.pack(padx=10, pady=10)

        dismiss_button = Button(help_window, text="Dismiss", command=lambda: self.close_help(help_window),
                                font=("Arial", "12", "bold"), bg="#FF5733", fg="#FFFFFF")
        dismiss_button.pack(pady=10)

    def close_help(self, help_window):
        help_window.destroy()
        self.help_button.config(state=NORMAL)  # Re-enable help button when help window is closed


# Main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Movie Quiz")
    Converter()
    root.mainloop()
