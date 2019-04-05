from pclpy import pcl

mesh = pcl.PolygonMesh()
pcl.io.loadPLYFile("../data/point_clouds/360.ply", mesh)
point_cloud = pcl.PointCloud.PointXYZRGB()

for field in mesh.cloud:
    print(field)
