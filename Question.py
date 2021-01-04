BR = '\r\n'


class Question:
    """
    Represents a question for the trivia.
    """

    def __init__(self, question_string):
        """
        Represents a question, expects input of the form:
        question
        ans0
        ans1
        ans2
        ans3
        correct ans num

        note: assuming correct answer number is in {0,1,2,3}.
        """
        self.question_string = question_string
        # Breaks down the question string
        self.answers = [None] * 4
        try:
            self.question, self.answers[0], self.answers[1], self.answers[2], self.answers[3], \
            self.correct_ans = [item for item in question_string.split('\r\n') if item]
        except ValueError:
            return

        self.correct_ans = int(self.correct_ans)

    def print_question(self):
        """
        Prints the question and the answers.
        """
        print(self.question)
        print(self.answers)
        print(self.correct_ans)

    def get_question(self):
        return self.question

    def set_question(self, new_question):
        self.question = new_question

    def get_answer(self, num):
        if not 0 <= num <= 3:
            return None
        return self.answers[num]

    def set_answer(self, num, new_answer):
        if not 0 <= num <= 3:
            return
        self.answers[num] = new_answer

    def get_correct_answer(self):
        return self.correct_ans

    def set_correct_answer(self, new_correct_ans):
        self.correct_ans = new_correct_ans

    def get_question_format(self):
        """
        Generates a valid question's format from a Question object.
        :return: The format
        """
        question_format = self.get_question() + '\r\n'
        for i in range(4):
            question_format += self.get_answer(i) + '\r\n'
        question_format += str(self.get_correct_answer())
        return question_format
