#!/usr/bin/env python
import numpy as np

'''
convert the point in the captured image to point related to the robot base to execute grasp
'''

from robot_grasp.srv import calibration_transform
import rospy

cx=947.266;
cy=577.551;  # (cx, cy) is center of image
fx=1068.6277;
fy=1069.2988; # (fx, fy) is focal length
dz=depth=0.713;
# R, image point to camera
Intrinsic_matrix = np.array([[fx, 0, cx],
                             [0, fy, cy],
                             [0, 0, 1.0]])   
# [R | T], R is the rotation matrix from robot base to camera coordinator, T is the translation vector [dx, dy, dz] and dz  # m
Extrinsic_matrix = np.array([[0.05067265, -0.99716277, 0.05566597, -0.52],
                             -0.99558933, -0.05484203, -0.07611985, -0.59],
                              0.07895671, -0.05156326, -0.9955436, 0.713],
                              0, 0, 0, 1]])

def transform(req):
    # (xm, ym) is the point on the image, the left-up corner is (0, 0)
    xm = req.obj_real_detected_in_cam.pose[0];
    ym = req.obj_real_detected_in_cam.pose[1];
    Orientation = req.obj_real_detected_in_cam.pose[2];
    # calculate the 3-d projected point from 2-d image point
    x1 = (xm-cx)*depth/fx;
    x2 = (ym-cy)*depth/fy;
    projection_point = np.array([x1, x2, depth, 1])
    # P_robotBase = T * P_camera
    grasp_point = np.dot(Extrinsic_matrix), projection_point)
    res_obj_param = []
    res_obj_param.append(grasp_point[0])
    res_obj_param.append(grasp_point[1])
    res_obj_param.append(grasp_point[2])
    res_obj_param.append(Orientation)
    return res_obj_param;

def main():
    rospy.init_node('coordinates_transformer')
    s = rospy.Service('transform', calibration_transform, transform)
    print "Ready to do transform."
    rospy.spin()

if __name__ == "__main__":
    main()
