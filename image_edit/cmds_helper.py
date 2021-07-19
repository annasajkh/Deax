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

def get_concat_h_repeat(img, column):
    result = Image.new("RGB", (img.width * column, img.height))

    for x in range(column):
        result.paste(img, (x * img.width, 0))

    return result


def get_concat_v_repeat(img, row):
    result = Image.new("RGB", (img.width, img.height * row))

    for x in range(row):
        result.paste(img, (0, x * img.height))

    return result


def get_concat_tile_repeat(img, column, row):
    result_h = get_concat_h_repeat(img, column)
    
    return get_concat_v_repeat(result_h, row)
