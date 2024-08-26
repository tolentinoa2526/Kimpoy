import random
from tkinter import *


class NumberGenerator:

    def __init__(self):
        # Initialise variables (such as the feedback variable)
        self.var_feedback = StringVar()
        self.var_feedback.set("")

        self.var_has_error = StringVar()
        self.var_has_error.set("no")

        self.all_generations = []

        # Set up GUI Frame
        self.num_frame = Frame(padx=10, pady=10)
        self.num_frame.grid()

        self.num_heading = Label(self.num_frame,
                                 text="Random Number Generator",
                                 font=("Arial", "16", "bold")
                                 )
        self.num_heading.grid(row=0)

        instructions = "Press 'Start' to generate random numbers between 1 and 10. Press 'Stop' to stop the generation."
        self.num_instruction = Label(self.num_frame,
                                     text=instructions,
                                     wrap=250, width=40,
                                     justify="left")
        self.num_instruction.grid(row=1)

        self.num_result_error = Label(self.num_frame, text="",
                                      fg="#004C00", font=("Arial", "14"))
        self.num_result_error.grid(row=2)

        self.num_entry = Entry(self.num_frame,
                               font=("Arial", "14")
                               )
        self.num_entry.grid(row=2, padx=10, pady=10)

        error = "Please enter a number"
        self.num_result_error = Label(self.num_frame, text="",
                                      fg="#9c0000")
        self.num_result_error.grid(row=3)

        # Generate and stop buttons
        self.button_frame = Frame(self.num_frame)
        self.button_frame.grid(row=3)

        self.start_button = Button(self.button_frame,
                                   text="Start",
                                   bg="#009900",
                                   fg="#FFFFFF",
                                   font=("Arial", "12", "bold"), width=15,
                                   command=self.start_generating)
        self.start_button.grid(row=0, column=0, padx=5, pady=5)

        self.stop_button = Button(self.button_frame,
                                  text="Stop",
                                  bg="#CC0000",
                                  fg="#FFFFFF",
                                  font=("Arial", "12", "bold"), width=15,
                                  command=self.stop_generating,
                                  state=DISABLED)
        self.stop_button.grid(row=0, column=1, padx=5, pady=5)

        self.generating = False

    def generate_number(self):
        random_number = random.randint(1, 10)
        self.var_feedback.set(f"Random number: {random_number}")
        self.var_has_error.set("no")
        self.all_generations.append(self.var_feedback.get())

        # Set the generated number to the entry widget
        self.num_entry.delete(0, END)
        self.num_entry.insert(0, str(random_number))

        self.output_result()

        if self.generating:
            self.num_frame.after(100, self.generate_number)  # Continue generating after 1 second

    def output_result(self):
        output = self.var_feedback.get()
        has_error = self.var_has_error.get()

        if has_error == "yes":
            self.num_result_error.config(fg="#9C0000")
        else:
            self.num_result_error.config(fg="#004C00")

        self.num_result_error.config(text=output)

    def start_generating(self):
        self.generating = True
        self.start_button.config(state=DISABLED)
        self.stop_button.config(state=NORMAL)
        self.generate_number()

    def stop_generating(self):
        self.generating = False
        self.start_button.config(state=NORMAL)
        self.stop_button.config(state=DISABLED)


if __name__ == "__main__":
    root = Tk()
    root.title("Random Number Generator")
    NumberGenerator()
    root.mainloop()
