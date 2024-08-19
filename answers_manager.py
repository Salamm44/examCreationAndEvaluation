import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Define a global variable to store the correct answers
correct_answers = []
answer_mark = 0

def set_correct_answers(new_correct_answers):
    global correct_answers
    correct_answers = new_correct_answers
    logging.info(f"Correct answers updated: {correct_answers}")

def get_correct_answers():
    """
    Get the correct answers from the global variable.
    :return: List of correct answers
    """
    global correct_answers
    return correct_answers

def set_answer_mark(mark):
    global answer_mark
    answer_mark = mark
    logging.info(f"Answer mark set to: {answer_mark}")

def get_answer_mark():
    """
    Get the mark assigned to each correct answer.
    :return: Mark assigned to each correct answer
    """
    global answer_mark
    return answer_mark

def calculate_score(student_answers):
    """
    Calculate the score for a student based on their answers and the correct answers.

    Args:
        student_answers (list): The list of answers provided by the student.

    Returns:
        int: The calculated score.
    """
    global correct_answers, answer_mark
    if not correct_answers:
        logging.warning("Correct answers have not been set.")
        return 0

    # Log both lists for debugging
    logging.debug(f"Correct answers: {correct_answers}")
    # logging.debug(f"Student answers: {student_answers}")

    # Check for length mismatch
    if len(student_answers) != len(correct_answers):
        logging.warning(f"Length mismatch: {len(student_answers)} student answers vs {len(correct_answers)} correct answers.")
        return 0

    score = 0
    # Compare each student answer to the corresponding correct answer
    for student_answer, correct_answer in zip(student_answers, correct_answers):
        # Skip if either the student answer or the correct answer is 0
        if student_answer == 0 or correct_answer == 0:
            continue
        # Increment score if the answer is correct
        if student_answer == correct_answer:
            score += answer_mark

    logging.info(f"Calculated score: {score}")
    return score
