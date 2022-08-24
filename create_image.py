import textwrap
import requests

from PIL import Image, ImageFont
from pilmoji import Pilmoji


def make_image_file(text, file):
    image = Image.open("images/" + file)
    make_image(image, text, width=20, font_size=42)


def make_image_web(text, url):
    image = Image.open(requests.get(url, stream=True).raw)
    x, y = image.size
    make_image(image, text, width=x // 35, font_size=35)


def make_image(image, text, width, font_size):
    font = ImageFont.truetype("fonts/Ubuntu-B.ttf", font_size)
    margin = offset = 20
    with Pilmoji(image) as pilmoji:
        for line in textwrap.wrap(text, width=width):
            pilmoji.text((margin, offset), line, font=font, fill='black')
            offset += font.getsize(line)[1]
    image.save("temp_images/" + "tmp.jpg")
