import numpy as np
import numexpr as ne
from PIL import Image

from cmds_helper import args_to_array


def get_comparison_func(comparison_str):
    # Not including "all"
    comparison_list = {
        '=': lambda x : x == limit,
        '<': lambda x : x < limit,
        '>': lambda x : x > limit,
        'a': True
        }

    # Get the comparison mode before converting the limit to int
    comparison_mode = comparison_str[0]
    if comparison_mode not in comparison_list.keys():
        raise Exception("pixel: comparison doesn't exist")

    # Convert limit to int
    # If mode isn't all
    if not comparison_mode == 'a':
        try:
            limit = int(comparison_str[1:])
        except:
            raise Exception("pixel: something wrong with the limit")

    return comparison_list[comparison_mode]


def pixel(value, img):
    """
    Args:

    1 - list of rgb channels the expression should be active on
    2 - a comparison on rgb values to be run on each pixel
    can be:
    =, like ==
    >
    <
    a, or apply on all pixels
    3 - the numexpr expression

    e.g.
    rg;>10;
    """
    
    rgb, comparison_str, exp = args_to_array(value, 3)

    # Get the function for comparing
    comparison = get_comparison_func(comparison_str)

    #
    # RGB booleans
    #

    r = 'r' in rgb
    g = 'g' in rgb
    b = 'b' in rgb

    #
    # Image processing
    #

    # Transform image to numpy array
    arr = np.array(img)

    # Evaluate 'exp' in the rgb channels desired
    for color_num, color_bool in enumerate([r, g, b]):
        print(color_bool)
        if color_bool:
            # make pixel the rgb channel desired
            pixel = arr[:,:,color_num]

            # evaluate expression
            arr_evaled = np.clip(ne.evaluate(exp), 0, 255)

            # replace

            # comparison_mode as True means that it's all
            if comparison == True:
                arr[:,:,color_num] = arr_evaled
            else:
                # Go through each pixel, checking if we should replace or not
                # TODO: rewrite to be more efficient
                for x in range(arr.shape[0]):
                    for y in range(arr.shape[1]):
                        if comparison(arr[x,y,color_num]):
                            arr[x,y,color_num] = arr_evaled[x, y]

    return Image.fromarray(arr)
    
