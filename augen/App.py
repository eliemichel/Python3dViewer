# This file is part of PyAugen
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

import glfw
import moderngl
import imgui
from imgui.integrations.glfw import GlfwRenderer as ImguiRenderer

class App:
    def __init__(self, width = 640, height = 480, title = "Hello world"):
        imgui.create_context()

        if not glfw.init():
            return
        
        self.window = glfw.create_window(width, height, title, None, None)
        if not self.window:
            glfw.terminate()
            return

        glfw.make_context_current(self.window)
        self.ctx = moderngl.create_context(require=460)

        self.impl = ImguiRenderer(self.window, attach_callbacks=False)
        
        glfw.set_key_callback(self.window, self._on_key)
        glfw.set_cursor_pos_callback(self.window, self._on_mouse_move)
        glfw.set_mouse_button_callback(self.window, self._on_mouse_button)
        glfw.set_window_size_callback(self.window, self._on_resize)
        glfw.set_char_callback(self.window, self._on_char)
        glfw.set_scroll_callback(self.window, self._on_scroll)

        self.init()

    def main_loop(self):
        previous_time = glfw.get_time()

        # Loop until the user closes the window
        while not glfw.window_should_close(self.window):
            glfw.poll_events()
            self.impl.process_inputs()

            current_time = glfw.get_time()
            delta_time = current_time - previous_time
            previous_time = current_time
            self.update(current_time, delta_time)
            self.render()

            imgui.new_frame()
            self.ui()
            imgui.render()
            self.impl.render(imgui.get_draw_data())

            glfw.swap_buffers(self.window)

        self.impl.shutdown()
        glfw.terminate()

    def should_close(self):
        glfw.set_window_should_close(self.window, True)

    def mouse_pos(self):
        return glfw.get_cursor_pos(self.window)

    def size(self):
        return glfw.get_window_size(self.window)

    def init(self):
        pass

    def update(self, time):
        pass

    def render(self):
        pass

    def ui(self):
        pass

    def _on_key(self, window, key, scancode, action, mods):
        self.impl.keyboard_callback(window, key, scancode, action, mods)
        self.on_key(key, scancode, action, mods)

    def on_key(self, key, scancode, action, mods):
        pass

    def _on_char(self, window, codepoint):
        self.impl.char_callback(window, codepoint)
        self.on_char(codepoint)

    def on_char(self, codepoint):
        pass

    def _on_mouse_move(self, window, x, y):
        self.impl.mouse_callback(window, x, y)
        self.on_mouse_move(x, y)

    def on_mouse_move(self, x, y):
        pass

    def _on_mouse_button(self, window, button, action, mods):
        if not imgui.get_io().want_capture_mouse:
            self.on_mouse_button(button, action, mods)

    def on_mouse_button(self, button, action, mods):
        pass

    def _on_scroll(self, window, xoffset, yoffset):
        self.impl.scroll_callback(window, xoffset, yoffset)
        self.on_scroll(xoffset, yoffset)

    def on_scroll(self, xoffset, yoffset):
        pass

    def _on_resize(self, window, width, height):
        self.impl.resize_callback(window, width, height)
        self.on_resize(width, height)

    def on_resize(self, width, height):
        pass
