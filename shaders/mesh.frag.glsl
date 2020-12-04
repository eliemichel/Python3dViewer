#version 330

/**
 * This file is part of Python 3D Viewer
 *
 * Copyright (c) 2020 -- Élie Michel <elie.michel@exppad.com>
 * 
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to
 * deal in the Software without restriction, including without limitation the
 * rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
 * sell copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 * 
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * The Software is provided "as is", without warranty of any kind, express or
 * implied, including but not limited to the warranties of merchantability,
 * fitness for a particular purpose and non-infringement. In no event shall the
 * authors or copyright holders be liable for any claim, damages or other
 * liability, whether in an action of contract, tort or otherwise, arising
 * from, out of or in connection with the software or the use or other dealings
 * in the Software.
 */

in vec3 v_normal;
in vec3 v_position;

out vec4 f_color;

uniform vec4 uColor = vec4(1.0, 0.5, 0.1, 1.0);
uniform mat4 uViewMatrix;
uniform float uHardness = 16.0;

const vec3 lightpos0 = vec3(22.0, 16.0, 50.0);
const vec3 lightcolor0 = vec3(1.0, 0.95, 0.9);
const vec3 lightpos1 = vec3(-22.0, -8.0, -50.0);
const vec3 lightcolor1 = vec3(0.9, 0.95, 1.0);
const vec3 ambient = vec3(1.0);

void main() {
    vec3 viewpos = inverse(uViewMatrix)[3].xyz;

    // This is a very basic lighting, for visualization only //

    vec3 n = normalize(v_normal);
    vec3 c = uColor.rgb * ambient;
    vec3 v = normalize(viewpos - v_position);
    vec3 l, r;
    float s, spec;

    l = normalize(lightpos0 - v_position);
    s = max(0.0, dot(n, l));
    c += uColor.rgb * s * lightcolor0;
    if (s > 0) {
        r = reflect(-l, n);
        spec = pow(max(0.0, dot(v, r)), uHardness);
        c += spec * lightcolor0;
    }

    l = normalize(lightpos1 - v_position);
    s = max(0.0, dot(n, l));
    c += uColor.rgb * s * lightcolor1;
    if (s > 0) {
        r = reflect(-l, n);
        spec = pow(max(0.0, dot(v, r)), uHardness);
        c += spec * lightcolor1;
    }

    f_color = vec4(c * 0.5, uColor.a);
}
