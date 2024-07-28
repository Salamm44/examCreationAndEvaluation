import cv2
import os
from image_processing import detect_quadrats, preprocess_image
import numpy as np

def get_image_paths(directory):
    file_names = os.listdir(directory)
    image_files = [file for file in file_names if file.lower().endswith(('.png', '.jpg', '.jpeg'))]
    image_paths = [os.path.join(directory, file) for file in image_files]
    return image_paths

def main(image_path):
    image, binary = preprocess_image(image_path)
    if image is not None and binary is not None:
        result_image = detect_quadrats(image, binary)
        
        if result_image is not None and isinstance(result_image, np.ndarray):
            print("Result image shape:", result_image.shape)
            cv2.imshow('Result', result_image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        else:
            print("Error: No result image to display or result image is not a valid numpy array.")
    else:
        print("Error: Image processing failed.")

if __name__ == "__main__":
    directory = './assets/processed_images'
    image_files = ['Student_sheet_20240726_150601.jpg']
    image_paths = [os.path.join(directory, file) for file in image_files]
    for image_path in image_paths:
        main(image_path)
