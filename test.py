# Import necessary libraries
import cv2
import numpy as np
import pytesseract
from PIL import Image

# Define the file path of the image to be processed
image_path = '/Users/kamrankhanalwi/Desktop/pic.png'

# Read the image using OpenCV
image = cv2.imread(image_path)

# Convert the image to grayscale
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply thresholding to enhance the text
_, thresholded_image = cv2.threshold(gray_image, 150, 255, cv2.THRESH_BINARY)

# Further denoise the image using morphological operations
kernel = np.ones((1, 1), np.uint8)
eroded_image = cv2.erode(thresholded_image, kernel, iterations=1)
denoised_image = cv2.dilate(eroded_image, kernel, iterations=1)

# Save the preprocessed image
preprocessed_image_path = "preprocessed_temp.png"
cv2.imwrite(preprocessed_image_path, denoised_image)

# Perform OCR on the preprocessed image using Tesseract
extracted_text = pytesseract.image_to_string(Image.open(preprocessed_image_path))

# Print the extracted text
print("Extracted Text:", extracted_text)

