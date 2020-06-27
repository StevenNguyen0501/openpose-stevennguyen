import math

import numpy as np


def is_correct_pose(pose):
    """
    Check the correction of pose, return true when pose was correct
    :param pose:list of tuple
    :return:bool
    """

    def corner(A1, A2, B1, B2):
        u = (A2[0] - A1[0], A2[1] - A1[1])
        v = (B2[0] - B1[0], B2[1] - B1[1])
        return math.acos((u[0] * v[0] + u[1] * v[1]) / (np.hypot(u[0], u[1]) * np.hypot(v[0], v[1]))) * 180 / math.pi

    def distance_of_two_points(point_1, point_2):
        return math.sqrt((point_1[0] - point_2[0]) ** 2 + (point_1[1] - point_2[1]) ** 2)

    MIN_ELBOW_CORNER = 120
    MIN_REVERSE_ARM_CORNER = 85
    MIN_REVERSE_HIPS_CORNER = 75
    MIN_KNEE_CORNER = 135
    left_elbow_corner = corner(pose[1], pose[2], pose[3], pose[2])
    right_elbow_corner = corner(pose[4], pose[5], pose[6], pose[5])
    left_reverse_armpit_corner = corner(pose[4], pose[1], pose[2], pose[1])
    right_reverse_armpit_corner = corner(pose[1], pose[4], pose[5], pose[4])
    if left_elbow_corner <= MIN_ELBOW_CORNER or right_elbow_corner <= MIN_ELBOW_CORNER:
        return False
    if left_reverse_armpit_corner <= MIN_REVERSE_ARM_CORNER or right_reverse_armpit_corner <= MIN_REVERSE_ARM_CORNER:
        return False
    if pose[2][1] <= pose[1][1] or pose[5][1] <= pose[4][1]:
        return False
    if corner(pose[1], pose[4], (pose[4][0], 0), pose[4]) <= 45 or corner(pose[1], pose[4], (pose[4][0], 0),
                                                                          pose[4]) >= 135:
        return False
    left_reverse_hips_corner = corner(pose[8], pose[7], pose[9], pose[7])
    right_reverse_hips_corner = corner(pose[7], pose[8], pose[11], pose[8])
    left_knee_corner = corner(pose[7], pose[9], pose[10], pose[9])
    right_knee_corner = corner(pose[8], pose[11], pose[12], pose[11])
    if left_reverse_hips_corner <= MIN_REVERSE_HIPS_CORNER or right_reverse_hips_corner <= MIN_REVERSE_HIPS_CORNER:
        return False
    if left_knee_corner <= MIN_KNEE_CORNER or right_knee_corner <= MIN_KNEE_CORNER:
        return False
    # too short
    shoulder_distance = distance_of_two_points(pose[1], pose[4])
    hips_distance = distance_of_two_points(pose[7], pose[8])
    if distance_of_two_points(pose[1], pose[2]) <= 0.6 * shoulder_distance or distance_of_two_points(pose[4], pose[
        5]) <= 0.6 * shoulder_distance:
        return False
    if distance_of_two_points(pose[2], pose[3]) <= 0.6 * shoulder_distance or distance_of_two_points(pose[5], pose[
        6]) <= 0.6 * shoulder_distance:
        return False
    if distance_of_two_points(pose[7], pose[9]) <= hips_distance or distance_of_two_points(pose[8],
                                                                                           pose[11]) <= hips_distance:
        return False
    if distance_of_two_points(pose[10], pose[9]) <= 0.8 * hips_distance or distance_of_two_points(pose[12], pose[
        11]) <= 0.8 * hips_distance:
        return False
    if distance_of_two_points(pose[1], pose[2]) * 0.5 >= shoulder_distance or distance_of_two_points(pose[4], pose[
        5]) * 0.5 >= shoulder_distance:
        return False

    return True


def is_the_pose_valid(body_pose):
    """
    Check the correction of pose and return processed pose. 4 case - 4 code message
    0 : Correct pose. Return body pose, code message
    1 : Missing parts of body or found no person. Return None, code message
    2 : Incorrect pose. Return None, code message
    3 : Too many person found. Return None, code message

    :param body_pose: origin output of pose key points (25 pair keys)
    :return: message, boolean (code message), list of tuple (body pose)
    """
    is_valid = False
    if len(body_pose) != 1:
        # Knock out!
        if len(body_pose) >= 2:
            return (
                       "The model you've uploaded has too many people in it, "
                       "for better experiment please follow the instruction from upload model"), is_valid, None
        else:
            return (
                       "The model you've uploaded missing some parts of their body, "
                       "for better experiment please follow the instruction from upload model"), is_valid, None
    else:
        # passed round 1!
        def add_point(point):
            x = int(point[0])
            y = int(point[1])
            if x == 0 and y == 0:
                return None
            else:
                return (x, y)

        nail = [1, 2, 3, 4, 5, 6, 7, 9, 12, 10, 11, 13, 14]
        body_points = []
        for i in nail:
            p = add_point(body_pose[0][i])
            if p is None:
                return (
                           "The model you've uploaded missing some parts of their body, "
                           "for better experiment please follow the instruction from upload model"), is_valid, None
            body_points.append(p)
        if is_correct_pose(body_points):
            # passed round 2!
            nail_2 = [19, 20, 21, 22, 23, 24, 0, 15, 16, 17, 18]
            for i in nail_2:
                body_points.append(add_point(body_pose[0][i]))

            return "successful", True, body_points  # passed all tests
        else:
            return (
                       "The model you've uploaded does not follow the correct pose as we suggested, "
                       "for better experiment please follow the instruction from upload model"), is_valid, None
