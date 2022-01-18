import random

from GUI.QuestionSelectionGUI import QuestionSelectionGui
from Question import Question
from GUI.TriviaGUI import TriviaGui
from GUI.ResultsGUI import ResultsGui
from Utils import read_json


# todo extract all the Tk objects here and send them to the constructor.

def show_results(time_played, correct_answers, wrong_answers):
    ResultsGui(time_played, correct_answers, wrong_answers, play)


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
        """
        Runs the game.
        """
        TriviaGui(self.get_question, self.game_cap, self.end_game)

    def get_question(self):
        """
        Returns a random question from the questions list.
        """
        return self.questions[random.randint(0, len(self.questions) - 1)]

    def end_game(self, game_root, score, time_played):
        """
        Terminates the game.
        :param game_root: The root window of the game.
        :param score: The score of the game.
        :param time_played: The amount of time played.
        """
        game_root.destroy()
        show_results(time_played, score, self.game_cap - score)


def play(res_root=None):
    """
    Starts the game, destroys the old windows if any given.
    :param res_root: result window to destroy.
    :return:
    """
    if res_root:
        res_root.destroy()
    GameLogic()


if __name__ == '__main__':
    play()
