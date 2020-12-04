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

import numpy as np
from scipy.spatial.transform import Rotation

from .utils import perspective

class Camera:
    def __init__(self, width, height):
        self.sensitivity = 0.01
        self.zoom_sensitivity = 0.1
        self.momentum = 0.93

        self._zoom = 2
        self.rot = Rotation.identity()
        self.previous_mouse_pos = None
        self.angular_velocity = None
        self.rot_around_vertical = 0
        self.rot_around_horizontal = 0
        self.resize(width, height)

    def resize(self, width, height):
        self.perspectiveMatrix = perspective(np.radians(80), width/height, 0.01, 100.0)

    def zoom(self, steps):
        self._zoom *= pow(1 - self.zoom_sensitivity, steps)

    def update(self, time, delta_time):
        if self.previous_mouse_pos is None and self.angular_velocity is not None:
            self._damping()

        self.rot = Rotation.identity()
        self.rot *= Rotation.from_rotvec(self.rot_around_horizontal * np.array([1,0,0]))
        self.rot *= Rotation.from_rotvec(self.rot_around_vertical * np.array([0,1,0]))

        viewMatrix = np.eye(4)
        viewMatrix[:3,:3] = self.rot.as_matrix()
        viewMatrix[0:3,3] = 0, 0, -self._zoom
        self.viewMatrix = viewMatrix

    def set_uniforms(self, program):
        if "uPerspectiveMatrix" in program:
            program["uPerspectiveMatrix"].write(self.perspectiveMatrix.T.astype('f4').tobytes())
        if "uViewMatrix" in program:
            program["uViewMatrix"].write(self.viewMatrix.T.astype('f4').tobytes())

    def start_rotation(self, x, y):
        self.previous_mouse_pos = x, y

    def update_rotation(self, x, y):
        if self.previous_mouse_pos is None:
            return
        sx, sy = self.previous_mouse_pos
        dx = x - sx
        dy = y - sy
        self._rotate(dx, dy)
        self.previous_mouse_pos = x, y

    def stop_rotation(self):
        self.previous_mouse_pos = None

    def _rotate(self, dx, dy):
        self.rot_around_vertical += dx * self.sensitivity
        self.rot_around_horizontal += dy * self.sensitivity
        self.rot_around_horizontal = np.clip(self.rot_around_horizontal, -np.pi / 2, np.pi / 2)
        self.angular_velocity = dx, dy

    def _damping(self):
        dx, dy = self.angular_velocity
        if dx * dx + dy * dy < 1e-6:
            self.angular_velocity = None
        else:
            self._rotate(dx * self.momentum, dy * self.momentum)
