import shutil

from direct.showbase.ShowBase import ShowBase, PandaNode
from panda3d.core import Filename, Camera, WindowProperties, Material


class ScannerSimulatorApp(ShowBase):
    def __init__(self, left_output_path="", right_output_path=""):
        ShowBase.__init__(self)

        self.left_output_path = left_output_path
        self.right_output_path = right_output_path

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
        self.cameras_base.set_pos(0, 0, 2)

        # Create and init left camera
        left_camera = self.cameras_base.attach_new_node(Camera("left"))
        left_camera.set_name("left_camera")
        left_camera.set_pos(0, -0.1, 0)
        self.left_display_region = self.win.make_display_region(0, 0.5, 0, 1)
        self.left_display_region.set_camera(left_camera)

        # Create and init right camera
        right_camera = self.cameras_base.attach_new_node(Camera("right"))
        right_camera.set_name("right_camera")
        right_camera.set_pos(0, 0.1, 0)
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
        room = scene.attach_new_node(PandaNode("room"))

        floor = self.loader.load_model("../data/models/room_01/floor.egg")
        tex = self.loader.load_texture("../data/models/room_01/tex/floor.jpg")
        floor.set_texture(tex)
        floor.set_scale(1000, 1000, 1000)
        floor.reparent_to(room)

        skybox = self.loader.load_model("../data/models/room_01/skybox.egg")
        tex = self.loader.load_texture("../data/models/room_01/tex/skybox.jpg")
        skybox.set_texture(tex)
        skybox.set_scale(15000, 15000, 15000)
        skybox.reparent_to(room)

        material = Material()
        # material.set_shininess(5.0)
        material.set_metallic(5)
        box_01 = self.loader.load_model("../data/models/room_01/box_01.egg")
        box_01.set_material(material)
        tex = self.loader.load_texture("../data/models/room_01/tex/box_tex.jpg")
        box_01.set_texture(tex)
        box_01.set_pos(20, 0, 0)
        box_01.reparent_to(room)

        box_02 = self.loader.load_model("../data/models/room_01/box_02.egg")
        box_02.set_material(material)
        tex = self.loader.load_texture("../data/models/room_01/tex/box_tex_2.jpg")
        box_02.set_texture(tex)
        box_02.set_pos(-14, 10, 0)
        box_02.reparent_to(room)

        # # Instantiate object model prefab
        # obj = self.loader.load_model("../data/models/box_01/box_01.egg")
        # tex = self.loader.load_texture("../data/models/box_01/tex/box_tex.jpg")
        # obj.set_texture(tex)
        # obj.reparent_to(objects)
        #
        # # Instantiate copies of model
        # obj_number = 10
        # angle_step = 2 * math.pi / obj_number
        # radius = 10
        # for i in range(obj_number):
        #     placeholder = objects.attach_new_node("obj_{}".format(i))
        #     placeholder.set_pos(radius * math.cos(i * angle_step), radius * math.sin(i * angle_step), 0)
        #     obj.instance_to(placeholder)
        #
        # # Destroy box model prefab
        # obj.remove_node()


    def rotation_task(self, task):
        if task.time < 0.04:
            return task.cont

        if self.rotation_angle > 360:
            return task.exit

        # Rotate cameras platform
        self.cameras_base.set_hpr(self.rotation_angle, 0, 0)

        file_name = "{0:0=3d}.png".format(self.rotation_angle)

        # Save snapshot from left camera
        self.left_display_region.save_screenshot(Filename(file_name))
        file_path = "{}/{}".format(self.left_output_path, file_name)
        shutil.move(file_name, file_path)

        # Save snapshot from right camera
        self.right_display_region.save_screenshot(Filename(file_name))
        file_path = "{}/{}".format(self.right_output_path, file_name)
        shutil.move(file_name, file_path)

        self.rotation_angle += 15

        return task.cont
