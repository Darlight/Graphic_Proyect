"""
Universidad del Valle de Guatemala
Gráficas por computadora
Seccion 10
Lic. Dennis Aldana
Mario Perdomo
18029

lab4.py
Proposito: Un framebuffer simple para pintar un punto con modificaciones simples como:
- Cambiar de color de los puntos
- Crear un punto
- Modificaciones del tamaño de la venta principal
"""
from pathlib import Path
from tezt import Render
from obj import *
from shaders import *
import os

dir_path = os.path.dirname(os.path.realpath( __file__))
model_path = os.path.join(dir_path, r'Models\wario.obj')
texture_path = os.path.join(dir_path, r'Textures\background_mp9.bmp')
bitmap = Render()
bitmap.glCreateWindow(1400,800)
bitmap.light = V3(1,1,1)
print(bitmap.glInit())

texture = Texture(texture_path)
bitmap.framebuffer = texture.pixels
bitmap.textures = texture
bitmap.shaders = gourad
bitmap.lookAt(V3(1, 0, 50), V3(0, 0, 0), V3(0, 1, 0))
bitmap.glFinish('output.bmp')

#modelo 1
#wario
model_path = os.path.join(dir_path, r'Models\wario.obj')
texture_path = os.path.join(dir_path, r'Textures\wario_txt.bmp')
texture = Texture(texture_path)

bitmap.textures = texture
bitmap.shaders = shader_obj
bitmap.lookAt(V3(1, 0, 5), V3(0, 0, 0), V3(0, 1, 0))
bitmap.load(model_path,translate=(0.25, 0.4, 0.1), scale=(0.25, 0.25, 0.25))
bitmap.draw_arrays('TRIANGLES')
bitmap.glFinish('output.bmp')
"""
#modelo 2
#mario
model_path = os.path.join(dir_path, r'Models\Mario.obj')
texture_path = os.path.join(dir_path, r'Textures\mario_main.bmp')
texture = Texture(texture_path)

bitmap.textures = texture
bitmap.shaders = shader_obj
bitmap.lookAt(V3(1, 0, 5), V3(0, 0, 0), V3(0, 1, 0))
bitmap.load(model_path,translate=(450, 225, 50), scale=(110, 110, 75))
bitmap.draw_arrays('TRIANGLES')
bitmap.glFinish('output.bmp')

#modelo 3
#boo
model_path = os.path.join(dir_path, r'Models\Boo.obj')
texture_path = os.path.join(dir_path, r'Textures\boo1.bmp')
texture = Texture(texture_path)

bitmap.textures = texture
bitmap.shaders = shader_obj
bitmap.lookAt(V3(1, 0, 5), V3(0, 0, 0), V3(0, 1, 0))
bitmap.load(model_path,translate=(450, 225, 50), scale=(110, 110, 75))
bitmap.draw_arrays('TRIANGLES')
bitmap.glFinish('output.bmp')

#modelo 4
#beagle
model_path = os.path.join(dir_path, r'Models\beagle.obj')
texture_path = os.path.join(dir_path, r'Textures\beagle_txt.bmp')
texture = Texture(texture_path)

bitmap.textures = texture
bitmap.shaders = shader_obj
bitmap.lookAt(V3(1, 0, 5), V3(0, 0, 0), V3(0, 1, 0))
bitmap.load(model_path,translate=(450, 225, 50), scale=(110, 110, 75))
bitmap.draw_arrays('TRIANGLES')
bitmap.glFinish('output.bmp')

#modelo 5
#coinblock
model_path = os.path.join(dir_path, r'Models\coin_block.obj')
texture_path = os.path.join(dir_path, r'Textures\coin)block_texture.bmp')
texture = Texture(texture_path)

bitmap.textures = texture
bitmap.shaders = shader_obj
bitmap.lookAt(V3(1, 0, 5), V3(0, 0, 0), V3(0, 1, 0))
bitmap.load(model_path,translate=(450, 225, 50), scale=(110, 110, 75))
bitmap.draw_arrays('TRIANGLES')
bitmap.glFinish('output.bmp')
"""