import cv2 as cv
import os

from src.point_cloud_builder import PointCloudBuilder
from src.scanner_simulator import ScannerSimulatorApp

data_path = "../data"
point_clouds_path = data_path + "/point_clouds"
captures_path = data_path + "/captures"
left_captures_path = captures_path + "/left"
right_captures_path = captures_path + "/right"

scanner_simulator = ScannerSimulatorApp(left_captures_path, right_captures_path)
scanner_simulator.run()

cloud_builder = PointCloudBuilder()

file_names = os.listdir(left_captures_path)
for file_name in file_names:
    left_path = "{}/{}".format(left_captures_path, file_name)
    right_path = "{}/{}".format(right_captures_path, file_name)

    ply_file_name = file_name.split(".")[0] + ".ply"
    ply_path = "{}/{}".format(point_clouds_path, ply_file_name)

    # TODO: Compress images with 'cv.pyrDown'
    img_left = cv.imread(left_path)
    img_right = cv.imread(right_path)

    cloud_builder.build_point_cloud(img_left, img_right, ply_path)
