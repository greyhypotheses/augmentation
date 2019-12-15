import os
import dask.delayed
import cv2
import skimage
import skimage.io


@dask.delayed
def alias(filename, angle):
    """
    :type filename: numpy.str_
    :type angle: int

    :params filename: The name of the image file, including the relative
                      path if applicable
    :params angle: The angle of rotation, in degrees.

    :return
          A name for the augmented.  String
    """

    assert type(angle) == int, "The angle of rotation must be an integer number"
    assert (angle >= 0) & (angle < 360), "The angle of rotation must be an integer >= 0 but < 360"

    baseline = os.path.splitext(os.path.basename(filename))[0]
    return baseline + '_' + str(angle).zfill(3) + '.png'


@dask.delayed
def read(filename):
    """
    :type filename: str

    :params filename: The image URL String, or a string accepted by skimage.io.imread()

    :return
          An image. numpy.ndarray ~ shape(rows, columns, channels)
    """

    return skimage.io.imread(filename)


@dask.delayed
def save(tensor, filename):
    """
    :type tensor: numpy.ndarray
    :type filename: str

    :param tensor:
    :param filename:
    :return:
        1 if success else 0
    """
    success = cv2.imwrite(filename, tensor)
    return 1 if success else 0
