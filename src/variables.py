ply_header = '''ply
format ascii 1.0
element vertex %(vert_num)d
property float x
property float y
property float z
property uchar red
property uchar green
property uchar blue
end_header
'''

data_path = "../data"
disparity_path = data_path + "/disp"
point_clouds_path = data_path + "/point_clouds"
captures_path = data_path + "/captures"
depth_maps_path = data_path + "/depth_maps"
left_captures_path = captures_path + "/left"
right_captures_path = captures_path + "/right"
left_depth_maps_path = depth_maps_path + "/left"
right_depth_maps_path = depth_maps_path + "/right"
