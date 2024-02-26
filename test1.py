from selenium import webdriver
from PIL import Image
from io import BytesIO
from datetime import datetime

current_datetime = datetime.now()
current_datetime = current_datetime.strftime("%d_%m_%Y_%H_%M_%S")
img_download_path = f'/Users/kamrankhanalwi/Desktop/seln/Captcha2Img/{current_datetime}.png'

# screenshot = driver.get_screenshot_as_png()
# image = Image.open(BytesIO(screenshot))

image_path = '/Users/kamrankhanalwi/Desktop/seln/Captcha2Img/screenshot.png'
# cropped_image = image.crop((left, top, right, bottom))
crop_box = (870, 400, 1100, 480)
image = Image.open(image_path)
cropped_image = image.crop(crop_box)

# Save the cropped image to a file
cropped_image.save(img_download_path)