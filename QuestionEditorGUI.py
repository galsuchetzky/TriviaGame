import re
import os

from Utils import write_json, read_json
from tkinter import *
from os import listdir
from Strings import *
from Question import Question

QUESTIONS_LOCATION = 'questions\\'

ENCODING = 'UTF-8'

WINDOW_HEIGHT = 1600

WINDOW_WIDTH = 450

FILE_FORMAT_REGEX = r'((.+\r\n){5}[0-3]\r\n\r\n)+'


def is_int(string):
    """
    Check if a given string is an integer.
    :param string: The string to check.
    :return: True iff the given string is an integer.
    """
    try:
        int(string)
        return True
    except ValueError:
        return False


class QuestionEditorGui:
    def __init__(self, caller_root, update_option_menu):
        self.update_option_menu = update_option_menu
        self.caller_root = caller_root
        self.questions = None
        self.current_question_index = 0
        self.file_loaded = False
        self.questions_file = None
        self.new_file_gui_root = None

        # Create root and root frame
        self.question_editor_root = Tk()
        self.question_editor_root.resizable(width=False, height=False)
        self.question_editor_root.title(TITLE)
        self.question_editor_root.protocol("WM_DELETE_WINDOW", self.reveal_caller_and_quit)
        self.hide_caller()

        self.root_frame = Frame(self.question_editor_root, height=WINDOW_HEIGHT // 4,
                                width=WINDOW_WIDTH)
        self.root_frame.pack()
        self.root_frame.pack_propagate(0)

        self.files_var, self.file_optionmenu, self.toolbar_frame, self.total_questions_number, \
        self.current_question_number_entry, self.questions_var, self.questions_optionmenu = \
            self.create_toolbar(self.root_frame)

        self.question_entry, self.answers_entries, self.correct_answer_var, \
            = self.create_editor(self.root_frame)

        self.create_buttons(self.root_frame)

        self.feedback_label = self.create_feedback(self.root_frame)

        self.question_editor_root.mainloop()

    def create_toolbar(self, root_frame):
        """
        Creates the tool bar.
        :param root_frame: The root_frame.
        :returns: members that needs to be updated further in the program.
        """
        toolbar_frame = Frame(root_frame)
        toolbar_frame.pack(expand=False, fill=X, anchor=N)
        toolbar_frame.pack_propagate(0)
        toolbar_frame.rowconfigure(0, weight=4)
        toolbar_frame.columnconfigure(0, weight=1)

        # Create the choose question file label
        choose_question_file_label = Label(toolbar_frame, text=QUESTION_FILE_LABEL)
        choose_question_file_label.grid(column=5)

        # Creates the option menu for the types of questions available
        question_files = [file_name.replace('.json', '') for file_name in listdir(QUESTIONS_LOCATION)
                          if file_name.endswith('.json')]
        files_var = StringVar(toolbar_frame)
        if question_files:
            files_var.set(question_files[0])
        else:
            question_files = [[]]

        # Creates the question file option menu
        questions_file_option_menu = OptionMenu(toolbar_frame, files_var, *question_files)
        questions_file_option_menu.grid(column=4, row=0, padx=10, sticky=E)

        # Creates the load button
        load_button = Button(toolbar_frame, text=LOAD_BUTTON_TEXT,
                             command=lambda: self.load_question_file(files_var.get()))
        load_button.grid(row=0, column=3, sticky=E)

        # Creates the question number label
        question_number_label = Label(toolbar_frame, text=QUESTION_NUMBER_LABEL_TEXT)
        question_number_label.grid(row=0, column=2, sticky=E, padx=5)

        # Creates the total question number label
        total_questions_number = Label(toolbar_frame, text="/0")
        total_questions_number.grid(row=0, column=1, sticky=E)

        # Creates the current_question_number entry
        current_question_number_entry = Entry(toolbar_frame, width=3)
        current_question_number_entry.grid(row=0, column=0, sticky=E)
        current_question_number_entry.insert(0, 0)
        current_question_number_entry.bind(ENTER_KEY, lambda e: self.load_question(
            question_index=current_question_number_entry.get()))

        # Creates the option menu for the questions available
        questions_var = StringVar(toolbar_frame)
        questions_optionmenu = OptionMenu(toolbar_frame, questions_var, [])
        questions_optionmenu.configure(state=DISABLED)
        questions_optionmenu.grid(row=1, column=0, columnspan=6, sticky=W + E)

        return files_var, questions_file_option_menu, toolbar_frame, total_questions_number, \
               current_question_number_entry, questions_var, questions_optionmenu

    def create_editor(self, root_frame):
        """
        Configure the editor.
        :param root_frame: The root_frame.
        """
        # Configure the editor frame.
        editor_frame = Frame(root_frame)
        editor_frame.pack(expand=False, fill=X, anchor=N)
        editor_frame.columnconfigure(1, weight=1)

        # Configure question label.
        question_label = Label(editor_frame, text=QUESTION_LABEL)
        question_label.grid(row=0, column=2, pady=10)

        # Configure question entry.
        question_entry = Entry(editor_frame, justify=RIGHT)
        question_entry.grid(row=0, column=1, sticky=W + E, padx=(5, 10))

        # Configure answers labels.
        answers_labels = []
        for i in range(4):
            answers_labels.append(Label(editor_frame, text=":" + "תשובה " + str(i + 1)))
            answers_labels[i].grid(row=i + 1, column=2, pady=10)

        # Configure answers entries.
        answers_entries = []
        for i in range(4):
            answers_entries.append(Entry(editor_frame, justify=RIGHT))
            answers_entries[i].grid(row=i + 1, column=1, pady=10, sticky=W + E, padx=(5, 10))

        # Configure The correct answer radiobuttons
        correct_answer_var = IntVar(editor_frame, value=0)
        correct_answer_radiobutton = []
        for i in range(4):
            radio_button = Radiobutton(editor_frame,
                                       variable=correct_answer_var, value=i,
                                       command=self.mark_correct_answer)
            correct_answer_radiobutton.append(radio_button)
            radio_button.grid(row=i + 1, column=0, padx=(10, 0))

        return question_entry, answers_entries, correct_answer_var

    def create_buttons(self, root_frame):
        """
        Configure the buttons frame.
        :param root_frame: The root_frame
        """
        button_frame = Frame(root_frame)
        button_frame.pack(expand=True, fill=X, anchor=N)

        # Configure column weights for expending the columns evenly.
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)
        button_frame.columnconfigure(2, weight=1)
        button_frame.columnconfigure(3, weight=1)
        button_frame.columnconfigure(4, weight=1)

        # Create next button.
        next_button = Button(button_frame, text=NEXT_BUTTON_TEXT,
                             command=lambda: self.load_question())
        next_button.grid(column=0, row=0, sticky=W + E, padx=5)

        # Create update button.
        update_button = Button(button_frame, text=UPDATE_BUTTON_TEXT,
                               command=lambda: self.update())
        update_button.grid(column=1, row=0, sticky=W + E, padx=5)

        # Create save_new button.
        save_new_button = Button(button_frame, text=SAVE_NEW_BUTTON_TEXT,
                                 command=lambda: self.save_new())
        save_new_button.grid(column=2, row=0, sticky=W + E, padx=5)

        # Create clear button.
        clear_button = Button(button_frame, text=CLEAR_BUTTON_TEXT,
                              command=lambda: self.clear_fields())
        clear_button.grid(column=3, row=0, sticky=W + E, padx=5)

        # Create previous button.
        prev_button = Button(button_frame, text=PREVIOUS_BUTTON_TEXT,
                             command=lambda: self.load_question(load_next=False))
        prev_button.grid(column=4, row=0, sticky=W + E, padx=5)

        # Create delete question button
        delete_question_button = Button(button_frame, text=DELETE_QUESTION_BUTTON_TEXT,
                                        command=self.delete_question)
        delete_question_button.grid(column=1, row=1, sticky=W + E, pady=5, padx=5)

        # Create new file button
        new_file_button = Button(button_frame, text=NEW_FILE_BUTTON_TEXT,
                                 command=self.create_new_file)
        new_file_button.grid(row=1, column=2, sticky=W + E, pady=5, padx=5)

        # Create the exit button
        exit_button = Button(button_frame, text=EXIT_BUTTON_TEXT,
                             command=self.reveal_caller_and_quit)
        exit_button.grid(row=2, column=2, sticky=W + E, padx=5)

    def create_feedback(self, root_frame):
        """
        Creates the feedback frame.
        :param root_frame: The root_frame.
        :return: Objects that might be updated.
        """
        feedback_frame = Frame(root_frame)
        feedback_frame.pack(expand=True, fill=X, anchor=N)
        feedback_frame.columnconfigure(0, weight=1)

        feedback_label = Label(feedback_frame, relief=SUNKEN)
        feedback_label.grid(row=0, column=0, sticky=W + E)

        return feedback_label

    def load_question_file(self, questions_file):
        """
        Loads the selected question file.
        If the selected file is empty, returns.
        :param questions_file: The name of the questions file.
        """
        questions_path = QUESTIONS_LOCATION + questions_file + '.json'
        if not os.path.isfile(questions_path):
            self.update_feedback(INVALID_FILE_STRUCTURE_FEEDBACK, FEEDBACK_ERROR_COLOR)
            return
        self.questions_file = questions_file  # Save the name of the current question file.
        questions_dict = read_json(questions_path)
        self.questions = [Question(question) for question in questions_dict.values()]

        self.total_questions_number['text'] = '/' + str(len(self.questions))
        self.questions_optionmenu.configure(state=ACTIVE if self.questions else DISABLED)

        self.current_question_index = 0
        self.file_loaded = True
        self.load_question(init=True)  # Loads the first question
        self.update_question_options()
        if self.questions:
            self.update_feedback(FILE_LOADED_SUCCESSFULLY_FEEDBACK, FEEDBACK_SUCCESS_COLOR)
        else:
            self.update_feedback(EMPTY_FILE_FEEDBACK, FEEDBACK_NOTIFY_COLOR)

    def load_question(self, question_index=None, init=False, load_next=True, new=False):
        """
        Loads a question to the editor.
        :param init:            True iff the question is the first from a loaded file.
        :param load_next:       True if the next question is to be loaded, False if the Previous
                                question is to be loaded.
        :param new:             True iff the loaded question is a new question that was added.
        :param question_index:  An index of a question to jump to, jump only if not None.
        """

        # In case the question file is empty
        if not self.questions:
            self.update_feedback(EMPTY_FILE_FEEDBACK, FEEDBACK_NOTIFY_COLOR)
            self.clear_fields()
            self.current_question_number_entry.delete(0, END)
            self.current_question_number_entry.insert(0, 0)
            return

        # Get question index.
        if question_index is not None:
            # If an index was given but is invalid, returns
            if is_int(question_index) and 0 < int(question_index) <= len(self.questions):
                self.current_question_index = int(question_index) - 1
            else:
                self.update_feedback(INVALID_QUESTION_INDEX_FEEDBACK, FEEDBACK_ERROR_COLOR)
                return
        else:
            if not self.file_loaded:  # Makes sure that a question file was indeed loaded.
                return

            if not init and not new:  # If not next or prev, don't changes the question's index.
                advance = 1
                if not load_next:
                    advance = -1

                self.current_question_index = (self.current_question_index + advance) % len(
                    self.questions)

        self.current_question_index %= len(self.questions)
        self.current_question_number_entry.delete(0, END)
        self.current_question_number_entry.insert(0, self.current_question_index + 1)

        self.clear_fields()  # Clears the fields for a new question to be loaded.

        # Loads the question.
        self.question_entry.insert(0, self.questions[self.current_question_index]["question"])

        # Loads the answers.
        for i in range(4):
            ans = self.questions[self.current_question_index]['ans' + str(i)]
            ans = ans if ans != '_' else ''
            self.answers_entries[i].insert(0, ans)

        # Load the correct answer
        self.correct_answer_var.set(
            self.questions[self.current_question_index]['correct'])
        self.mark_correct_answer()

        # Update the question optionmenu
        self.questions_var.set(self.questions[self.current_question_index]['question'])
        self.update_feedback(QUESTION_LOADED_SUCCESSFULLY_FEEDBACK, FEEDBACK_SUCCESS_COLOR)

    def delete_question(self):
        """
        Deletes the currently edited question question.
        """
        if not self.questions:
            self.update_feedback(NOTHING_TO_DELETE_FEEDBACK, FEEDBACK_ERROR_COLOR)
            return

        to_delete = self.questions[self.current_question_index]
        self.questions.remove(to_delete)
        self.regenerate_file()
        self.load_question(init=True)  # Init = True for keeping the index the same.
        self.update_question_options()
        self.total_questions_number['text'] = '/' + str(len(self.questions))
        self.update_feedback(QUESTION_DELETED_SUCCESSFULLY_FEEDBACK, FEEDBACK_SUCCESS_COLOR)

    def check_valid(self):
        """
        Checks that all the entries corresponds to a valid question.
        :return: True iff the question is valid.
        """
        # Check that the question is not empty, replace empty answers with '_', make sure that the
        # correct answer is not an empty answer and make sure that at least one answer is not empty

        # Check that the question is not empty
        if not self.question_entry.get():
            return False

        # Check that the correct answer is not an empty answer.
        # Make sure that at least one answer is not empty.
        if self.answers_entries[self.correct_answer_var.get()].get() == '':
            self.update_feedback(INVALID_CORRECT_ANSWER_FEEDBACK, FEEDBACK_ERROR_COLOR)
            return False

        return True

    def update(self):
        """
        Updates the currently edited to the current fields.
        """
        if not self.check_valid():  # Check that the question is valid.
            self.update_feedback(UPDATE_FAILED_FEEDBACK, FEEDBACK_ERROR_COLOR)
            return

        if not self.questions:
            self.update_feedback(NO_QUESTION_TO_UPDATE_FEEDBACK, FEEDBACK_ERROR_COLOR)
            return

        # Extracts the answers from the editor, replacing empty fields with "_".
        answers = []
        for i in range(4):
            if self.answers_entries[i].get():
                answers.append(self.answers_entries[i].get())
            else:
                answers.append(EMPTY_ANSWER)

        # Update the question.
        question = self.questions[self.current_question_index]
        question['question'] = self.question_entry.get()

        # Update the answers.
        for i in range(4):
            question['ans' + str(i)] = answers[i]

        # Update the correct answer
        question['correct'] = self.correct_answer_var.get()

        self.regenerate_file()
        self.update_question_options()
        self.mark_correct_answer()
        self.update_feedback(UPDATED_SUCCESSFULLY_FEEDBACK, FEEDBACK_SUCCESS_COLOR)

    def update_file_options(self):
        """
        Updates the files option menu to the file's list after adding a new file.
        """
        # Gets the files names.
        question_files = [file_name.replace('.json', '') for file_name in listdir(QUESTIONS_LOCATION) if
                          file_name.endswith('.json')]
        self.questions_file = question_files[0] if question_files else ''
        if not question_files:  # The option menu requires something to display. if there are no files to display,
            # display nothing.
            question_files = ['']

        # Recreates the question file option menu
        self.file_optionmenu.grid_remove()
        self.file_optionmenu = OptionMenu(self.toolbar_frame, self.files_var, *question_files)
        self.file_optionmenu.grid(column=4, row=0, padx=10, sticky=E)
        self.files_var.set(self.questions_file)

    def update_question_options(self):
        """
        Updates the questions option menu to the question's list after updating a question's name.
        """

        # If the question file is empty, defines the question list as an empty dictionary.
        if not self.questions:
            questions = {}
        else:
            # Gets the questions.
            questions = {str(question['index'] + 1) + ". " + question['question']:
                             question['index'] + 1 for question in self.questions}

        # Recreates the question file option menu
        self.questions_optionmenu.grid_remove()
        self.questions_optionmenu = OptionMenu(self.toolbar_frame, self.questions_var,
                                               *questions.keys() if questions.keys() else [''],
                                               command=lambda e: self.load_question(
                                                   question_index=questions[
                                                       self.questions_var.get()]))

        self.questions_var.set(self.question_entry.get())

        # If the question file is empty, disables it.
        if not self.questions:
            self.questions_optionmenu.configure(state=DISABLED)

        self.questions_optionmenu.grid(row=1, column=0, columnspan=6, sticky=W + E)

    def update_feedback(self, text, color):
        self.feedback_label['text'] = text
        self.feedback_label['fg'] = color

    def save_new(self):
        """
        Creates a new question from the editor.
        """
        if not self.check_valid():  # If not valid, returns.
            self.update_feedback(SAVE_FORMAT_ERROR, FEEDBACK_ERROR_COLOR)
            return

        if self.questions is None:  # If no file is yet loaded.
            self.update_feedback(FILE_NOT_LOADED_FEEDBACK, FEEDBACK_ERROR_COLOR)
            return

        # Updates the current question's index to the last question.
        self.current_question_index = len(self.questions)

        # Generates the question's text format, creates a new Question objects ans adds it to the
        # questions list
        question_format = self.get_edited_question_format()
        question = Question(question_format)
        self.questions.append(question)

        self.total_questions_number['text'] = '/' + str(len(self.questions))

        self.regenerate_file()
        self.update_question_options()

        self.load_question(new=True)
        self.update_feedback(QUESTION_SAVED_SUCCESSFULLY_FEEDBACK, FEEDBACK_SUCCESS_COLOR)

    def get_edited_question_format(self):
        """
        Generates a valid question's format (valid for the Question object) from the editor.
        :return: The generated question format.
        """
        # Create question dict
        question = {
            'index': self.current_question_index,
            'question': self.question_entry.get(),
            'correct': self.correct_answer_var.get()
        }

        # Add answers to question dict.
        for i in range(4):
            ans = self.answers_entries[i].get()
            ans = ans if ans else EMPTY_ANSWER
            question['ans' + str(i)] = ans

        return question

    def regenerate_file(self):
        """
        Regenerates the current file, where the newly generated file contains all the questions
        currently loaded to the system.
        """
        questions = {'question_' + str(question['index']): question.question_dict for question in self.questions}
        write_json(questions, QUESTIONS_LOCATION + self.questions_file + '.json')

    def clear_fields(self):
        """
        Clears all the editor's fields.
        """
        # Clear the question's entry.
        self.question_entry.delete(0, END)

        # Clear the answer's entries.
        for i in range(4):
            self.answers_entries[i].delete(0, END)

        # Reset the correct answer's radiobutton.
        self.correct_answer_var.set(0)

    def mark_correct_answer(self):
        for entry in self.answers_entries:
            entry['bg'] = 'white'
        self.answers_entries[self.correct_answer_var.get()]['bg'] = CORRECT_ANSWER_COLOR

    def create_new_file(self):
        """
        Creates a new file.
        """

        def create(new_file_name):
            if os.path.isfile(new_file_name):
                self.update_feedback(FAILED_TO_CREATE_FILE_FEEDBACK, FEEDBACK_SUCCESS_COLOR)

            # Create a file with the given name.
            write_json({}, QUESTIONS_LOCATION + new_file_name + '.json')
            # f = open(QUESTIONS_LOCATION + new_file_name, 'w')
            # f.close()

            self.load_question_file(new_file_name)
            self.update_file_options()
            self.update_feedback(FILE_CREATED_SUCCESSFULLY_FEEDBACK, FEEDBACK_SUCCESS_COLOR)
            self.new_file_gui_root = None

        def window_terminated():
            """
            Called when file name request window is terminated without creating a new file.
            """
            self.new_file_gui_root.destroy()
            self.new_file_gui_root = None

        self.new_file_gui_root = Tk()
        self.new_file_gui_root.protocol("WM_DELETE_WINDOW", window_terminated)

        NewFileGui(create, window_terminated, self.new_file_gui_root)

    def hide_caller(self):
        self.caller_root.withdraw()

    def reveal_caller_and_quit(self):
        self.question_editor_root.destroy()
        self.caller_root.deiconify()
        if self.new_file_gui_root is not None:
            self.new_file_gui_root.destroy()
        self.update_option_menu()


class NewFileGui:
    """Gui for getting a file's name on new file creation."""

    def __init__(self, create, windows_terminated, root):
        self.file_name_request_root = root
        self.create = create
        self.window_terminated = windows_terminated

        file_name_label = Label(self.file_name_request_root, text=NEW_FILE_NAME_LABEL)
        file_name_label.grid(row=0, column=0, padx=10, pady=10)

        self.file_name_entry = Entry(self.file_name_request_root, justify=RIGHT)
        self.file_name_entry.bind('<Return>', lambda e: self.finish())
        self.file_name_entry.grid(row=1, column=0, padx=10, pady=5)

        create_file_button = Button(self.file_name_request_root, text=CREATE_FILE_BUTTON_TEXT,
                                    command=self.finish)
        create_file_button.grid(row=2, column=0, padx=10, pady=10)

        self.file_name_request_root.mainloop()

    def finish(self):
        name = self.file_name_entry.get()
        self.file_name_request_root.destroy()
        self.create(name)


if __name__ == '__main__':
    r = QuestionEditorGui(Tk(), print)
