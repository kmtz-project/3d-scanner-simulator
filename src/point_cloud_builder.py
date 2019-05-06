import math
import cv2 as cv
import numpy as np


class PointCloudBuilder:
    def build_point_cloud_by_disparity(self, img, disparity_map):
        fx, cx, fy, cy = 1274.8875758012014, 637.7988145297046, 1262.6746085506568, 359.85906609832153
        cam_baseline = 61
        z_max = 2000

        # Crop image
        img_crop = img.shape[1] - disparity_map.shape[1]
        img = img[:, img_crop:]

        points = np.zeros(shape=img.shape)
        colors = np.zeros(shape=img.shape)

        for i in range(0, points.shape[0]):
            for j in range(0, points.shape[1]):
                disp = disparity_map[i][j]
                if disp > 0:
                    z = fx * cam_baseline / disp
                    if z < z_max:
                        points[i][j] = [z * (j - cx) / fx, -(z * (i - cy) / fy), z]
                        colors[i][j] = img[i][j]

        return points, colors

    def build_point_cloud_by_disparity_obsolete(self, img, disparity_map):
        h, w = disparity_map.shape[:2]
        f = 0.8 * w
        Q = np.float32([[1, 0, 0, -0.5 * w],
                        [0, -1, 0, 0.5 * h],
                        [0, 0, 0, -f],
                        [0, 0, 1, 0]])

        # Crop image
        img_crop = img.shape[1] - disparity_map.shape[1]
        img = img[:, img_crop:]

        points = cv.reprojectImageTo3D(disparity_map, Q)
        colors = cv.cvtColor(img, cv.COLOR_BGR2RGB)

        return points, colors

    def build_point_cloud_by_depth(self, img_left, depth_map):
        points = np.zeros((720, 1280, 3), np.float32)

        depth_map = depth_map / depth_map.max() * 1280

        cam_pos_x = depth_map.shape[1] / 2
        cam_pos_y = depth_map.shape[0] / 2
        for x in range(0, depth_map.shape[0]):
            for y in range(0, depth_map.shape[1]):
                dist = depth_map[x][y]
                z = 0 + math.sqrt(abs(dist**2 - (x - cam_pos_x)**2 - (y - cam_pos_y)**2))
                depth_map[x][y] = z
                points[x][y] = [x, y, z]

        points = points / points.max() * 255
        colors = cv.cvtColor(img_left, cv.COLOR_BGR2RGB)

        return points, colors
