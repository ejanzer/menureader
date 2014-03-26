from PIL import Image, ImageOps, ImageFilter
import numpy
from skimage.morphology import skeletonize, dilation, selem, opening, closing

# Threshold offset to help with antialiasing problems.
THRESHOLD_OFFSET = 20

# TODO: check if the image is really an image, for security purposes.
def check_image(im):
    pass

# TODO: Check if an image has a dark background and white foreground.
# If so, invert it.
def sample_corners(im):
    pass

def get_threshold(im):
    """Get the threshold for determining whether a pixel turns to white or black."""
    # get_data returns an array of all pixel values in image.
    pixel_values = im.getdata()
    average = sum(pixel_values)/len(pixel_values)

    # using a treshold offset to deal with antialiasing... remove if it doesn't work
    return average - THRESHOLD_OFFSET


def binarize(im):
    """Remove background noise from image by changing all pixels to white or black."""
    threshold = get_threshold(im)

    for column in range(im.size[0]):
        for row in range(im.size[1]):
            if im.getpixel((column, row)) < threshold:
                # If pixel is darker than threshold, replace with black.
                value = 0
            else:
                # Otherwise, replace with white.
                value = 255
            im.putpixel((column, row), value)
            
    return im


def smooth_and_grayscale(im):
    """Prepare an image for processing by running through a smoothing filter and 
    converting to grayscale"""
    im = im.filter(ImageFilter.SMOOTH_MORE)
    im = im.filter(ImageFilter.SMOOTH_MORE)

    if im.mode != 'L':
        im = im.convert('L')

    return im

def thin_image(im):
    """Thin ("skeletonize") a binarized image using 
    scikit-image.morphology.skeletonize()."""

    pix = im_to_trutharray(im)

    # Skeletonize removes layers of the foreground, leaving only a skeleton 
    thinned_pix = skeletonize(pix)

    thinned_im = trutharray_to_im(thinned_pix)

    return thinned_im

def im_to_trutharray(im):
    # First convert image to numpy array of pixel values
    pix = numpy.array(im)

    # Convert black values to 1 (foreground), white to 0 (background)
    for row in pix:
        for i in range(len(row)):
            if row[i] == 255:
                row[i] = 0
            else:
                row[i] = 1

    return pix

def trutharray_to_im(ndarray):
    # Convert back to pixel array. PIL requires uint8 array
    pix = numpy.uint8(ndarray)

    # Convert from 1s and 0s back to pixel values (255 and 0)
    for row in pix:
        for i in range(len(row)):
            if row[i] == 0:
                row[i] = 255
            elif row[i] == 1:
                row[i] = 0

    # Convert back to image and return.
    im = Image.fromarray(pix.astype('uint8'))

    return im

def opening_image(ndarray):
    opened = opening(ndarray, selem.square(3))
    return opened

def closing_image(ndarray):
    closed = closing(ndarray, selem.square(3))
    return closed

def dilate(ndarray):
    dilated = dilation(ndarray, selem.square(3))
    return dilated

def erode(ndarray):
    pass

def stentiford_smoothing(pix):
    for i in range(1, len(pix) - 1):
        for j in range(1, len(pix[i]) - 1):
            if num_black_neighbors(pix, i, j) < 2 and connectivity(pix, i, j) < 2:
                pix[i][j] = 1


def get_neighbors(pix, i, j):

    # TODO: What do I do on the edges? This won't work until I figure that out...

    neighbors = [
        pix[i][j+1],
        pix[i+1][j+1],
        pix[i+1][j],
        pix[i+1][j-1],
        pix[i][j-1],
        pix[i-1][j-1],
        pix[i-1][j],
        pix[i-1][j+1]
    ]

    return neighbors


def num_black_neighbors(pix, i, j):
    neighbors = get_neighbors(pix, i, j)

    count = 0

    for neighbor in neighbors:
        if neighbor == 0:
            count += 1

    return count

def connectivity(pix, i, j):
    neighbors = get_neighbors(pix, i, j)
    
    last = neighbors[0]
    conn = 0

    for k in range(len(neighbors)):
        if neighbors[k] != last:
            conn += 1
        last = neighbors[k]

    return conn


def normalize_image(path):
    im = Image.open(path)
    im = smooth_and_grayscale(im)

    pix = numpy.array(im)
    pix = opening_image(pix)
    pix = closing_image(pix)

    im = Image.fromarray(pix)
    im = binarize(im)
    im = thin_image(im)

    im.save(path)
