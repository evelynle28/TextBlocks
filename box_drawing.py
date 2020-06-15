import cv2
from math import *
import numpy as np
from scipy.ndimage.measurements import label

def get_boxes(label, num_components, positions, input_image):
    '''
    Retrieve bounding boxes from the marked connected components
    '''
    boxes = []

    min_area = 300 #threshold for the bounding boxes

    for i in range(1,num_components+1):

        # Recreate the image from the connected component to retrieve
        # the contours for the component
        img = recreate_img(positions[label == i], input_image.shape)
        contours = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[0]

        if len(contours) == 0:
            continue

        contour = contours[0]
        rect = cv2.minAreaRect(contour)
        w, h = rect[1]
        box = reorder_points(np.int0(cv2.boxPoints(rect)))

        # Ensure that the rectangle meets the minimum threshold
        # to avoid noises
        if w * h < min_area:
            continue

        boxes.append(box)

    return boxes

def recreate_img(marked_pixels, original_dims):
    '''
    Create an image from the given points to help
    find contour on a given component
    '''
    h, w = original_dims[:2]
    img = np.zeros((h, w, 3), np.uint8)

    for coor in marked_pixels:
        x, y = coor
        img[x, y] = [0, 255, 0]

    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    return img

def reorder_points (rectangle):
    '''
    Reorder the box points into the clockwise order:
        > top-left, top-right, bottom-right, bottom-left
    '''
    #Sort by x-coordinates
    sortByX = rectangle[np.argsort(rectangle[:,0]),:]
    leftSorted = sortByX[:2,:]
    rightSorted = sortByX[2:,:]

    #Sort by y-coordinates
    leftSorted = leftSorted[np.argsort(leftSorted[:,1]),:]
    (tl, bl) = leftSorted

    rightSorted = rightSorted[np.argsort(rightSorted[:,1]),:]
    (tr, br) = rightSorted

    return np.array([tl, tr, br, bl], dtype="int32")

def should_merge(box1, box2):
    '''
    Check if 2 boxes are close, vertically and horizontally,
    and determine if they should be merged
    '''

    tl1 = box1[0]
    br1 = box1[2]
    tl2 = box2[0]
    br2 = box2[2]

    horizontal_thres = 5
    vertical_thres = 5

    # Check if they are vertically near each other
    near_vertical = abs(tl1[1] - br2[1]) < vertical_thres \
                         or abs(br1[1] - tl2[1]) < vertical_thres

    # Check if they are horizontally near each other
    near_horizontal = abs(br1[0] - tl2[0]) < horizontal_thres \
                            or abs(br2[0] - tl1[0]) < horizontal_thres

    # Check if they are aligned to avoid merging from 2 opposite quadrants
    diag1 = sqrt(((tl1[0] - br1[0])**2 + (tl1[1] - br1[1])**2))
    diag2 = sqrt(((tl1[0] - br1[0])**2 + (tl1[1] - br1[1])**2))
    cross_diag = sqrt(((tl1[0] - tl2[0])**2 + (tl1[1] - tl2[1])**2))

    if cross_diag > 1.2 * max(diag1, diag2):
        return False
    else:
        return (near_horizontal or near_vertical)

def merge(box1, box2):
    '''
    Determine whether or not 2 boxes need to be merged
    Check if they are overlap or near each other at a certain distance
     and create a new bounding box that merge the given two if needed
    '''
    tl1 = box1[0]
    br1 = box1[2]
    tl2 = box2[0]
    br2 = box2[2]

    overlap_area = 0

    # If 2 boxes meet one of these conditions, they do not overlap
    # each other but still can be close neighbor
    if (tl1[0] > br2[0] or tl2[0] > br1[0]) \
        or (tl1[1] > br2[1] or tl2[1] > br1[1]):

        if should_merge(box1, box2):
            return True, mergeBox(box1, box2)
        else:
            return False, None

    else:
        # Calculate their overlap area to see
        # if they are good for merging
        overlap_area = abs((min(br1[0], br2[0]) - max(tl1[0], tl2[0])) \
                             * (min(br1[1], br2[1]) - max(tl1[1], tl2[1])))

        area1 = abs((br1[0] - tl1[0]) * (br1[1] - tl1[1]))
        area2 = abs((br2[0] - tl2[0]) * (br2[1] - tl2[1]))

        thres = 0.1

        # Combine 2 boxes if the overlap exceeds the threshold
        if overlap_area/area1 > thres or overlap_area/area2 > thres:
            return True, mergeBox(box1,box2)
        else:
            # Otherwise, depends on their relationship to each
            # other to decide should they be combined
            if should_merge(box1, box2):
                return True, mergeBox(box1, box2)
            else:
                return False, None

def mergeBox(box1, box2):
    '''
    Combine 2 given boxes and return a new bounding box
    that cover both of the given space bounded
    '''
    new_box = []

    #top-left
    new_box.append([min(box1[0][0], box2[0][0]), min(box1[0][1], box2[0][1])])

    #top-right
    new_box.append([max(box1[1][0], box2[1][0]), min(box1[1][1], box2[1][1])])

    #bottom-right
    new_box.append([max(box1[2][0], box2[2][0]), max(box1[2][1], box2[2][1])])

    #bottom-left
    new_box.append([min(box1[3][0], box2[3][0]), max(box1[3][1], box2[3][1])])

    return  reorder_points(np.asarray(new_box))

def minimize_box_num(boxes):
    '''
    Minimize the number of boxes to draw by determine
    if they should be merged together or if there is
    any duplicate that needs to be removed.

    Return the minimal number of boxes that need to draw
    '''
    # List of boxes that have already been merged together
    merge_marks = [0] * len(boxes)
    mergeOnce = True

    while mergeOnce:
        mergeOnce = False
        total_boxes = len(boxes)

        for i in range(total_boxes - 1):
            if mergeOnce:
                break

            if (merge_marks[i] == 1):
                continue

            for j in range(i + 1, total_boxes):
                if (merge_marks[j] == 1):
                    continue

                merged, new_box = merge(boxes[i], boxes[j])

                if merged:
                    mergeOnce = True
                    merge_marks[i] = 1
                    merge_marks[j] = 1

                    boxes.append(new_box)
                    merge_marks.append(0)
                    break


    unique_boxes = []
    for i, box in enumerate(boxes):
        if merge_marks[i] == 0:
            unique_boxes.append(box)

    return unique_boxes






