import cv2 as cv
import numpy as np


class DisparityCalculator:
    def get_disparity_map(self, img_left, img_right):
        window_size = 3
        min_disp = 0
        num_disp = 96
        left_matcher = cv.StereoSGBM_create(
            minDisparity=min_disp,
            numDisparities=num_disp,
            blockSize=2,
            uniquenessRatio=15,
            speckleWindowSize=0,
            speckleRange=2,
            P1=8 * 3 * window_size ** 2,
            P2=32 * 3 * window_size ** 2,
            mode=cv.STEREO_SGBM_MODE_SGBM_3WAY
        )

        right_matcher = cv.ximgproc.createRightMatcher(left_matcher)

        lmbda = 80000  # 80000
        sigma = 2.8    # 1.2

        wls_filter = cv.ximgproc.createDisparityWLSFilter(matcher_left=left_matcher)
        wls_filter.setLambda(lmbda)
        wls_filter.setSigmaColor(sigma)

        disp_left = left_matcher.compute(img_left, img_right)
        disp_left = np.int16(disp_left)
        disp_right = right_matcher.compute(img_right, img_left)
        disp_right = np.int16(disp_right)

        filtered_img = wls_filter.filter(disp_left, img_left, None, disp_right)
        filtered_img = filtered_img[:, 100:] # Crop image
        filtered_img = cv.normalize(src=filtered_img, dst=filtered_img, beta=0, alpha=255, norm_type=cv.NORM_MINMAX)
        filtered_img = np.uint8(filtered_img)

        return filtered_img
