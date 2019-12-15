import cv2
import dask.delayed


@dask.delayed
def clip(tensor, strip):
    """
    :type tensor: numpy.ndarray
    :type strip: int

    :params tensor: An image.
    :params strip: The width that would be clipped of each image edge.

    :return
      A clipped image.  numpy.ndarray ~ (rows, columns, channels)
    """
    return tensor[strip:(tensor.shape[0] - strip), strip:(tensor.shape[1] - strip)]


@dask.delayed
def resize(tensor, dimensions):
    """
    :type tensor: numpy.ndarray
    :type dimensions: tuple

    :params tensor: An image.
    :params dimensions: The target size.  Expected ~ tuple(width or columns, height or rows)

    :return
      A resized image. numpy.ndarray ~ (rows, columns, channels)
    """
    return cv2.resize(tensor, dsize=dimensions, interpolation=cv2.INTER_AREA)


@dask.delayed
def rotate(tensor, dimensions, centre, angle):
    """
    :type tensor: numpy.ndarray
    :type dimensions: tuple
    :type centre: tuple
    :type angle: int

    :params tensor: An image.
    :params dimensions: The target size.  Expected ~ tuple(width or columns, height or rows)
    :params centre: The centre point about which an image is rotated. A tuple of
                    the y & x co-ordinates, i.e., (y, x), of the centre is expected.
    :params angle: Rotation angle in degrees.

    :return
      A rotated image.  numpy.ndarray ~ (rows, columns, channels)
    """

    assert type(angle) == int, "The angle of rotation must be an integer number"
    assert (angle >= 0) & (angle < 360), "The angle of rotation must be an integer >= 0 but < 360"

    transformer = cv2.getRotationMatrix2D(centre, angle=angle, scale=1)
    return cv2.warpAffine(tensor, transformer, dimensions)
