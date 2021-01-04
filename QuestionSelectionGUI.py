from tkinter import *
from os import listdir
from QuestionEditorGUI import QuestionEditorGui

INVALID_CAP_AMOUNT_FEEDBACK = '.מספר שאלות לא תקין'

GAME_CAP_LABEL_TEXT = ':מספר שאלות'

EDITOR_BUTTON_TEXT = 'עורך שאלונים'

EMPTY_FILE_FEEDBACK = ".קובץ שאלות ריק"

QUESTIONS_FILE_NOT_SELECTED_FEEDBACK = '.אנא בחר קובץ שאלות'

START_GAME_LABEL = "התחל שאלון"

QUESTIONS_LOCATION = 'questions\\'

CHOOSE_QUESTIONS_LABEL = ':בחר נושא'

WINDOW_HEIGHT = 200

WINDOW_WIDTH = 350

FILE_FORMAT_REGEX = r'((.+\r\n){5}[0-3]\r\n\r\n)+'

ENCODING = 'UTF-8'

INVALID_FILE_STRUCTURE_FEEDBACK = ".קובץ שאלות לא תקין"

FEEDBACK_ERROR_COLOR = 'red'

DEFAULT_GAME_CAP = 10


# todo add instructions (maybe in a new window).
# todo add game cap selector.
# todo update the files list after using the editor (added files do not appear)

class QuestionSelectionGui:
    """
    Creates a window where you can choose the questions file.
    """

    def __init__(self, start_trivia_callback):
        self.start_trivia_callback = start_trivia_callback

        self.choose_questions_root = Tk()
        self.choose_questions_root.resizable(width=False, height=False)
        self.choose_questions_root.pack_propagate(0)

        root_frame = Frame(self.choose_questions_root, height=WINDOW_HEIGHT, width=WINDOW_WIDTH)
        root_frame.pack(expand=True, fill=BOTH)

        self.file_var, self.game_cap_entry, self.questions_option_menu, self.conf_frame \
            = self.create_configuration_frame(root_frame)

        self.create_buttons(root_frame)

        self.feedback_label = self.create_feedback(root_frame)

        self.choose_questions_root.mainloop()

    def create_configuration_frame(self, root_frame):
        conf_frame = Frame(root_frame)
        conf_frame.pack(fill=X, expand=True)
        conf_frame.columnconfigure(0, weight=1)

        # Create choose question file label
        choose_questions_label = Label(conf_frame, text=CHOOSE_QUESTIONS_LABEL)
        choose_questions_label.grid(row=0, column=1, sticky=E)

        # Creates the option menu for the types of questions available
        file_var = StringVar(conf_frame)
        question_files = listdir(QUESTIONS_LOCATION)
        question_files = question_files if question_files else [[]]

        questions_option_menu = OptionMenu(conf_frame, file_var, *question_files)
        questions_option_menu.grid(row=0, column=0, sticky=E + W, padx=5)

        # Create game cap label
        game_cap_label = Label(conf_frame, text=GAME_CAP_LABEL_TEXT)
        game_cap_label.grid(row=1, column=1, sticky=E)

        # Create game cap entry
        game_cap_entry = Entry(conf_frame, width=3)
        game_cap_entry.grid(row=1, column=0, sticky=E, padx=5)
        game_cap_entry.insert(0, DEFAULT_GAME_CAP)

        return file_var, game_cap_entry, questions_option_menu, conf_frame

    def create_buttons(self, root_frame):
        button_frame = Frame(root_frame)
        button_frame.pack(fill=BOTH, expand=True)
        button_frame.columnconfigure(0, weight=1)

        # Creates the editor button.
        open_editor_button = Button(button_frame, text=EDITOR_BUTTON_TEXT, command=self.open_editor)
        open_editor_button.grid(row=0, column=0, pady=10, padx=10, sticky=W + E)

        # Creates the start button.
        start_trivia_button = Button(button_frame, text=START_GAME_LABEL,
                                     command=lambda: self.start_trivia(QUESTIONS_LOCATION,
                                                                       self.file_var.get(),
                                                                       self.game_cap_entry.get()))
        start_trivia_button.grid(row=1, column=0, pady=10, padx=10, sticky=W + E)

    def create_feedback(self, root_frame):
        """
        Creates the feedback frame.
        :param root_frame: The root_frame.
        :return: Objects that might be updated.
        """
        feedback_frame = Frame(root_frame)
        feedback_frame.pack(fill=X)
        feedback_frame.columnconfigure(0, weight=1)

        feedback_label = Label(feedback_frame, relief=SUNKEN)
        feedback_label.grid(row=0, column=0, sticky=W + E, pady=(0, 10), padx=10)

        return feedback_label

    def start_trivia(self, questions_location, file_name, game_cap):
        # Check that the game_cap is positive.
        try:
            print(game_cap)
            if int(game_cap) <= 0:
                self.update_feedback(INVALID_CAP_AMOUNT_FEEDBACK, FEEDBACK_ERROR_COLOR)
                return
        except:
            self.update_feedback(INVALID_CAP_AMOUNT_FEEDBACK, FEEDBACK_ERROR_COLOR)
            return

        # Check that the file is not empty and if of a correct format.
        if not self.file_var.get():
            self.update_feedback(QUESTIONS_FILE_NOT_SELECTED_FEEDBACK, FEEDBACK_ERROR_COLOR)
            return
        with open(QUESTIONS_LOCATION + file_name, 'rb') as qf:
            lines = [s.decode(ENCODING) for s in qf.readlines()]
            if not lines:
                self.update_feedback(EMPTY_FILE_FEEDBACK, FEEDBACK_ERROR_COLOR)
                return
            else:
                file_content = ''.join(lines)
                # print(file_content)
                valid_format = re.sub(FILE_FORMAT_REGEX, '', file_content) == ''
                if not valid_format:
                    self.update_feedback(INVALID_FILE_STRUCTURE_FEEDBACK, FEEDBACK_ERROR_COLOR)
                    return

        self.choose_questions_root.destroy()
        self.start_trivia_callback(questions_location, file_name, int(game_cap))

    def open_editor(self):
        QuestionEditorGui(self.choose_questions_root, self.update_file_options)

    def update_feedback(self, text, color):
        self.feedback_label['text'] = text
        self.feedback_label['fg'] = color

    def update_file_options(self):
        self.questions_option_menu.grid_remove()
        question_files = listdir(QUESTIONS_LOCATION)
        question_files = question_files if question_files else [[]]
        self.questions_option_menu = OptionMenu(self.conf_frame, self.file_var, *question_files)
        self.questions_option_menu.grid(row=0, column=0, sticky=E + W, padx=5)



if __name__ == '__main__':
    q = QuestionSelectionGui(print)
