from tkinter import *
from functools import partial  # to prevent unwanted windows
import csv
import random
import re


class Converter:
    def __init__(self, root):
        self.root = root  # Use the root window passed in the main routine
        self.root.title("Movie Quiz")

        self.var_feedback = StringVar()
        self.var_feedback.set("")

        self.var_has_error = StringVar()
        self.var_has_error.set("no")

        self.all_calculations = []

        # Common format for all butto ns
        self.button_font = ("Arial",  "12", "bold")
        self.button_fg = "#FFFFFF"
        self.button_width = 12  # Consistent width for all buttons

        # Set up GUI Frame
        self.boundary_frame = Frame(self.root, padx=10, pady=10)
        self.boundary_frame.grid()

        self.boundary_heading = Label(self.boundary_frame,
                                      text="Choose User Rounds",
                                      font=("Arial", "16", "bold"))
        self.boundary_heading.grid(row=0)

        instructions = "This is a test about Movie Quotes, " \
                       "where you pick a movie that belongs to the " \
                       "character."
        self.boundary_instruction = Label(self.boundary_frame,
                                          text=instructions,
                                          wrap=250,
                                          width=40,
                                          justify="left")
        self.boundary_instruction.grid(row=1)

        self.boundary_entry = Entry(self.boundary_frame,
                                    font=("Arial", "14"))
        self.boundary_entry.grid(row=2, padx=10, pady=10)

        self.boundary_result_error = Label(self.boundary_frame, text="",
                                           fg="#9c0000")
        self.boundary_result_error.grid(row=3)

        # Button frame
        self.button_frame = Frame(self.boundary_frame)
        self.button_frame.grid(row=4, pady=10)

        self.convert_button = Button(self.button_frame,
                                     text="Enter",
                                     bg="#0096FF",
                                     fg=self.button_fg,
                                     font=self.button_font, width=self.button_width,
                                     command=self.convert)
        self.convert_button.pack(side=LEFT, padx=10)

        # Help button in the main GUI
        self.help_button = Button(self.button_frame,
                                  text="Help",
                                  command=partial(self.show_help),
                                  font=self.button_font,
                                  bg="#FF5733", fg=self.button_fg, width=self.button_width)
        self.help_button.pack(side=LEFT, padx=10)

    def check_boundary(self):
        has_error = "no"
        error = "Please enter a whole number between 1 and 10."

        # Check that user has entered a valid whole number
        response = self.boundary_entry.get()

        try:
            # Check if the response is an integer and within the range
            response = int(response)

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

        # Disable the "Enter" button after clicking once
        self.convert_button.config(state=DISABLED)

        # If the response is valid, launch the Play class
        if status == "valid":
            self.load_quotes()
            self.to_play(int(response))

    # Rest of the class methods...

    def load_quotes(self):
        self.all_quotes = []
        with open("movie_quotes.csv", "r") as file:
            reader = csv.reader(file, delimiter=",")
            next(reader)  # skip the header
            for row in reader:
                quote = row[0]
                answer = re.sub(r'\s*\(\d{4}\)$', '', row[1])  # Remove the year
                self.all_quotes.append([quote, answer])

    def to_play(self, num_rounds):
        self.play_window = Play(self.root, num_rounds, self.all_quotes, self.var_feedback, self.all_calculations)
        self.root.withdraw()

    def output_answer(self):
        output = self.var_feedback.get()
        has_error = self.var_has_error.get()

        if has_error == "yes":
            self.boundary_result_error.config(fg="#9C0000")
            self.boundary_entry.config(bg="#F8CECC")
        else:
            self.boundary_result_error.config(fg="#004C00")
            self.boundary_entry.config(bg="#FFFFFF")

        self.boundary_result_error.config(text=output)

    def show_help(self):
        DisplayHelp(self)


