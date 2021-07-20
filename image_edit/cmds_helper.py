#####################################
# HELPER FUNCTIONS FOR THE COMMANDS #
#####################################

from PIL import Image

def args_to_array(value, min_args):
    """
    Converts a string of arguments seperated by ";" to a list of values
    """
    value = value.split(';')

    if len(value) < min_args:
        raise Exception("not enough arguments")

    return value


def all_to_int(array):
    """
    Used to convert an array of string args to ints
    """
    
    return [int(x.strip()) for x in array]


def blend(img1, img2, alpha):
    img2 = img2.resize(img1.size)

    return Image.blend(img1.convert("RGBA"), img2.convert("RGBA"), alpha)
