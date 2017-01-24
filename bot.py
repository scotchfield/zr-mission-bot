import flickrapi
import os
import random
import textwrap
import urllib

import config

from PIL import Image, ImageFont, ImageDraw

IMAGE_SIZE = ( 512, 512 )


def getListFromFile( filename ):
    obj = []
    input_file = open( filename, 'r' )
    for line in input_file:
        obj.append( line.strip() )
    input_file.close()
    return obj

def getPhotos( flickr, search ):
    print( 'Searching for {0}'.format( search ) )
    photo_obj = flickr.photos.search(
        text = '{0}'.format( search ),
        sort = 'relevance',
        per_page = 10
    )
    return photo_obj[ 'photos' ][ 'photo' ]

def getFile( url, url_filename ):
    if os.path.isfile( 'cache/{0}'.format( url_filename ) ):
        return

    print( 'File does not exist!' )

    urllib.urlretrieve( url, 'cache/{0}'.format( url_filename ) )



def main():
    object_obj = getListFromFile( 'objects.txt' )
    mission_object = random.choice( object_obj )

    image = Image.new( 'RGB', IMAGE_SIZE, ( 0, 32, 32 ) )

    message = 'Abel township is in trouble, and only your ' + mission_object + ' can help. #zombiesrun'
    message_lines = textwrap.wrap( message, 50 )

    flickr = flickrapi.FlickrAPI(
        config.API_KEY, config.API_SECRET, format='parsed-json'
    )
    photo_obj = getPhotos( flickr, mission_object )

    photo = random.choice( photo_obj )
    url_filename = '{0}_{1}.jpg'.format( photo[ 'id' ], photo[ 'secret' ] )
    url = 'https://farm{0}.staticflickr.com/{1}/{2}'.format(
        photo[ 'farm' ], photo[ 'server' ], url_filename )

    print( url )

    getFile( url, url_filename )

    image_mission = Image.open( 'cache/' + url_filename ).convert( 'L' ).resize( IMAGE_SIZE )
    source = image_mission.split()
    nr = source[0].point(lambda i: 0 if i < 128 else 159)
    ngb = source[0].point(lambda i: 32)
    image_mission = Image.merge( 'RGB', ( nr, ngb, ngb ) )
    offset = int( IMAGE_SIZE[1] * 0.16 )
    image_mission_crop = image_mission.crop(
        ( 0, offset, IMAGE_SIZE[0] - 1, int( IMAGE_SIZE[1] * 0.67 ) + offset )
    )

    image.paste( image_mission_crop, ( 0, 0 ) )

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

    image.show()
    image.save( 'output/' + url_filename )


if __name__ == "__main__":
    main()
