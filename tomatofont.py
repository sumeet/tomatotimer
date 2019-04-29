from PIL import Image
import pathlib

CURRENT_DIR = pathlib.Path(__file__).parent

def open_image(filename):
    img = Image.open(filename)
    # cut out the top 5px or so, and see if it looks any better...
    x, y = img.size
    return img.crop((0, 10, x, y))

# for example {'0': <Image>, '1': <Image>, ...}
IMAGE_BY_CHAR = {str(i): open_image(f'{i}.png') for i in range(10)}




def to_tomato_image(num):
    if num < 0 or num > 99:
        raise ValueError('num must be between 0 and 99')

    num_str = str(num).zfill(2)
    images = [IMAGE_BY_CHAR.get(n) for n in num_str]
    return make_square(stretch_a_bit(combine_images(images)))


# makes it a square by adding transparent borders around the outside
def make_square(im):
    x, y = im.size
    size = max(x, y)
    new_im = Image.new('RGBA', (size, size))
    new_im.paste(im, (int((size - x) / 2), int((size - y) / 2)))
    return new_im


def stretch_a_bit(im):
    x, y = im.size
    #assert x == 120 and y == 85
    return im.resize((120, 100), Image.LANCZOS)

# https://stackoverflow.com/a/30228308/149987
def combine_images(images):
    widths, heights = zip(*(i.size for i in images))

    total_width = sum(widths)
    max_height = max(heights)

    new_im = Image.new('RGBA', (total_width, max_height))

    x_offset = 0
    for im in images:
      new_im.paste(im, (x_offset,0))
      x_offset += im.size[0]

    return new_im
