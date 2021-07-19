import random

import math
import numpy as np
from PIL import Image, ImageFilter, ImageFont, ImageDraw, ImageOps, ImageEnhance
from opensimplex import OpenSimplex

from cmds_helper import *
from impact import make_caption
from pixel import pixel


#####################
# COMMAND FUNCTIONS #
#####################


def crop(value, img):
    """
    Crops image by percent

    args:
    x;y;width;height
    """

    # Convert the argument string to a list of ints
    values = all_to_int(args_to_array(value, 4))

    # Limit the values to 0-100 so they're percentages
    # Then divide the values by 100 so multiplying a number
    # with them yields the <value> percentile of that number
    # Also deconstruct the list into variables
    x, y, w, h = map(lambda x: np.clip(int(x), 0, 100) / 100, values)
    
    # Coordinates for Image.crop()
    coord = tuple([int(c) for c in [img.size[0]*x,
                                    img.size[1]*y,
                                    img.size[0]*w,
                                    img.size[1]*h]])
    
    # Crop the image, by percentages
    return img.crop(coord)


def blur(value, img):
    try:
        value = np.clip(int(value), 0, 100)
    except:
        raise Exception("Error with blur value")
    
    return img.filter(ImageFilter.GaussianBlur(value))


def flip(value, img):
    """
    args:
    h or v
    """
    
    if value == "h":
        return img.transpose(Image.FLIP_LEFT_RIGHT)
    elif value == "v":
        return img.transpose(Image.FLIP_TOP_BOTTOM)
    else:
        raise Exception("Argument error for flip")
        

def impact(value, img):
    """
    args:
    toptext;bottomtext
    """

    values = args_to_array(value, 1)

    top_text = values[0] if values[0] != "" else None
    bottom_text = values[1] if len(values) != 1 else None

    make_caption(img, top_text, bottom_text)

    return img


# TODO automate min max and median
def minfunc(value, img):
    """Applies the min filter to 'img'"""
    try:
        value = np.clip(int(value), 0, 17)
    except:
        raise Exception("Argument error for min")

    return img.filter(ImageFilter.MinFilter(value))


def maxfunc(value, img):
    #value = number
    
    try:
        value = int(value)
    except:
        raise Exception("there is something wrong with max value")
    
    return img.filter(ImageFilter.MaxFilter(value))
    

def median(value, img):
    #value = number
    
    try:
        value = int(value)
    except:
        raise Exception("there is something wrong with median value")
    
    return img.filter(ImageFilter.MedianFilter(value))
    

def contrast(value, img):
    try:
        value = np.clip(int(value), -1000, 1000)
    except:
        raise Exception("Argument error for contrast")

    value = (259 * (value + 255)) / (255 * (259 - value))

    def c(x):
        x = 128 + value * (x - 128)
        return max(0, min(255, x))

    return img.point(c)


def multi(value, img):
    """
    Allows applying different commands in different parts of the image

    Args:
    x_percent;y_percent;width;height;<commands>
    commands are separated with :

    e.g
    10;30;40;80;blur=10:contrast=30
    10;30;40;80;glitch=true:blur=90:contrast=37
    """

    global commands_list


    def apply_commands(comlist, img):
        comlist = ";".join(comlist).split(':')

        for command in comlist:
            command = command.split('=')
            print(command[0])

            # Don't allow multi calls inside of multi
            if command[0] == 'multi' or command[0] == 'multirand':
                raise Exception("multi: multi not allowed recursively")
                
            # Run the commands
            if command[0] in commands_list:
                print("COMMAND IS")
                print(command)
                img = commands_list[command[0]](command[1], img)
            else:
                raise Exception("multi: command doesn't exist!")
        
        return img


    # Separate arguments
    values = args_to_array(value, 5)
    print(values)

    # Name the variables for readibility
    x, y, w, h = values[:4]

    # Convert string to int
    x, y, w, h = [int(i) for i in [x, y, w, h]]

    print(x, y, w, h)

    # Convert percentages to pixel coords
    x = int(img.size[0] * (x/100))
    y = int(img.size[1] * (y/100))
    w = int(img.size[0] * (w/100))
    h = int(img.size[1] * (h/100))

    print(x, y, w, h)

    #
    # Apply the effects
    #
    
    # Crop the rectangle
    rect = img.crop((x, y, w, h))

    # Apply the commands to the rectangle
    comlist = values[4:]
    rect = apply_commands(comlist, rect)

    #
    # Paste and return
    #

    # Paste the rectangle to the final image
    img.paste(rect, (x, y))

    return img


