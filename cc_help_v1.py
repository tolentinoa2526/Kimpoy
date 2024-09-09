from tkinter import *
from functools import partial  # To prevent unwanted windows


# users choose 3, 5 or 10 rounds
class ChooseRounds:

    def __init__(self):
        # invoke play class with three rounds for testing purposes.
        self.to_play(3)

    def to_play(self, num_rounds):
        Play(num_rounds)

        # Hide root window (ie: hide rounds choice window).
        root.withdraw()


class Play:

    def __init__(self, how_many):

        self.play_box = Toplevel()

        self.quest_frame = Frame(self.play_box, padx=10, pady=10)
        self.quest_frame.grid()

        self.control_frame = Frame(self.quest_frame)
        self.control_frame.grid(row=6)

        control_buttons = [
            ["#CC6600", "Help", "get help"]
        ]

        # list to hold references for control buttons
        # so that the text of the 'start over' button
        # can easily be configured when the game is over
        self.control_button_ref = []

        for item in range(0, 1):
            self.make_control_button = Button(self.control_frame,
                                              fg="#FFFFFF",
                                              bg=control_buttons[item][0],
                                              text=control_buttons[item][1],
                                              width=11, font=("Arial", "12", "bold"),
                                              command=lambda i=item: self.to_do(control_buttons[i][2]))
            self.make_control_button.grid(row=0, column=item, padx=5, pady=5)

            # Add buttons to control list
            self.control_button_ref.append(self.make_control_button)

            self.to_help_btn = self.control_button_ref[0]

    def to_do(self, action):
        if action == "get help":
            DisplayHelp(self)
        else:
            self.close_play()

    # close the application
    def close_play(self):
        root.destroy()


# shows users help / game tips
class DisplayHelp:

    def __init__(self, partner):

        # setup dialogue box and background colour
        background = "#ffe6cc"
        self.help_box = Toplevel()

        # disable help button
        partner.to_help_btn.config(state=DISABLED)

        # If user press cross at top, close help and
        # 'release' help button
        self.help_box.protocol('WM_DELETE_WINDOW',
                               partial(self.close_help, partner))

        self.help_frame = Frame(self.help_box, width=350,
                                height=200,
                                bg=background)
        self.help_frame.grid()

        self.help_heading_label = Label(self.help_frame,
                                        bg=background,
                                        text="Help / Info",
                                        font=("Arial", "14", "bold"))
        self.help_heading_label.grid(row=0)

        help_text = "Welcome to the Movie Quotes Quiz!\n\n" \
                    "1. Enter the number of rounds (1-10) you want to play.\n" \
                    "2. Click 'Enter' to start the quiz.\n" \
                    "3. For each round, select the correct movie for the given quote.\n" \
                    "4. Click 'Next' to proceed to the next question.\n" \
                    "5. Your score will be displayed at the end of the quiz.\n" \
                    "6. Click 'Play Again' to play the quiz again.\n\n" \
                    "Good luck and have fun!"

        self.help_text_label = Label(self.help_frame, bg=background,
                                     text=help_text, wraplength=350,
                                     justify="left")
        self.help_text_label.grid(row=1, padx=10)

        self.dismiss_button = Button(self.help_frame,
                                     font=("Arial", "12", "bold"),
                                     text="Dismiss", bg="#CC6600",
                                     fg="#FFFFFF",
                                     command=partial(self.close_help,
                                                     partner))
        self.dismiss_button.grid(row=2, padx=10, pady=10)

    # close help dialogue (used by button and x at top of dialogue)
    def close_help(self, partner):
        # put help button back to normal...

        partner.to_help_btn.config(state=NORMAL)
        self.help_box.destroy()


# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Movie Quiz")
    ChooseRounds()
    root.mainloop()
