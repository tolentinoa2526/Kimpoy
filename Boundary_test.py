from tkinter import *


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

        instructions = "This is a tests about Movie Quotes, " \
                       "where ypu pick a movie that belongs to the " \
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
        self.button_frame.grid(row=4)

        self.convert_button = Button(self.button_frame,
                                     text="Enter",
                                     bg="#0096FF",
                                     fg=button_fg,
                                     font=button_font, width=12,
                                     command=self.convert)
        self.convert_button.grid(row=0, column=0, padx=5, pady=5)

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


# Main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Boundary Testing")
    Converter()
    root.mainloop()
