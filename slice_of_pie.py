import numpy as np
from warnings import warn


def slice_of_pie(matrix, phi_1, phi_2, r_1=0, r_2=np.inf, center=False):
    """isolates the sclice of an image using polar coordinates
    Prerequisites: numpy
    Parameters:
        matrix:2D ndarray: input matrix as 2D numpy array (your input image)
        r_1:float: the length in pixels of the min radius
        r_2:float: the length in pixels of the max radius
        center:(float, float): tuple of coordinates of the center
        phi_1:float: start value in degrees
        phi_2:float: end value in degrees
        (the angle is measured from 0 to 360, starting from 6 o'clock counter clockwise)
        Note: You have to remember that numpy matrix indexes start from upper left corner
        Consequently, our positive quadrant is on the lower right
    Output:
        slice:masked 2D ndarray: the same imput matrix with all the values but the slice masked

    Example:
        Say you want to keep only the values of the given matrix
        inside the area 10°-45°, r<60:

        # initialize some basic matrix:
        my_matrix = np.zeros((150,200))
        # define the slice:
        my_slice = slice_of_pie(my_matrix, 10, 45, r_max=60)
        # show the result:
        plt.imshow(my_slice)
        """
    
    # Transforming negative angles into positive:
    if phi_1 < 0:
        phi_1 += 360
        if phi_2 == 0:
            phi_2 = 360
    if phi_2 < 0:
        phi_2 += 360

    def _angle_condition(alpha, phi_1=phi_1, phi_2=phi_2):
        '''specifies the condition to be satisfied by the angle value
        depending on the relative input values of phi_1 and phi_2
        Example:
            phi_1 = -20
            phi_2 = 20
            We suppose that the user wanted to isolate the 40° slice
            and not the 320° slice.
            '''
        if phi_1 > phi_2:
            return ((alpha > phi_1) | (alpha < phi_2)) # bitwise logical OR
        else:
            return ((alpha > phi_1) & (alpha < phi_2)) # bitwise logical AND

    M, N = matrix.shape
    if type(center) == tuple and ((center[0] <= M) & (center[1] <= N)):
        img_cen = center
    elif center:
        raise ValueError('Your center needs to be a tuple of coordinates inside the image')
    elif center == False:
        img_cen = ((M-1)/2, (N-1)/2) # IMPORTANT: The center of the image
    furthest_point = np.sqrt((max(img_cen[0], M-img_cen[0]))**2 +
                             (max(img_cen[1], N-img_cen[1]))**2)
    # Checking if the values are valid:
    if not ((r_2 > r_1) and (r_1 >= 0)):
        raise ValueError('You must have "0 <= r_1 < r_2"')
    if r_1 > furthest_point:
        warn("Check your r_1 value, you risk getting an empty image")
    x, y = np.mgrid[0:M, 0:N]
    X = x - img_cen[0] # New X from the center of the image
    Y = y - img_cen[1]
    Z = X + 1j*Y
    PHI = np.angle(Z, deg=True)
    # in order to have values from 0 to 360 instead from -180 to +180 as given by default:
    PHI += 180 * (1 - np.sign(PHI))
    
    # here follows the definition of the radius condition:
    R = np.abs(Z)
    def _radius_condition(radius, r_1=r_1, r_2=r_2):
        return ((radius < r_2) & (radius > r_1))

    slice_mask = _angle_condition(PHI) & _radius_condition(R) # combining the conditions on angle and radius
    return np.ma.masked_array(matrix, mask=np.logical_not(slice_mask))
