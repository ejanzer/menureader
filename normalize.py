from PIL import Image, ImageOps, ImageFilter

THRESHOLD_OFFSET = 20

def check_image(im):
    pass

def resize_image(im):
    pass

def get_threshold(im):
    """Get the threshold for determining whether a pixel turns to white or black."""
    # get_data returns an array of all pixel values in image.
    pixel_values = im.get_data()
    average = sum(pixel_values)/len(pixel_values)

    # using a treshold offset to deal with antialiasing... remove if it doesn't work
    return average - THRESHOLD_OFFSET


def remove_noise(im):
    """Remove background noise from image by changing all pixels to white or black."""
    threshold = get_threshold(im)

    for column in range(im.size[0]):
        for row in range(im.size[1]):
            if im.get_pixel((column, row)) < threshold:
                # If pixel is darker than threshold, replace with black.
                value = 0
            else:
                # Otherwise, replace with white.
                value = 255
            im.put_pixel((column, row), value)


def sample_corners(im):
    pass

def crop_image(im):
    pass

def smooth_and_grayscale(im):
    """Prepare an image for processing by running through a smoothing filter and 
    converting to grayscale"""
    im = im.filter(ImageFilter.SMOOTH_MORE)
    im = im.filter(ImageFilter.SMOOTH_MORE)

    if im.mode != 'L':
        im = im.convert('L')

    return im

def normalize_image(path):
    im = Image.open(path)
    im = smooth_and_grayscale(im)
    im = remove_noise(im)
    im.save(path)
