from pdf2image import convert_from_path
import cv2
import numpy as np

# Convert PDF to image
pages = convert_from_path('test_sample.pdf', 300)
page = pages[0]

# Save the image for further processing
page.save('answer_sheet.jpg', 'JPEG')

# Load the image
image = cv2.imread('answer_sheet.jpg')

# Convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply GaussianBlur to reduce noise
blurred = cv2.GaussianBlur(gray, (5, 5), 0)

# Apply adaptive thresholding
thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                               cv2.THRESH_BINARY_INV, 11, 2)

# Find contours
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Filter and sort contours
filtered_contours = [c for c in contours if cv2.contourArea(c) > 1000]
filtered_contours = sorted(filtered_contours, key=lambda c: cv2.boundingRect(c)[1])

# Draw contours on the image
contour_image = image.copy()
cv2.drawContours(contour_image, filtered_contours, -1, (0, 255, 0), 2)

# Save the contour image for debugging
cv2.imwrite('contours.jpg', contour_image)

def is_bubble_filled(bubble_roi):
    # Count the number of non-zero pixels within the ROI
    return cv2.countNonZero(bubble_roi) > 500

# Iterate through each detected contour
for contour in filtered_contours:
    x, y, w, h = cv2.boundingRect(contour)
    roi = thresh[y:y+h, x:x+w]
    
    # Assuming three options per question, divide the region into three parts
    height, width = roi.shape
    bubble_height = height // 3
    
    filled_bubbles = []
    for i in range(3):
        bubble_roi = roi[i*bubble_height:(i+1)*bubble_height, :]
        if is_bubble_filled(bubble_roi):
            filled_bubbles.append(i + 1)  # Assuming options are numbered 1, 2, 3
    
    print(f"Question at ({x}, {y}): Filled Bubbles: {filled_bubbles}")

# Save the final processed image for reference
cv2.imwrite('final_result.jpg', image)
