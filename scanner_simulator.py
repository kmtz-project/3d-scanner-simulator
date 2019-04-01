import math

from direct.showbase.ShowBase import ShowBase, PandaNode
from direct.task import Task
from panda3d.core import Filename, Camera, WindowProperties


class ScannerSimulatorApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        self.__init_cameras__()
        self.__init_window__()
        self.__init_scene__()

        # Run rotation task
        self.rotation_angle = 0
        self.task_mgr.add(self.rotation_task, "rotation_task")

    def __init_cameras__(self):
        # Disable current active camera
        self.cam.node().set_active(False)

        # Create rotating platform for cameras
        self.cameras_base = self.render.attach_new_node("cameras_base")
        self.cameras_base.set_pos(0, 0, 1.5)

        # Create and init left camera
        left_camera = self.cameras_base.attach_new_node(Camera("left"))
        left_camera.set_name("left_camera")
        left_camera.set_pos(0, -0.5, 0)
        self.left_display_region = self.win.make_display_region(0, 0.5, 0, 1)
        self.left_display_region.set_camera(left_camera)

        # Create and init right camera
        right_camera = self.cameras_base.attach_new_node(Camera("right"))
        right_camera.set_name("right_camera")
        right_camera.set_pos(0, 0.5, 0)
        self.right_display_region = self.win.make_display_region(0.5, 1, 0, 1)
        self.right_display_region.set_camera(right_camera)

    def __init_window__(self):
        # Remove current display region
        display_region = self.cam.node().get_display_region(0)
        self.win.remove_display_region(display_region)

        # Change window size
        props = WindowProperties()
        props.set_size(2 * 1920, 1080)
        self.win.request_properties(props)

    def __init_scene__(self):
        # Create parent nodes
        scene = self.render.attach_new_node(PandaNode("scene"))
        boxes = scene.attach_new_node(PandaNode("boxes"))

        # Instantiate box model prefab
        box = self.loader.load_model("models/box")
        box.reparent_to(boxes)

        # Instantiate copies of box model
        box_number = 10
        angle_step = 2 * math.pi / box_number
        radius = 10
        for i in range(box_number):
            placeholder = boxes.attach_new_node("box_{}".format(i))
            placeholder.set_pos(radius * math.cos(i * angle_step), radius * math.sin(i * angle_step), 0)
            box.instance_to(placeholder)

        # Destroy box model prefab
        box.remove_node()


    def rotation_task(self, task):
        if self.rotation_angle > 360:
            return Task.exit

        # Rotate cameras platform
        self.cameras_base.set_hpr(self.rotation_angle, 0, 0)

        # Save snapshot from left camera
        file_path = "cam_left_{}.png".format(self.rotation_angle)
        self.left_display_region.save_screenshot(Filename(file_path))

        # Save snapshot from right camera
        file_path = "cam_right_{}.png".format(self.rotation_angle)
        self.right_display_region.save_screenshot(Filename(file_path))

        self.rotation_angle += 15

        return Task.cont


app = ScannerSimulatorApp()
app.run()
