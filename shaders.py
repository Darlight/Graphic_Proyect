from tezt import *
from math_functions import *
import random



def psychedelic(render, **kwargs):
    u, v, w = kwargs['barycentric']
    ta, tb, tc = kwargs['texCoords']
    na, nb, nc = kwargs['normals']
    b, g, r = kwargs['color']

    b /= 255
    g /= 255
    r /= 255

    if render:
        tx = ta.x * u + tb.x * v + tc.x * w
        ty = ta.y * u + tb.y * v + tc.y * w
        texColor = render.activeT.getColor(tx, ty)
        b *= texColor[0] / 255
        g *= texColor[1] / 255
        r *= texColor[2] / 255

    nx = na[0] * u + nb[0] * v + nc[0] * w
    ny = na[1] * u + nb[1] * v + nc[1] * w
    nz = na[2] * u + nb[2] * v + nc[2] * w

    normal = V3(nx, ny, nz)

    intensity = dot(normal, render.light)
    if intensity >0:
        if intensity > 0.95:
            r *= 0.7 * intensity
        elif intensity > 0.9:
            g *= 0.7 * intensity
        elif intensity > 0.85:
            b *= 0.7 * intensity
        elif intensity > 0.8:
            r *= 0.5 * intensity

        elif intensity > 0.75:
            g *= 0.5 * intensity

        elif intensity > 0.7:
            b *= 0.5 * intensity

        elif intensity > 0.65:
            r *= 0.25 * intensity

        elif intensity > 0.6:
            g *= 0.25 * intensity

        elif intensity > 0.55:
            b *= 0.25 * intensity

        elif intensity > 0.5:
            r *= 0.12 * intensity

        elif intensity > 0.4:
            g *= 0.12 * intensity

        elif intensity > 0.3:
            b *= 0.12 * intensity

        elif intensity > 0.2:
            r *= 0.6 * intensity

        elif intensity > 0.1:
            g *= 0.6 * intensity

        elif intensity >= 0.0:
            b *= 0.6 * intensity
    b *= intensity
    g *= intensity
    r *= intensity

    if intensity > 0:
        return r, g, b
    else:
        return 0, 0, 0


def intense(render, **kwargs):
    u, v, w = kwargs['barycentric']
    ta, tb, tc = kwargs['texCoords']
    na, nb, nc = kwargs['normals']
    b, g, r = kwargs['color']

    b /= 255
    g /= 255
    r /= 255

    if render:
        tx = ta.x * u + tb.x * v + tc.x * w
        ty = ta.y * u + tb.y * v + tc.y * w
        texColor = render.activeT.getColor(tx, ty)
        b *= texColor[0] / 255
        g *= texColor[1] / 255
        r *= texColor[2] / 255

    nx = na[0] * u + nb[0] * v + nc[0] * w
    ny = na[1] * u + nb[1] * v + nc[1] * w
    nz = na[2] * u + nb[2] * v + nc[2] * w

    normal = V3(nx, ny, nz)

    intensity = dot(normal, render.light)
    if intensity >0:
        if intensity > 0 and intensity < 0.25:
            intensity = 0.125
        elif intensity > 0.25 and intensity < 0.50:
            intensity = 0.375

        elif intensity > 0.50 and intensity <0.75:
            intensity = 0.625

        elif intensity > 0.75 and intensity <1:
            intensity = 0.875


    b *= intensity
    g *= intensity
    r *= intensity

    if intensity > 0:
        return r, g, b
    else:
        return 0, 0, 0


