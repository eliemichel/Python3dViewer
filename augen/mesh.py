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
from moderngl import TRIANGLES

class Mesh:
    """Simply contains an array of triangles and an array of normals.
    Could be enhanced, for instance with an element buffer"""
    def __init__(self, P, N):
        self.P = P
        self.N = N


class ObjMesh(Mesh):
    """An example of mesh loader, using the pywavefront module.
    Only load the first mesh of the file if there are more than one."""
    def __init__(self, filepath):
        import pywavefront
        print(f"Loading mesh from {filepath}...")
        scene = pywavefront.Wavefront(filepath)
        for name, material in scene.materials.items():
            assert(material.vertex_format == "N3F_V3F")  # T2F, C3F, N3F and V3F may appear in this string
            data = np.array(material.vertices).reshape(-1, 6)
            self.P = data[:,3:]
            self.N = data[:,:3]
            break
        print(f"(Object has {len(self.P)//3} points)")


class RenderedMesh:
    """The equivalent of a Mesh, but stored in OpenGL buffers (on the GPU)
    ready to be rendered."""
    def __init__(self, ctx, mesh, program):
        self.mesh = mesh
        self.vboP = ctx.buffer(mesh.P.astype('f4').tobytes())
        self.vboN = ctx.buffer(mesh.N.astype('f4').tobytes())
        self.vao = ctx.vertex_array(
            program,
            [
                (self.vboP, "3f", "in_vert"),
                (self.vboN, "3f", "in_normal"),
            ]
        )

    def release(self):
        self.vboP.release()
        self.vboN.release()
        self.vao.release()

    def render(self, ctx):
        self.vao.render(TRIANGLES)
