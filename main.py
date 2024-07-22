import gui
import cv2
import os
from image_processing import load_images
from opencv_test import display_image
from image_processing import preprocess_image  # Assuming this is a custom module for preprocessing

def get_image_paths(directory):
    file_names = os.listdir(directory)
    image_files = [file for file in file_names if file.lower().endswith(('.png', '.jpg', '.jpeg'))]
    # Create full paths to the images
    image_paths = [os.path.join(directory, file) for file in image_files]
    return image_paths

def main():
    
    # Test Code
    # Specify the directory containing images
    directory = './assets/processed_images'
    image_paths = get_image_paths(directory)  # Retrieve image paths

    for path in image_paths:
        # Read the image from each path
        image = cv2.imread(path)
        
        # Apply preprocessing to the image
        processed_image = preprocess_image(image)
        
        # Display the processed image
        cv2.imshow('Processed Image', processed_image)
        cv2.waitKey(0)  # Wait for a key press to proceed to the next image
    
    cv2.destroyAllWindows()  # Close all OpenCV windows after displaying all images


    # Main Code
	# Initialize the GUI
	# gui.init_gui()


	# Any additional setup can go here. The GUI will handle file uploads and conversions.
	# If there's image processing to be done after conversion, it should be triggered from the GUI.

if __name__ == "__main__":
	main()