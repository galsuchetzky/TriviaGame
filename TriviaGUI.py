from tkinter import *

QUESTION_NUMBER_TEXT = "מספר שאלה:"

PLAY_TIME_TEXT = "זמן משחק: "

SCORE_TEXT = "ניקוד: "


class TriviaGui:
    def __init__(self, get_question, game_cap, end_game):
        """
        Initiates all the variables needed for the game.
        :param get_question: function to get the next question
        :param game_cap: The number of questions to ask.
        :param end_game: Function to end the game.
        """
        self.get_question = get_question
        self.game_cap = game_cap
        self.end_game = end_game
        self.respond = False  # To eliminate clicks while presenting the correct answer.
        self.questionText = ""  # The question to display.
        self.answersText = ['', '', '', '']  # The possible 4 answers to the question.
        self.correct_answer = 0  # The number of the correct answer.
        # The number in the questions list of the question that is currently being displayed.
        self.curr_question_num = -1
        self.questions = []  # A list to load the questions to from the triviaQuestions file.
        self.questions_to_load = None
        self.score = 0  # The current score.
        self.score_text = SCORE_TEXT + str(self.score)  # The score label text.
        self.time_played = "00:00:00"  # The total time played.
        self.questions_asked = 0  # The number of questions that were asked till now.

        # Creates in the init all the needed variables for later use.
        self.root, self.answer_buttons, self.score_label, self.timer_label, self.question_label, \
        self.question_number_label = [None] * 6

        self.root, self.answer_buttons, self.score_label, self.question_number_label, \
        self.timer_label, self.question_label = self.create_gui()

        self._time_job = None

        self.change_question()

        self.update_time_played()  # Starts the timer

        self.root.mainloop()

    def create_gui(self):
        """
        Creates the game's gui.
        :return: All the objects created that are needed for modifications later.
        """
        # The following lines configures the game's window.
        window_height = 600
        window_width = 400

        # The main frame, is set to default size.
        root = Tk()
        root.resizable(width=False, height=False)

        # Creates a frame for the score and other stats.
        score_frame = Frame(root, bg='grey93')
        score_frame.grid(row=0, sticky=W + E)

        # Creates a frame for the question.
        question_frame = Frame(root, bg='black', height=window_height // 4, width=window_width)
        question_frame.pack_propagate(
            0)  # Prevents the frame from shrinking to fit the label's size.
        question_frame.grid(row=1)

        # Creates a frame for the answers.
        answer_frame = Frame(root, bg='yellow', height=window_height - window_height // 4,
                             width=window_width)
        answer_frame.grid(row=2, sticky=W + E)

        # Creates the score's label
        score_label = Label(score_frame, text=self.score_text)
        score_label.grid(column=0, row=0)

        # Creates the timer's label
        timer_label = Label(score_frame, text=PLAY_TIME_TEXT + self.time_played)
        timer_label.grid(column=1, row=0)

        # Creates the question number label
        question_number_label = Label(score_frame, text=QUESTION_NUMBER_TEXT + str(
            self.questions_asked) + '/' + str(self.game_cap))
        question_number_label.grid(column=2, row=0)

        score_frame.columnconfigure(0, weight=4)
        score_frame.columnconfigure(1, weight=4)
        score_frame.columnconfigure(2, weight=4)

        # Creates the question's label.
        question_label = Label(question_frame, bg='skyblue')
        question_label.pack(fill=BOTH, expand=YES, padx=4, pady=4)

        # Creates the answer's buttons.
        button_height = 5
        answer_buttons = []
        for i in range(4):
            answer_buttons.append(
                Button(answer_frame, height=button_height,
                       command=lambda k=i: self.check_answer(k)))
            answer_buttons[i].pack(fill=X, expand=YES)

        return root, answer_buttons, score_label, question_number_label, timer_label, question_label

    def check_answer(self, ans_num):
        """
        Checks the player's answer, displays the correct answer in green (and the wrong one if chosen in red),
        then changes the current question to the next one.
        :param ans_num: The player's answer.
        """
        if self.answer_buttons[ans_num]['text'] == "_":
            return

        if self.respond:
            return

        self.respond = True

        self.answer_buttons[self.correct_answer]['bg'] = 'green'
        if ans_num == self.correct_answer:
            self.score += 1
            self.score_text = SCORE_TEXT + str(self.score)
            self.score_label['text'] = self.score_text
        if ans_num != self.correct_answer:
            self.answer_buttons[ans_num]['bg'] = 'red'

        # If the game has reached it's cap, end it.
        if self.questions_asked == self.game_cap:
            self.root.after_cancel(self._time_job)
            self.root.after(1000, self.finish)
            return

        # Waits 1 second and changes the question.
        self.root.after(1000, self.change_question)

    def finish(self):
        """
        For finishing the game.
        """
        self.end_game(self.root, self.score, self.time_played)

    def update_time_played(self):
        """
        Updates the game's timer time.
        """
        self.time_played = list(map(lambda x: int(x), self.time_played.split(':')))
        self.time_played[2] = (self.time_played[2] + 1) % 60
        if self.time_played[2] == 0:
            self.time_played[1] = (self.time_played[1] + 1) % 60

        if self.time_played[1] == 0 and self.time_played[2] == 0:
            self.time_played[0] = (self.time_played[0] + 1) % 24

        self.time_played = ':'.join(list(map(lambda x: '0' + str(x) if len(str(x)) == 1 else str(x),
                                             self.time_played)))
        self.timer_label['text'] = PLAY_TIME_TEXT + self.time_played
        self._time_job = self.root.after(1000, self.update_time_played)

    def change_question(self):
        """
        Loads the next question to the system.
        """
        self.questions_asked += 1
        question = self.get_question()

        self.questionText = question.get_question()  # Loads the question.
        self.correct_answer = question.get_correct_answer()  # Loads the correct answer's number.

        # Loads the possible answers.
        for i in range(4):
            self.answersText[i] = question.get_answer(i)

            # Displays the next question and it's possible answers.
            self.question_label["text"] = self.questionText
            for i in range(4):
                self.answer_buttons[i]['text'] = self.answersText[i]

        self.display_question()

    def display_question(self):
        """
        Displays the next question on the screen.
        """
        self.respond = False

        self.question_number_label['text'] = str(self.questions_asked) + '/' + str(self.game_cap)
        for i in range(4):  # Resets the colors of the buttons.
            self.answer_buttons[i]['bg'] = 'grey93'

        # Displays the next question and it's possible answers.
        self.question_label["text"] = self.questionText
        for i in range(4):
            self.answer_buttons[i]['text'] = self.answersText[i]
