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

    font = ImageFont.truetype('SFText-RegularItalic.otf', 20)

    font_offset = int(IMAGE_SIZE[1] * 0.70)

    for line in message_lines:
        _, font_height = font.getsize(line)
        draw.text(
            (16, font_offset),
            line,
            font=font,
            fill=(192, 192, 192, 150)
        )
        font_offset += font_height + 5

    return image

def addStatsText(image):
    draw = ImageDraw.Draw(image)

    font_label = ImageFont.truetype('SFDisplay-Regular.otf', 18)
    fill = (192, 192, 192, 255)

    font_label_offset = int(IMAGE_SIZE[1] * 0.945)
    draw.text((16, font_label_offset), 'TIME', font=font_label, fill=fill)
    draw.text((115, font_label_offset), 'KM', font=font_label, fill=fill)
    draw.text((212, font_label_offset), 'KCAL', font=font_label, fill=fill)
    draw.text((315, font_label_offset), '/ KM', font=font_label, fill=fill)
    draw.text((410, font_label_offset), 'STEPS', font=font_label, fill=fill)

    font_detail = ImageFont.truetype('SFDisplay-Regular.otf', 26)
    fill = (255, 255, 255, 255)

    stats = (
        str(random.randint(24, 60)) + '.' + str(random.randint(10, 59)),
        str(random.randint(1, 10)) + '.' + str(random.randint(10, 99)),
        '-',
        str(random.randint(5, 9)) + ':' + str(random.randint(10, 59)),
        str(random.randint(1000, 10000))
    )

    font_detail_offset = int(IMAGE_SIZE[1] * 0.88)
    draw.text((16, font_detail_offset), stats[0], font=font_detail, fill=fill)
    draw.text((115, font_detail_offset), stats[1], font=font_detail, fill=fill)
    draw.text((212, font_detail_offset), stats[2], font=font_detail, fill=fill)
    draw.text((315, font_detail_offset), stats[3], font=font_detail, fill=fill)
    draw.text((410, font_detail_offset), stats[4], font=font_detail, fill=fill)

    return image