class Play:
    def __init__(self, root, how_many, quotes, var_feedback, all_calculations):
        self.root = root  # Store the root window reference
        self.how_many = how_many
        self.all_quotes = quotes
        self.var_feedback = var_feedback
        self.all_calculations = all_calculations

        self.play_box = Toplevel()
        self.play_box.title("Movie Quiz")
        self.play_box.geometry(f"+100+100")

        self.user_scores = []
        self.computer_scores = []

        self.quest_frame = Frame(self.play_box, padx=10, pady=10)
        self.quest_frame.grid()

        self.current_round = 1
        self.correct_answers = 0
        self.quiz_completed = False

        random.shuffle(self.all_quotes)
        self.display_question()

    def display_question(self):
        if self.current_round > self.how_many or self.current_round > len(self.all_quotes):
            self.quiz_completed = True
            self.show_statistics()
            return

        quote, answer = self.all_quotes[self.current_round - 1]

        quiz_heading = Label(self.quest_frame,
                             text=f"Movie Quotes Quiz - Round {self.current_round}/{self.how_many}",
                             font=("Arial", "16", "bold"))
        quiz_heading.grid(row=0, columnspan=3, pady=10)

        # UPDATED: Wrap text in the quiz question label
        self.quiz_question = Label(self.quest_frame,
                                   text=quote,
                                   font=("Arial", "14"),
                                   wraplength=300,
                                   justify="left")
        self.quiz_question.grid(row=1, columnspan=3, pady=10)

        options = [answer]
        while len(options) < 3:
            random_quote = random.choice(self.all_quotes)[1]
            if random_quote not in options:
                options.append(random_quote)

        random.shuffle(options)

        self.var_option = StringVar()
        self.answer_buttons = []

        max_option_length = max(len(option) for option in options)
        button_width = min(max(20, max_option_length + 5), 30)

        self.next_button = Button(self.quest_frame,
                                  text="Next",
                                  command=self.next_question,
                                  font=("Arial", "12", "bold"),
                                  bg="#4CAF50",
                                  fg="#FFFFFF",
                                  width=12,
                                  state=DISABLED)
        self.next_button.grid(row=5, columnspan=3, pady=10)

        for i, option in enumerate(options):
            answer_button = Button(self.quest_frame,
                                   text=option,
                                   font=("Arial", "12", "bold"),
                                   bg="#0096FF",
                                   fg="#FFFFFF",
                                   width=button_width,
                                   wraplength=200,
                                   justify="left")
            answer_button.config(command=lambda opt=option, btn=answer_button: self.check_answers(opt, btn))
            answer_button.grid(row=i + 2, column=0, columnspan=3, pady=5)
            self.answer_buttons.append(answer_button)

        self.feedback_label = Label(self.quest_frame,
                                    text="",
                                    font=("Arial", "12"))
        self.feedback_label.grid(row=6, columnspan=3, pady=10)

        self.control_buttons_frame = Frame(self.quest_frame)
        self.control_buttons_frame.grid(row=7, columnspan=3, pady=10)

        self.help_button = Button(self.control_buttons_frame,
                                  text="Help",
                                  command=self.show_help,
                                  font=("Arial", "12", "bold"),
                                  bg="#FF5733",
                                  fg="#FFFFFF",
                                  width=12)
        self.help_button.pack(side=LEFT, padx=10)

        self.play_again_button = Button(self.control_buttons_frame,
                                        text="Play Again",
                                        command=self.play_again,
                                        font=("Arial", "12", "bold"),
                                        bg="#0096FF",
                                        fg="#FFFFFF",
                                        width=12)
        self.play_again_button.pack(side=LEFT, padx=10)

    def check_answers(self, user_answer, answer_button):
        if self.quiz_completed:
            return

        quote, correct_answer = self.all_quotes[self.current_round - 1]

        # Determine the color for correct and incorrect answers
        correct_color = "#004C00"  # Green
        incorrect_color = "#9C0000"  # Red

        if user_answer == correct_answer:
            self.correct_answers += 1
            self.feedback_label.config(text="Correct!", fg=correct_color)
            # Change the color of the correct answer button to green
            answer_button.config(bg=correct_color)
        else:
            self.feedback_label.config(text=f"Incorrect! The correct answer was: {correct_answer}", fg=incorrect_color)
            # Change the color of the selected button to red
            answer_button.config(bg=incorrect_color)
            # Change the color of the correct answer button to green
            for button in self.answer_buttons:
                if button.cget("text") == correct_answer:
                    button.config(bg=correct_color)

        # Disable answer buttons after a selection is made
        for button in self.answer_buttons:
            button.config(state=DISABLED)

        # Enable the Next button
        self.next_button.config(state=NORMAL)

    def next_question(self):
        self.current_round += 1
        for widget in self.quest_frame.winfo_children():
            widget.destroy()
        self.display_question()

    def show_statistics(self):
        self.quiz_completed = True
        self.var_feedback.set(f"Quiz Complete!\nYou answered {self.correct_answers} out of {self.how_many} correctly.")

        # Display the statistics directly in the current window
        for widget in self.quest_frame.winfo_children():
            widget.destroy()

        stats_label = Label(self.quest_frame,
                            text=self.var_feedback.get(),
                            font=("Arial", "14"),
                            justify=LEFT)
        stats_label.grid(row=0, column=0, padx=10, pady=10)

        # Play Again button to restart the quiz
        play_again_button = Button(self.quest_frame,
                                   text="Start Over",
                                   command=self.play_again,
                                   font=("Arial", "12", "bold"),
                                   bg="#0096FF",
                                   fg="#FFFFFF",
                                   width=12)
        play_again_button.grid(row=1, column=0, pady=10)

    def play_again(self):
        self.play_box.destroy()  # Close the Play window
        self.root.deiconify()  # Show the main window again

        # Clear the content of the main window to prevent stacking
        for widget in self.root.winfo_children():
            widget.destroy()

        # Restart the Converter class without creating multiple instances
        Converter(self.root)

    def show_help(self):
        DisplayHelp(self)


