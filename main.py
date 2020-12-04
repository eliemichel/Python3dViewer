# This file is part of Python 3D Viewer
#
# Copyright (c) 2020 -- Élie Michel <elie.michel@exppad.com>
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# The Software is provided "as is", without warranty of any kind, express or
# implied, including but not limited to the warranties of merchantability,
# fitness for a particular purpose and non-infringement. In no event shall the
# authors or copyright holders be liable for any claim, damages or other
# liability, whether in an action of contract, tort or otherwise, arising
# from, out of or in connection with the software or the use or other dealings
# in the Software.

import moderngl
import struct
import glfw
import imgui
import numpy as np

from augen import App, Camera
from augen.mesh import ObjMesh, RenderedMesh

class MyApp(App):
    def init(self):
        ctx = self.ctx
        # Load a mesh
        self.mesh = ObjMesh("sample-data/dragon.obj")

        # Load the glsl program
        self.program = ctx.program(
            vertex_shader=open("shaders/mesh.vert.glsl").read(),
            fragment_shader=open("shaders/mesh.frag.glsl").read(),
        )

        # Create the rendered mesh from the mesh and the program
        self.rendered_mesh = RenderedMesh(ctx, self.mesh, self.program)

        # Setup camera
        w, h = self.size()
        self.camera = Camera(w, h)

        # Initialize some value used in the UI
        self.some_slider = 0.42

    def update(self, time, delta_time):
        # Update damping effect (and internal matrices)
        self.camera.update(time, delta_time)

    def render(self):
        ctx = self.ctx
        self.camera.set_uniforms(self.program)

        ctx.screen.clear(1.0, 1.0, 1.0, -1.0)

        ctx.enable_only(moderngl.DEPTH_TEST | moderngl.CULL_FACE)
        self.rendered_mesh.render(ctx)

    def on_key(self, key, scancode, action, mods):
        if key == glfw.KEY_ESCAPE:
            self.should_close()

    def on_mouse_move(self, x, y):
        self.camera.update_rotation(x, y)

    def on_mouse_button(self, button, action, mods):
        if action == glfw.PRESS and button == glfw.MOUSE_BUTTON_LEFT:
            x, y = self.mouse_pos()
            self.camera.start_rotation(x, y)
        if action == glfw.RELEASE and button == glfw.MOUSE_BUTTON_LEFT:
            self.camera.stop_rotation()

    def on_resize(self, width, height):
        self.camera.resize(width, height)
        self.ctx.viewport = (0, 0, width, height)

    def on_scroll(self, x, y):
        self.camera.zoom(y)

    def ui(self):
        """Use the imgui module here to draw the UI"""
        if imgui.begin_main_menu_bar():
            if imgui.begin_menu("File", True):

                clicked_quit, selected_quit = imgui.menu_item(
                    "Quit", 'Esc', False, True
                )

                if clicked_quit:
                    self.should_close()

                imgui.end_menu()
            imgui.end_main_menu_bar()

        imgui.begin("Hello, world!", True)
        self.shape_need_update = False
        changed, self.some_slider = imgui.slider_float(
            "Some Slider", self.some_slider,
            min_value=0.0, max_value=1.0,
            format="%.02f"
        )
        imgui.end()

def main():
    app = MyApp(1280, 720, "Python 3d Viewer - Elie Michel")
    app.main_loop()

if __name__ == "__main__":
    main()

