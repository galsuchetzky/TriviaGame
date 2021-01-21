class Question:
    """
    Represents a question for the trivia.
    """

    def __init__(self, question_dict):
        """
        Represents a question, expects input of the form:
        {
        "index": question index
        "question": question
        "ans0": ans0
        "ans1": ans1
        "ans2": ans2
        "ans3": ans3
        "correct": correct answer idx
        }

        note: assuming correct answer number is in {0,1,2,3}.
        """
        self.question_dict = question_dict

    def __str__(self):
        """
        Returns a string representation of the question.
        """
        return 'question: ' + self.question_dict['question'] \
               + 'answer 1: ' + self.question_dict['ans0'] \
               + 'answer 1: ' + self.question_dict['ans1'] \
               + 'answer 1: ' + self.question_dict['ans2'] \
               + 'answer 1: ' + self.question_dict['ans3'] \
               + 'correct answer: ' + str(self.question_dict['correct'])

    def __getitem__(self, key):
        return self.question_dict[key]

    def __setitem__(self, key, value):
        self.question_dict[key] = value
