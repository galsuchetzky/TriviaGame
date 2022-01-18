from tkinter import *

PLAY_AGAIN_BUTTON_TEXT = "שחק שוב"

CLOSE_BUTTON_TEXT = "סגור"

SUCCESS_RATE_LABEL_TEXT = "אחוז הצלחה: "

CORRECT_ANSWERS_LABEL_TEXT = "מספר תשובות נכונות: "

GAME_TIME_LABEL_TEXT = "זמן משחק: "


class ResultsGui:
    def __init__(self, time_played, correct_answers, wrong_answers, play):
        self.root = Tk()
        # Initiates the values to present
        self.time_played = time_played
        self.correct_answers = correct_answers
        self.correctness_percentage = (correct_answers * 100) // (wrong_answers + correct_answers)

        # Initiates the labels
        self.time_played_label = Label(self.root, text=GAME_TIME_LABEL_TEXT + self.time_played)
        self.correct_answers_label = Label(self.root, text=CORRECT_ANSWERS_LABEL_TEXT + str(
            correct_answers) + "/" + str(correct_answers + wrong_answers))
        self.success_rate_label = Label(self.root, text=SUCCESS_RATE_LABEL_TEXT + str(
            self.correctness_percentage) + "%")

        # Grids the labels into the root
        self.time_played_label.grid(row=0, columnspan=2, pady=10, padx=10)
        self.correct_answers_label.grid(row=1, columnspan=2, pady=10, padx=10)
        self.success_rate_label.grid(row=2, columnspan=2, pady=10, padx=10)

        # Create the close button
        self.close_button = Button(self.root, text=CLOSE_BUTTON_TEXT, command=self.root.destroy)
        self.close_button.grid(row=3, column=0, pady=10, padx=10)

        # Create the play again button
        self.play_again = Button(self.root, text=PLAY_AGAIN_BUTTON_TEXT,
                                 command=lambda: play(self.root))
        self.play_again.grid(row=3, column=1, pady=10, padx=10)
