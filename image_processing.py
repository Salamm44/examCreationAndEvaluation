import cv2
import numpy as np
import os

def preprocess_image(image_path):
    image = cv2.imread(image_path)
    if image is None:
        print(f"Error loading image: {image_path}")
        return None, None

    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)
    binary_image = cv2.adaptiveThreshold(blurred_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
    return gray_image, binary_image


def detect_quadrat(gray_image, binary_image):
    contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    filled_quadrats = []
    empty_quadrats = []

    min_area = 400  # Adjust this value based on your expected quadrat size

    for contour in contours:
        approx = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True)
        if len(approx) == 4:
            x, y, w, h = cv2.boundingRect(approx)
            if 10 < w < 200 and 10 < h < 200:  # Adjusted size range
                contour_area = cv2.contourArea(contour)
                if contour_area > min_area:
                    mask = np.zeros_like(binary_image)
                    cv2.drawContours(mask, [approx], -1, 255, -1)

                    # Calculate mean value of the pixels within the quadrat
                    mean_val = cv2.mean(gray_image, mask=mask)[0]

                    # Debug output
                    print(f"Contour area: {contour_area}, Mean value: {mean_val}")

                    # Adjusted threshold value
                    if mean_val > 150:  # Higher mean value indicates an empty quadrat
                        empty_quadrats.append(approx)
                        print("Added to empty_quadrats")
                    else:
                        filled_quadrats.append(approx)
                        print("Added to filled_quadrats")
    
    # Create a copy of the original image to draw on
    output_image = cv2.cvtColor(binary_image, cv2.COLOR_GRAY2BGR)

    # Draw filled quadrats in red
    for quadrat in filled_quadrats:
        cv2.drawContours(output_image, [quadrat], -1, (0, 0, 255), 2)  # Red color in BGR

    # Draw empty quadrats in green
    for quadrat in empty_quadrats:
        cv2.drawContours(output_image, [quadrat], -1, (0, 255, 0), 2)  # Green color in BGR

    # Display the final image
    cv2.imshow('Detected Quadrats', output_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return filled_quadrats, empty_quadrats