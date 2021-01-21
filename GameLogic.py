import random

from QuestionSelectionGUI import QuestionSelectionGui
from Question import Question
from TriviaGUI import TriviaGui
from ResultsGUI import ResultsGui
from Utils import read_json, write_json


# todo extract all the Tk objects here and send them to the constructor.

class GameLogic:
    """
    Runs the logic of the game: enables to choose the questions file, then play and then shows
    the questions asked along with their correct answers.
    """

    def __init__(self):
        self.game_cap = None
        self.questions = []  # List for the questions
        QuestionSelectionGui(self.create_question_list)

    def create_question_list(self, questions_loc, file_name, game_cap):
        """
        Destroys the questions selection gui and loads the questions.
        :param questions_loc: The path of the chosen question file's directory.
        :param file_name: The name of the chosen questions file.
        """
        if not file_name:
            return
        self.game_cap = game_cap
        questions_path = questions_loc + file_name + '.json'
        questions_dict = read_json(questions_path)
        self.questions = [Question(question) for question in questions_dict.values()]

        self.run_game()

    def run_game(self):
        TriviaGui(self.get_question, self.game_cap, self.end_game)

    def get_question(self):
        return self.questions[random.randint(0, len(self.questions) - 1)]

    def end_game(self, game_root, score, time_played):
        game_root.destroy()
        self.show_results(time_played, score, self.game_cap - score)

    def show_results(self, time_played, correct_answers, wrong_answers):
        ResultsGui(time_played, correct_answers, wrong_answers, play)


def play(res_root=None):
    if res_root:
        res_root.destroy()
    GameLogic()


if __name__ == '__main__':
    play()
