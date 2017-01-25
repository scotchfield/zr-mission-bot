import random
import textwrap
import util

from PIL import Image, ImageFont, ImageDraw

IMAGE_SIZE = ( 512, 512 )


def getMissionObject():
    object_obj = util.getListFromFile( 'objects.txt' )

    return random.choice( object_obj )

def getMessageLines(obj):
    message_obj = [
        'Abel township is in trouble, and only your ' + obj + ' can help. #zombiesrun'
    ]
    message = random.choice(message_obj)
    return textwrap.wrap(message, 50)

def getNewImage(input_filename):
    image = Image.new('RGB', IMAGE_SIZE, (0, 32, 32))
    image_mission = Image.open('cache/' + input_filename).convert('L').resize(IMAGE_SIZE)

    source = image_mission.split()
    nr = source[0].point(lambda i: 0 if i < 128 else 159)
    ngb = source[0].point(lambda i: 32)
    image_mission = Image.merge('RGB', (nr, ngb, ngb))

    offset = int(IMAGE_SIZE[1] * 0.16)
    image_mission_crop = image_mission.crop(
        (0, offset, IMAGE_SIZE[0] - 1, int(IMAGE_SIZE[1] * 0.67) + offset)
    )
    image.paste(image_mission_crop, (0, 0))

    return image

def addMissionText(image, message_lines):
    draw = ImageDraw.Draw(image)

    font_italic = ImageFont.truetype( 'SFText-RegularItalic.otf', 20 )
    font = ImageFont.truetype( 'SFDisplay-Regular.otf', 20 )

    font_offset = int( IMAGE_SIZE[1] * 0.72 )

    for line in message_lines:
        _, font_height = font.getsize( line )
        draw.text(
            ( 10, font_offset ),
            line,
            font=font_italic,
            fill=( 255, 255, 255, 192 )
        )
        font_offset += font_height

    return image