def multirand(value, img):
    """
    Like multi but the rectangle's position is chosen randomly

    Args:

    h_or_v;min_start;max_start;min_length;max_length;<commands>

    min_start, max_start and min_length are all in percentages
    """

    # Arguments
    values = args_to_array(value, 5)
    print(values)

    # Check if argument 0 is valid
    if value[0] not in ["h", "v"]:
        raise Exception('multirand: first argument must be "h" or "v"')


    # Assign names to the variables for readibility
    percent = lambda x : np.clip(int(x), 1, 100)
    min_start = percent(values[1])
    max_start = percent(values[2])
    min_length = percent(values[3])
    max_length = percent(values[4])

    # No trolling
    if min_length > max_length:
        raise Exception('multirand: min_length cannot be greater than max_length!')
        

    v = value[0] == "v"

    # size1 is width if vertical, else horizontal
    # size2 is the opposite
    size1 = img.size[0] if v else img.size[1]
    size2 = img.size[0] if not v else img.size[1]

    
    # Get the start and end percentages
    start = random.randint(min_start, max_start)
    end = percent(random.randint(start + min_length, start + max_length))

    start = int(start)
    end = int(end)

    # Call multi
    if v:
        value = str(start) + ';0;' + str(end) + ';' + str(size2) + ';' + ';'.join(values[5:])
    else:
        value = '0;' + str(start) + ';' + str(size2) + ';' + str(end) + ';' + ';'.join(values[5:])


    return multi(value, img)


def wave(value, img):
    """
    Waves the image according to a gradient noise generator

    Args:
    1 - h or v
    2 - frequency
    3 - amplitude

    e.g.
    h;50;300
    """

    values = args_to_array(value, 3)

    frequency = int(values[1])
    amplitude = int(values[2])

    v = values[0] == 'v'

    print(img.size)

    # Start the noise
    s = OpenSimplex(seed=random.randint(0, 1000000))

    # Make the waves start at 0
    # so using multi with them creates horrifying results
    offset = s.noise2d(0, 1) * amplitude

    # We're either going to loop through the width or height of the image
    # depending on wether the wave is horizontal or vertical

    # Vertical: width
    # Horizontal: height
    size = img.size[0] if v else img.size[1]

    # Convert the image to numpy array for rolling
    arr = np.array(img)

    # Loop through size
    # Size is the width of the image if the wave is vertical, else it's the height
    for x in range(size):
        # Takes the pixels
        a = arr[:, x] if v else arr[x]

        # Rolls/waves the pixels
        a = np.roll(a, int(s.noise2d(x/frequency, 1) * amplitude - offset), 0)

        # Replaces the pixels
        # in the same manner that we took them
        if v:
            arr[:, x] = a
        else:
            arr[x] = a

    return Image.fromarray(arr)


def filterfunc(value, img):
    """
    apply filter easily
    
    value=blur;emboss

    the function list is

    ['BLUR', 'BoxBlur', 'BuiltinFilter', 'CONTOUR', 'Color3DLUT', 'DETAIL', 
    'EDGE_ENHANCE', 'EDGE_ENHANCE_MORE', 'EMBOSS', 'FIND_EDGES', 'Filter', 
    'GaussianBlur', 'Kernel', 'MaxFilter', 'MedianFilter', 'MinFilter', 
    'ModeFilter', 'MultibandFilter', 'RankFilter', 'SHARPEN', 'SMOOTH', 
    'SMOOTH_MORE', 'UnsharpMask']
    """
    value = value.split(";")
    
    #remove function with that has _ in it
    filter_func = filter(lambda x : not "_" in x,dir(ImageFilter))

    #apply each function to the image
    for val in value:
        for func in filter_func:
            if val.lower() == func.lower():
                img = img.filter(getattr(ImageFilter,func))
                break
    return img


