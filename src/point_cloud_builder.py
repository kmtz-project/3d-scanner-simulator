import cv2 as cv
import numpy as np


class PointCloudBuilder:
    def build_point_cloud(self, img_left, disparity_map):
        h, w = disparity_map.shape[:2]
        f = 0.8 * w
        Q = np.float32([[1, 0, 0, -0.5 * w],
                        [0, -1, 0, 0.5 * h],
                        [0, 0, 0, -f],
                        [0, 0, 1, 0]])
        points = cv.reprojectImageTo3D(disparity_map, Q)
        colors = cv.cvtColor(img_left, cv.COLOR_BGR2RGB)

        return points, colors
