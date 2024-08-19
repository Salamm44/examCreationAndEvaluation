import cv2
import numpy as np

def preprocess_image(image_path):
    # Load image
    image = cv2.imread(image_path)
    if image is None:
        print("Error: Unable to load image.")
        return None, None

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Convert to binary with adaptive thresholding
    binary = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY_INV, 11, 2)

    # Perform morphological operations to improve contour detection
    kernel = np.ones((3, 3), np.uint8)
    binary = cv2.dilate(binary, kernel, iterations=1)
    binary = cv2.erode(binary, kernel, iterations=1)

    return image, binary

def detect_quadrats(image, binary):
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    empty_quadrats = []
    filled_quadrats = []

    for contour in contours:
        area = cv2.contourArea(contour)
        if 500 < area < 800:  # Assuming quadrat area falls within this range
            mask = np.zeros_like(binary)
            cv2.drawContours(mask, [contour], -1, color=255, thickness=-1)
            mean_val = cv2.mean(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), mask=mask)[0]

            if mean_val > 180:  # Adjusted threshold for distinguishing between empty and filled quadrats
                empty_quadrats.append(contour)
            else:
                filled_quadrats.append(contour)

    for contour in empty_quadrats:
        cv2.drawContours(image, [contour], -1, color=(0, 0, 255), thickness=2)

    for contour in filled_quadrats:
        cv2.drawContours(image, [contour], -1, color=(0, 255, 0), thickness=2)

    return image, filled_quadrats, empty_quadrats



def extract_answers(filled_quadrats, empty_quadrats):
    # Assuming each quadrat corresponds to a question and filled quadrats are the selected answers
    answers = []
    for i in range(len(filled_quadrats)):
        answers.append(1)  # 1 for filled (selected answer)
    for i in range(len(empty_quadrats)):
        answers.append(0)  # 0 for empty (not selected)
    return answers

def calculate_scores(student_answers, correct_answers):
    score = 0
    for student_answer, correct_answer in zip(student_answers, correct_answers):
        if student_answer == correct_answer:
            score += 1
    return score


def process_image_for_scoring(image_path, correct_answers):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY_INV)

    processed_image, filled_quadrats, empty_quadrats = detect_quadrats(image, binary)
    student_answers = extract_answers(filled_quadrats, empty_quadrats)
    score = calculate_scores(student_answers, correct_answers)

    return processed_image, score


