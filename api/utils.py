import os
import random
import string


def random_string(length):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))


def get_video_upload_path(instance, filename):
    name = filename.split('.')[0]
    ext = filename.split('.')[1]
    return os.path.join(
        "user_%s" % instance.owner.user_id, "videos", "{}_{}.{}".format(name, random_string(5), ext))


def get_audio_upload_path(instance, filename):
    name = filename.split('.')[0]
    ext = filename.split('.')[1]
    return os.path.join(
        "user_%s" % instance.owner.user_id, "audios", "{}_{}.{}".format(name, random_string(5), ext))


def get_image_upload_path(instance, filename):
    name = filename.split('.')[0]
    ext = filename.split('.')[1]
    return os.path.join(
        "user_%s" % instance.owner.user_id, "images", "{}_{}.{}".format(name, random_string(5), ext))
