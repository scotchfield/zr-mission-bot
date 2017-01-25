import util
import zombify


def main():
    mission_object = zombify.getMissionObject()
    message_lines = zombify.getMessageLines( mission_object )

    url, url_filename = util.getPhoto(mission_object)

    util.getFileFromUrl(url, url_filename)

    image = zombify.getNewImage(url_filename)
    image = zombify.addMissionText(image, message_lines)

    image.show()
    image.save('output/' + url_filename)


if __name__ == "__main__":
    main()
