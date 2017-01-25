import flickrapi
import os
import random
import urllib

import config


def getListFromFile( filename ):
    obj = []

    input_file = open( filename, 'r' )
    for line in input_file:
        obj.append( line.strip() )
    input_file.close()

    return obj

def getFileFromUrl( url, url_filename ):
    if os.path.isfile( 'cache/{0}'.format( url_filename ) ):
        return

    urllib.urlretrieve( url, 'cache/{0}'.format( url_filename ) )

def getPhoto( search ):
    print( 'Searching for {0}'.format( search ) )

    flickr = flickrapi.FlickrAPI(
        config.API_KEY, config.API_SECRET, format='parsed-json'
    )

    photo_obj = flickr.photos.search(
        text = '{0}'.format( search ),
        sort = 'relevance',
        per_page = 10
    )

    photo = random.choice( photo_obj['photos']['photo'] )

    url_filename = '{0}_{1}.jpg'.format( photo[ 'id' ], photo[ 'secret' ] )
    url = 'https://farm{0}.staticflickr.com/{1}/{2}'.format(
        photo[ 'farm' ], photo[ 'server' ], url_filename )

    return url, url_filename
