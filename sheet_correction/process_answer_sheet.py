import cv2
from pdf2image import convert_from_path

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
thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
filtered_contours = [c for c in contours if cv2.contourArea(c) > 1000]
filtered_contours = sorted(filtered_contours, key=lambda c: cv2.boundingRect(c)[1])

def is_bubble_filled(bubble_roi):
    return cv2.countNonZero(bubble_roi) > 200

# Estimate the number of checkboxes per question
total_height = sum(cv2.boundingRect(c)[3] for c in filtered_contours)
average_height = total_height / len(filtered_contours)
num_checkboxes_per_question = round(average_height / (average_height / len(filtered_contours)))

checkbox_field_number = 1

for contour in filtered_contours:
    x, y, w, h = cv2.boundingRect(contour)
    cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
    
    roi = thresh[y:y+h, x:x+w]
    height, width = roi.shape
    checkbox_height = height // num_checkboxes_per_question
    
    for i in range(num_checkboxes_per_question):
        checkbox_roi = roi[i*checkbox_height:(i+1)*checkbox_height, :]
        cv2.rectangle(image, (x, y + i*checkbox_height), (x + w, y + (i+1)*checkbox_height), (255, 0, 0), 2)
        
        if is_bubble_filled(checkbox_roi):
            print(f"Checkbox Field {checkbox_field_number}: Filled")
            break
        else:
            print(f"Checkbox Field {checkbox_field_number}: Not Filled")
    
    checkbox_field_number += 1

cv2.imwrite('debug_final_result.jpg', image)