def static(render, **kwargs):
    u, v, w = kwargs['barycentric']
    ta, tb, tc = kwargs['texCoords']
    na, nb, nc = kwargs['normals']

    b = random.random()
    g = random.random()
    r = random.random()

    if render:
        tx = ta.x * u + tb.x * v + tc.x * w
        ty = ta.y * u + tb.y * v + tc.y * w
        texColor = render.activeT.getColor(tx, ty)
        b *= texColor[0] / 255
        g *= texColor[1] / 255
        r *= texColor[2] / 255

    nx = na[0] * u + nb[0] * v + nc[0] * w
    ny = na[1] * u + nb[1] * v + nc[1] * w
    nz = na[2] * u + nb[2] * v + nc[2] * w

    normal = V3(nx, ny, nz)

    intensity = dot(normal, render.light)

    b *= intensity
    g *= intensity
    r *= intensity

    if intensity > 0:
        return r, g, b
    else:
        return 0,0,0

def rainbow(render, **kwargs):
    u, v, w = kwargs['barycentric']
    na, nb, nc = kwargs['normals']

    b = 255
    g = 255
    r = 255
    limit = 0

    nx = na[0] * u + nb[0] * v + nc[0] * w
    ny = na[1] * u + nb[1] * v + nc[1] * w
    nz = na[2] * u + nb[2] * v + nc[2] * w

    normal = V3(nx, ny, nz)

    intensity = dot(normal, render.light)

    if nz > limit+0*0.048 and nz < limit+1*0.048 or nz > limit+7*0.048 and nz < limit+8*0.048 or nz > limit+14*0.048 and nz < limit+15*0.048:
        b = 140
        r = 120
        g = 40
    elif nz > limit+1*0.048 and nz < limit+2*0.048 or nz > limit+8*0.048 and nz < limit+9*0.048 or nz > limit+15*0.048 and nz < limit+16*0.048:
        b = 255
        r = 0
        g = 0
    elif nz > limit+2*0.048 and nz < limit+3*0.048 or nz > limit+9*0.048 and nz < limit+10*0.048 or nz > limit+16*0.048 and nz < limit+17*0.048:
        b = 246
        r = 0
        g = 176
    elif nz > limit+3*0.048 and nz < limit+4*0.048 or nz > limit+10*0.048 and nz < limit+11*0.048 or nz > limit+17*0.048 and nz < limit+18*0.048:
        b = 0
        r = 0
        g = 255
    elif nz > limit+4*0.048 and nz < limit+5*0.048 or nz > limit+11*0.048 and nz < limit+12*0.048 or nz > limit+18*0.048 and nz < limit+19*0.048:
        b = 0
        r = 255
        g = 255
    elif nz > limit+5*0.048 and nz < limit+6*0.048 or nz > limit+12*0.048 and nz < limit+13*0.048 or nz > limit+19*0.048 and nz < limit+20*0.048:
        b = 0
        r = 255
        g = 127
    elif nz > limit+6*0.048 and nz < limit+7*0.048 or nz > limit+13*0.048 and nz < limit+14*0.048 or nz > limit+20*0.048 and nz < limit+21*0.048:
        b = 0
        r = 255
        g = 0

    b *= intensity / 255
    r *= intensity / 255
    g *= intensity / 255

    if intensity > 0:
        return r, g, b
    else:
        return 0,0,0

def twoface(render, **kwargs):
    u, v, w = kwargs['barycentric']
    ta, tb, tc = kwargs['texCoords']
    na, nb, nc = kwargs['normals']
    b, g, r = kwargs['color']

    b /= 255
    g /= 255
    r /= 255

    if render:
        tx = ta.x * u + tb.x * v + tc.x * w
        ty = ta.y * u + tb.y * v + tc.y * w
        texColor = render.activeT.getColor(tx, ty)
        b *= texColor[0] / 255
        g *= texColor[1] / 255
        r *= texColor[2] / 255

    nx = na[0] * u + nb[0] * v + nc[0] * w
    ny = na[1] * u + nb[1] * v + nc[1] * w
    nz = na[2] * u + nb[2] * v + nc[2] * w

    normal = V3(nx, ny, nz)
    intensity = dot(normal, render.light)

    if nx < 0:
        r = 1 - r
        b = 1 - b
        g = 1 - g

    b *= intensity
    g *= intensity
    r *= intensity

    if intensity > 0:
        return r, g, b
    else:
        return 0,0,0