class DisplayHelp:

    def __init__(self, partner):
        # setup dialogue box and bg colour
        background = "#ffe6cc"
        self.help_box = Toplevel()

        # disable help button
        partner.help_button.config(state=DISABLED)

        # if users press cross at top, close help and release help button
        self.help_box.protocol('WM_DELETE_WINDOW', partial(self.close_help, partner))

        # Create the background frame and configure it to expand
        self.help_frame = Frame(self.help_box, bg=background)
        self.help_frame.pack(fill="both", expand=True)

        self.help_heading_label = Label(self.help_frame,
                                        bg=background,
                                        text="Help / Info",
                                        font=("Arial", "14", "bold"))
        self.help_heading_label.pack(pady=(10, 5))

        help_text = "Welcome to the Movie Quotes Quiz!\n\n" \
                    "1. Enter the number of rounds (1-10) you want to play.\n" \
                    "2. Click 'Enter' to start the quiz.\n" \
                    "3. For each round, select the correct movie for the given quote.\n" \
                    "4. Click 'Next' to proceed to the next question.\n" \
                    "5. Your score will be displayed at the end of the quiz.\n" \
                    "6. Click 'Play Again' to play the quiz again.\n\n" \
                    "Good luck and have fun!"
        self.help_text_label = Label(self.help_frame,
                                     bg=background,
                                     text=help_text,
                                     wraplength=350,
                                     justify="left")
        self.help_text_label.pack(pady=(5, 10), padx=10, anchor="center")

        self.dismiss_button = Button(self.help_frame,
                                     font=("Arial", "12", "bold"),
                                     text="Dismiss",
                                     bg="#CC6600", fg="#FFFFFF",
                                     command=partial(self.close_help, partner))
        self.dismiss_button.pack(pady=(5, 10))

    # closes help dialogue
    def close_help(self, partner):
        # put help button back to normal...
        partner.help_button.config(state=NORMAL)
        self.help_box.destroy()


# Main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Movie Quiz")
    Converter(root)
    root.mainloop()
