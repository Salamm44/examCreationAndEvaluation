# answers_manager.py

# Define a global variable to store the correct answers
correct_answers = []

def set_correct_answers(answers):
    """
    Set the correct answers in the global variable.
    :param answers: List of correct answers
    """
    global correct_answers
    correct_answers = answers

def get_correct_answers():
    """
    Get the correct answers from the global variable.
    :return: List of correct answers
    """
    global correct_answers
    return correct_answers


def calculate_score(student_answers):
    """
    Compare student answers with correct answers and calculate the score.
    :param student_answers: List of student answers
    :return: Score of the student
    """
    global correct_answers
    score = 0
    for student_answer, correct_answer in zip(student_answers, correct_answers):
        if student_answer == correct_answer: # If student answer is correct
            score += 1

    return score