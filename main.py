import cv2
import os
from image_processing import detect_quadrat, preprocess_image

def get_image_paths(directory):
    file_names = os.listdir(directory)
    image_files = [file for file in file_names if file.lower().endswith(('.png', '.jpg', '.jpeg'))]
    image_paths = [os.path.join(directory, file) for file in image_files]
    return image_paths

def main(image_path):
    gray_image, binary_image = preprocess_image(image_path)
    if gray_image is not None and binary_image is not None:
        filled_quadrats, empty_quadrats = detect_quadrat(gray_image, binary_image)
        original_image = cv2.imread(image_path)

        if not filled_quadrats and not empty_quadrats:
            print(f"No quadrats detected in image: {image_path}")
        else:
            print(f"Detected {len(filled_quadrats)} filled quadrats and {len(empty_quadrats)} empty quadrats")
            cv2.drawContours(original_image, empty_quadrats, -1, (0, 0, 255), 2)  # Red for empty quadrats
            cv2.drawContours(original_image, filled_quadrats, -1, (0, 255, 0), 2)  # Green for filled quadrats
            cv2.namedWindow('Original Image with Detected Quadrats', cv2.WINDOW_NORMAL)
            cv2.imshow('Original Image with Detected Quadrats', original_image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

if __name__ == "__main__":
    directory = './assets/processed_images'
    image_files = ['Student_sheet_20240726_150601.jpg']
    image_paths = [os.path.join(directory, file) for file in image_files]
    for image_path in image_paths:
        main(image_path)