def crop_circle(value, img):
    """
    crop by using circle
    value is percentage
    """

    value = np.clip(int(value.strip()), 0, 100) / 100 * img.width if img.width > img.height else img.height

    center = (img.width // 2, img.height // 2)

    img_data = img.load()


    for x in range(img.width):
        for y in range(img.height):
            if math.dist(center,(x,y)) <= value:
                img_data[x, y] = img_data[x, y]
            else:
                img_data[x, y] = 0
    return img

def move(value, img):
    """
    move image
    args
    1. h / v
    2. percentage
    """

    value = args_to_array(value, 2)


    img_arr = np.array(img)

    if value[0] == "h":
        val = int(np.clip(int(value[1].strip()),0,100) / 100 * img.width)

        for i in range(img.width):
            img_arr[i,:] = np.roll(img_arr[i,:],val,0)

    elif value[0] == "v":
        val = int(np.clip(int(value[1].strip()),0,100) / 100 * img.height)

        for i in range(img.height):
            img_arr[:,i] = np.roll(img_arr[:, i],val,0)
        
    else:
        raise Exception("Argument error for flip")
    
    return Image.fromarray(img_arr)

        
def repeat(value, img):
    # value = number;number
    # range 0 -> 20
    value = all_to_int(args_to_array(value, 2))

    img = get_concat_tile_repeat(img, np.clip(value[0],0,20), np.clip(value[1],0,20))

    return img

    
def resize(value, img):
    print("whyyy")
    value = all_to_int(args_to_array(value, 2))

    img = img.resize((np.clip(value[0], 0, 8192), np.clip(value[1], 0, 8192)))

    return img


def hue(value, img):
    #value = number
    try:
        value = int(value)
    except:
        raise Exception("there is something wrong with hue value")

    
    HSV = img.convert("HSV")
    H, S, V = HSV.split()
    H = H.point(lambda x : value)
    return Image.merge("HSV", (H, S, V)).convert("RGB")


def sheer(value, img):
    value = int(value)




#def square_crop(self, value):
#        # value = number
#        value = int(value)
#
#        half_size_x = self.img.size[0] // 2
#        half_size_y = self.img.size[1] // 2
#
#        self.img = self.img.crop((  half_size_x - value,
#                                    half_size_y - value,
#                                    half_size_x + value,
#                                    half_size_y + value))
    

#def binary(self, value):
#        self.grayscale("true")
#        value = int(value)
#        pixels = self.img.load()
#        
#        for i in range(self.img.size[0]):
#                for j in range(self.img.size[1]):
#                    if pixels[i, j] >= value:
#                        pixels[i, j] = 255
#                    else:
#                        pixels[i, j] = 0


#def light(self,value):
#        value = float(value)
#
#        max_radius = self.img.width if self.img.width < self.img.height else self.img.height
#        img = self.img.load()
#        center = (self.img.width // 2, self.img.height // 2)
#
#        max_x = abs(max_radius - center[0])
#        max_y = abs(max_radius - center[1])
#
#
#        max_distance = math.sqrt(max_x * max_x + max_y * max_y)
#
#        for i in range(self.img.width):
#            for j in range(self.img.height):
#
#                x = abs(i - center[0])
#                y = abs(j - center[1])
#
#                distance = math.sqrt(x * x + y * y)
#                img[i ,j] = tuple(map(lambda x : int(x * (1 - (distance / max_distance * value)) * 3), img[i ,j]))


##########################################
# HELPER FUNCTIONS FOR THE COMMANDS LIST #
##########################################


def lambda_filter(imgfilter):
    """
    Returns a lambda with two arguments
    if the first argument is the string "true", 'imgfilter' is applied to the second argument
    """

    return lambda value, img : img.filter(imgfilter) if value == "true" else img
    
def lambda_function(func):
    """
    Returns a lambda with two arguments
    if the first argument is the string "true", 'func' is applied to the second argument
    """

    return lambda value, img : func(img) if value == "true" else img


def lambda_function_adv(func, minval, maxval):
    """
    Returns a function with two arguments

    the first argument is a string
    that string is converted to an int and clamped between 'minval' and 'maxval'

    The second argument is an image
    """
    def fun(value, img):
        try:
            value = np.clip(int(value), minval, maxval)
        except:
            raise Exception("Argument error")
        
        return func(img, value)

    return fun


#################
# COMMANDS LIST #
#################


commands_list = {
    "rotate": lambda value, img : img.rotate(int(value), expand=True),
    "glitch": lambda value, img : img.point(lambda x : random.randint(-256, 256)) if value == "true" else img,
    "brightness": lambda value, img : ImageEnhance.Brightness(img).enhance(float(value)),
    "hue": lambda value, img : Image.merge('HSV', (img.convert('HSV').split()[0].point(lambda x : int(value))) + img.convert('HSV')[1:]).convert('RGB'),

    "contour": lambda_filter(ImageFilter.CONTOUR),
    "enhance": lambda_filter(ImageFilter.EDGE_ENHANCE_MORE),
    "emboss": lambda_filter(ImageFilter.EMBOSS),
    "edges": lambda_filter(ImageFilter.FIND_EDGES),

    "grayscale": lambda_function(ImageOps.grayscale),
    "invert": lambda_function(ImageOps.invert),

    "crop": crop,
    "blur": blur,
    "flip": flip,
    "impact": impact,
    "min": minfunc,
    "max": maxfunc,
    "median": median,
    "contrast": contrast,
    "multi": multi,
    "multirand": multirand,
    "wave": wave,
    "pixel": pixel,

    "solarize": lambda_function_adv(ImageOps.solarize, -100, 100),

    "filter": filterfunc,
    "crop_circle": crop_circle,
    "move": move,
    "repeat": repeat,
    "resize": resize
}
