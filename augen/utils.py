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

def _perspective(n, f, t, b, l, r):
    return np.array([
        [ 2*n/(r-l),     0    ,   (r+l)/(r-l) ,       0        ],
        [     0    , 2*n/(t-b),   (t+b)/(t-b) ,       0        ],
        [     0    ,     0    , -((f+n)/(f-n)), -(2*n*f/(f-n)) ],
        [     0    ,     0    ,       -1      ,       0        ],
    ])

def perspective(fovy, aspect, near, far):
    top = near * np.tan(fovy / 2)
    right = top * aspect
    return _perspective(near, far, top, -top, -right, right)
