import textwrap
from PIL import Image, ImageFont
from pilmoji import Pilmoji


def make_image(text, in_image, out_image):
    image = Image.open("images/" + in_image)
    font = ImageFont.truetype("fonts/Ubuntu-B.ttf", 37)

    margin = offset = 40
    with Pilmoji(image) as pilmoji:
        for line in textwrap.wrap(text, width=50):
            pilmoji.text((margin, offset), line, font=font, fill='black')
            offset += font.getsize(line)[1]
    image.save("temp_images/" + out_image)
