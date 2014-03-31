from PIL import Image, ImageOps, ImageFilter
import numpy
from skimage.morphology import skeletonize, dilation, selem, opening, closing
import datetime as dt
from timing import time_elapsed

# Threshold offset to help with antialiasing problems.
THRESHOLD_OFFSET = 20

# Templates for Stentiford's acute angle emphasis step.
D1 = [
    [1,1,0,1,1],
    [1,1,0,1,1],
    [1,1,1,1,1],
    [1,1,1,1,1],
    ['*',1,1,1,'*']
]

D2 = [
    [1,0,0,1,1],
    [1,1,0,1,1],
    [1,1,1,1,1],
    [1,1,1,1,1],
    ['*',1,1,1,'*']
]

D3 = [
    [1,1,0,0,1],
    [1,1,0,1,1],
    [1,1,1,1,1],
    [1,1,1,1,1],
    ['*',1,1,1,'*']
]

D4 = [
    [1,0,0,1,1],
    [1,1,0,1,1],
    [1,1,1,1,1],
    [1,1,1,1,1],
    ['*',1,1,1,'*']
]

D5 = [
    [1,1,0,0,1],
    [1,1,0,0,1],
    [1,1,1,1,1],
    [1,1,1,1,1],
    ['*',1,1,1,'*']
]

U1 = [
    ['*',1,1,1,'*'],
    [1,1,1,1,1],
    [1,1,1,1,1],
    [1,1,0,1,1],
    [1,1,0,1,1]
]

U2 = [
    ['*',1,1,1,'*'],
    [1,1,1,1,1],
    [1,1,1,1,1],
    [1,1,0,1,1],
    [1,0,0,1,1]
]

U3 = [
    ['*',1,1,1,'*'],
    [1,1,1,1,1],
    [1,1,1,1,1],
    [1,1,0,1,1],
    [1,1,0,0,1]
]

U4 = [
    ['*',1,1,1,'*'],
    [1,1,1,1,1],
    [1,1,1,1,1],
    [1,0,0,1,1],
    [1,0,0,1,1]
]

U5 = [
    ['*',1,1,1,'*'],
    [1,1,1,1,1],
    [1,1,1,1,1],
    [1,1,0,0,1],
    [1,1,0,0,1]
]

TEMPLATES = [D1, D2, D3, D4, D5, U1, U2, U3, U4, U5]

########### STANDARD PREPROCESSING ###########

# TODO: check if the image is really an image, for security purposes.
def check_image(im):
    pass

# TODO: Check if an image has a dark background and white foreground.
# If so, invert it.
def sample_corners(im):
    pass

def smooth_and_grayscale(im):
    """Prepare an image for processing by running through a smoothing filter and 
    converting to grayscale"""
    im = im.filter(ImageFilter.SMOOTH_MORE)
    im = im.filter(ImageFilter.SMOOTH_MORE)

    if im.mode != 'L':
        im = im.convert('L')

    return im


########### THRESHOLDING/IMAGE BINARIZATION ###########
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

def get_threshold(im):
    """Get the threshold for determining whether a pixel turns to white or black."""
    # get_data returns an array of all pixel values in image.
    pixel_values = im.getdata()
    average = sum(pixel_values)/len(pixel_values)

    # using a treshold offset to deal with antialiasing... remove if it doesn't work
    return average - THRESHOLD_OFFSET


########### THINNING/SKELETONIZING IMAGE ###########
def thin_image(pix):
    """Thin ("skeletonize") a binarized image using 
    scikit-image.morphology.skeletonize(). Returns a copy, does not modify array in place."""

    # Skeletonize removes layers of the foreground, leaving only a skeleton 
    thinned_pix = skeletonize(pix)

    return thinned_pix

########### CONVERTING IMAGE DATA FOR USE BY SCIKIT-IMAGE ###########
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
    # Warning! This modifies the original array. Don't try to reuse after.
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

########### STENTIFORD'S IMAGE PREPROCESSING: SMOOTHING AND ACUTE ANGLE EMPHASIS ###########

def smooth_and_emphasize_angles(pix):
    """Get rid of 'spurious projections' on the image by removing (changing to white) any black pixels that
    have 2 or fewer black neighbors and have a connectivity number less than two.
    Reduce necking for image thinning/skeletonization by turning pixels on the interior of an acute angle to white."""
    
    # TODO: What do I do on the edges? This won't work until I figure that out...
    for i in range(2, len(pix) - 2):
        for j in range(2, len(pix[i]) - 2):
            if pix[i][j] == 1 and (is_spurious_projection(pix, i, j) or is_acute_angle(pix, i, j)):
                pix[i][j] = 0


def is_spurious_projection(pix, i, j):
    return num_black_neighbors(pix, i, j) <=2 and connectivity(pix, i, j) < 2

def is_acute_angle(pix, i, j):
    """Check if a pixel's immediate surroundings match one of Stentiford's templates 
    for acute angles."""
    for template in TEMPLATES:
        if check_template(pix, i, j, template):
            return True

    return False

def get_neighbors_1(pix, i, j):
    """Returns all neighbors within a 1-pixel radius of a pixel as an array, 
    starting on the right and going counterclockwise."""
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

def get_neighbors_2(pix, i, j):
    """Get a 5x5 grid of the neighbors around the pixel at i, j"""
    neighbors = [pix[i-2][j-2:j+3], pix[i-1][j-2:j+3], pix[i][j-2:j+3], pix[i+1][j-2:j+3], pix[i+2][j-2:j+3]]
    return neighbors

def num_black_neighbors(pix, i, j):
    """Return the number of black (foreground) neighbors a pixel has."""
    neighbors = get_neighbors_1(pix, i, j)

    count = 0

    for neighbor in neighbors:
        if neighbor == 1:
            count += 1

    return count

def connectivity(pix, i, j):
    """Return the connectivity number of a pixel in an image.
    Connectivity is defined as the number of regions a pixel connects, measured by
    how many times you change from background to foreground or vice versa as you iterate
    over its immediate neighbors, starting on the right and going counterclockwise."""
    neighbors = get_neighbors_1(pix, i, j)
    
    last = neighbors[0]
    conn = 0

    for k in range(len(neighbors)):
        if neighbors[k] != last:
            conn += 1
        last = neighbors[k]

    return conn


def check_template(pix, i, j, template):
    """Check a pixel's surroundings against a certain template. Return true if the same, 
    false if different. Ignore wildcards ('*')"""
    neighbors = get_neighbors_2(pix, i, j)
    for x in range(len(neighbors)):
        for y in range(len(neighbors[x])):
            if template[x][y] != '*' and template[x][y] != neighbors[x][y]:
                return False

    return True


######## MAIN FUNCTION #########

def normalize_image(path):
    """Normalize an image."""

    start = dt.datetime.now()

    # Steps using PIL
    im = Image.open(path)

    im = smooth_and_grayscale(im)
    start = time_elapsed("Smoothing", start)

    im = binarize(im)
    start = time_elapsed("Binarization", start)

    # Steps using scikit-image
    pix = im_to_trutharray(im)

    # Stentiford preprocessing for image thinning.
    smooth_and_emphasize_angles(pix)
    start = time_elapsed("Stentiford preprocessing", start)

    # Thinning
    pix = thin_image(pix)
    start = time_elapsed("Thinning", start)

    im = trutharray_to_im(pix)

    im.save(path)
