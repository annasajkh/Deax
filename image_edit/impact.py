import numpy as np

"""Generates impact font memes"""
from PIL import Image, ImageFont, ImageDraw

def get_font(image, caption):
    """Create font with dynamic size"""
    font_size = int(np.clip(image.width / 9 / (len(caption) / 16), 1, image.width / 8))
    return ImageFont.truetype("impact.ttf", size=font_size)

def draw_caption_text(x, y, border_size, caption, font, draw):
    """Draws the caption at the x and y, you need to initiate the draw first"""
    border_color = (0,0,0)
    text_color = (255, 255, 255)

    # Draw the border
    draw.text((x-border_size, y-border_size), caption, font=font, fill=border_color)
    draw.text((x+border_size, y-border_size), caption, font=font, fill=border_color)
    draw.text((x-border_size, y+border_size), caption, font=font, fill=border_color)
    draw.text((x+border_size, y+border_size), caption, font=font, fill=border_color)

    # Draw the caption
    draw.text((x, y), caption, text_color, font)

def generate_text_position(image, caption, font, draw, bottom=False):
    """Returns the position the text should be given the image, caption and font"""

    # Get caption size
    caption_width, caption_height = draw.textsize(caption, font)

    # Upper text position
    caption_position = (image.height-caption_height)/10

    if bottom:
        # The bottom caption position
        caption_position = (image.height-caption_height)-caption_position
    
    # Position horizontally
    x_position = (image.width-caption_width)/2
    
    return (x_position, caption_position)
    

def make_caption(image, caption=None, bottom_caption=None):
    """Generates impact font caption, if bottom_caption isn't specified there will be no bottom text"""

    # Create draw object on the image
    draw = ImageDraw.Draw(image)

    border_size = 2

    # 
    # UPPER
    #

    if caption:
        # Font
        upper_font = get_font(image, caption)

        # Position
        x, upper_text_position = generate_text_position(image, caption, upper_font, draw)

        # Draw
        draw_caption_text(x, upper_text_position, border_size, caption, upper_font, draw)

    #
    # BOTTOM
    #
        
    if bottom_caption: 
        # Font
        bottom_font = get_font(image, bottom_caption)

        # Position
        x, bottom_text_position = generate_text_position(image, bottom_caption, bottom_font, draw, True)

        # Draw
        draw_caption_text(x, bottom_text_position, border_size, bottom_caption, bottom_font, draw)

    return image
