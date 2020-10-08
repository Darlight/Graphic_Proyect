"""
Universidad del Valle de Guatemala
Gráficas por computadora
Seccion 10
Lic. Dennis Aldana
Mario Perdomo
18029

tezt.py
Proposito: Un framebuffer simple para pintar un punto con modificaciones simples como:
- Cambiar de color de los puntos
- Crear un punto
- Modificaciones del tamaño de la venta principal
"""
#struc pack
# wikipedia bmp file format
import struct
from obj import Obj, Texture
from math_functions import *
import math 
import random #Solo para dar texturas random al planeta
#opcion = 0
def char(c):
    # un char que vale un caracter de tipo string
    return struct.pack('=c', c.encode('ascii'))

def word(c):
    #convierte el numero de posicion de pixel a 2 bytes
    return struct.pack('=h', c)

def dword(c):
    #4 bytes de la estructura de un framebuffer
    return struct.pack('=l', c)

def color(r, g, b):
    return bytes([b, g, r])

#Colores como constantes
GREEN = color(0, 255, 0)
RED = color(255, 0, 0)
BLUE = color(0, 0, 255)
BLACK = color(0, 0, 0)
WHITE = color(255, 255, 255) 

class Render(object):
    def __init__(self):
        #Tamanio del bitmap
        self.framebuffer = []
        self.color = WHITE
        self.bg_color = BLACK
        self.xPort = 0
        self.yPort = 0
        self.vertex_arrays = []
        self.light = V3(0,0,1)
        self.textures = None
        self.shaders = None
        self.glCreateWindow()
    
    #Basicamente __init__ ^ hace esta funcion, asi que cree esta funcion por estética
    def glInit(self):
        return "Bitmap creado... \n"

    def point(self, x, y):
        self.framebuffer[y][x] = self.color

    def glCreateWindow(self, width=800, height=600):
        self.windowWidth = width
        self.windowHeight = height
        self.glClear()
        self.glViewPort(self.xPort, self.yPort, width, height)

    def glViewPort(self, x, y, width, height):
        self.xPort = x
        self.yPort = y
        self.viewPortWidth = width
        self.viewPortHeight = height

    def glClear(self):
        self.framebuffer = [
            [self.bg_color for x in range(self.windowWidth)] for y in range(self.windowHeight)
        ]
        self.zbuffer = [
        [-float('inf') for x in range(self.windowWidth)]
        for y in range(self.windowHeight)
        ]



    def glClearColor(self, r=0, g=0, b=0):
        self.bg_color = color(r,g,b)

    def glVertex(self, x, y):
        #Formula sacada de:
        # https://www.khronos.org/registry/OpenGL-Refpages/gl4/html/glViewport.xhtml
        newX = round((x + 1)*(self.viewPortWidth/2) + self.xPort)
        newY = round((y + 1)*(self.viewPortHeight/2) + self.yPort)
        #funcion point para optimar
        self.point(newX,newY)

    def glColor(self, r=0, g=0, b=0):
        #self.framebuffer[self.yPort][self.xPort] = color(r,g,b)
        #Cambiar los valores de 0-255 a 0-1
        self.color = color(r,g,b)

    def glLine(self, placement, ycardinal = False):
        #variables condicionales y misma formula del vertex
        position = ((placement + 1) * (self.viewPortHeight/2) + self.yPort) if ycardinal else ((placement+1) * (self.viewPortWidth/2) + self.xPort)
        return round(position)

    
    def Line(self,x1,y1,x2,y2):
        #Da error con multiples puntos y salen del index si los metemeos a glLine
       # x1 = self.glLine(x1)
       # x2 = self.glLine(x2)
       # y1 = self.glLine(y1,True)
       # y2 = self.glLine(y2,True)
    
        #El steep es la direccion de la recta
        steep = abs(y2 - y1) > abs(x2 - x1)

        if steep:
            x1, y1 = y1, x1
            x2, y2 = y2, x2

        if x1 > x2:
            x1, x2 = x2, x1
            y1, y2 = y2, y1

        dy = abs(y2 - y1)
        dx = abs(x2 - x1)
        #Es una resta con el punto original para determinar su coordenada
        offset = 0
        #El limite de la pendiente
        threshold = dx

        y = y1
        for x in range(x1, x2 + 1):
            if steep:
                self.point(y, x)
            else:
                self.point(x, y)
            
            offset += dy*2

            if offset >= threshold:
                y += 1 if y1 < y2 else -1
                threshold += dx*2
                
    
    def drawPolygon(self, points):
        iterations = len(points)
        for i in range(iterations):
            v0 = points[i]
            v1 = points[(i+1)%iterations]
            self.Line(v0[0], v0[1], v1[0], v1[1]) 

    def inundation_left(self, x, y, color1, color2):
        current_color = self.framebuffer[y][x]
        if (current_color != color1 and current_color != color2):
            self.point(x,y)
            #self.inundation(x+1,y,color1,color2)
            self.inundation_left(x,y+1,color1,color2)
            self.inundation_left(x-1,y,color1,color2)
            self.inundation_left(x,y-1,color1,color2)
    
    def inundation_right(self, x, y, color1, color2):
        current_color = self.framebuffer[y][x]
        if (current_color != color1 and current_color != color2):
            self.point(x,y)
            self.inundation_right(x+1,y,color1,color2)
            self.inundation_right(x,y+1,color1,color2)
            #self.inundation(x-1,y,color1,color2)
            self.inundation_right(x,y-1,color1,color2)

    def triangle(self):
        A = next(self.vertex_arrays)
        B = next(self.vertex_arrays)
        C = next(self.vertex_arrays)

        if self.textures:
            tA = next(self.vertex_arrays)
            tB = next(self.vertex_arrays)
            tC = next(self.vertex_arrays)

            nA = next(self.vertex_arrays)
            nB = next(self.vertex_arrays)
            nC = next(self.vertex_arrays)

        xmin, xmax, ymin, ymax = bbox(A, B, C)
        normal = norm(cross(sub(B, A), sub(C, A)))
        intensity = dot(normal, self.light)

        if intensity < 0:
            return
            
        for x in range(round(xmin), round(xmax) + 1):
            for y in range(round(ymin), round(ymax) + 1):
                
                w, v, u = barycentric(A, B, C, V2(x, y))
                if w < 0 or v < 0 or u < 0: 
                    continue
                if self.textures:
                    tx = tA.x * w + tB.x * u + tC.x * v
                    ty = tA.y * w + tB.y * u + tC.y * v

                    self.current_color = self.shaders(
                        self,
                        triangle=(A, B, C),
                        bar=(w, v, u),
                        texture_coords=(tx, ty),
                        varying_normals=(nA, nB, nC)
                    )
                else:
                    self.current_color = color(round(255 * intensity),0,0)
                    
                z = A.z * w + B.z * u + C.z * v
                if x < 0 or y < 0:
                    continue

                if x < len(self.zbuffer) and y < len(self.zbuffer[x]) and z > self.zbuffer[y][x]:
                    self.point(x, y)
                    self.zbuffer[y][x] = z

    def transform(self,vertex):
        augmented_vertex = [
        [vertex.x],
        [vertex.y],
        [vertex.z],
        [1]
        ]
        #matrix calculada al ser multiplicada, siendo las trasalaciones
        tranformed_vertex = MultMatriz(self.Viewport, self.Projection) 
        tranformed_vertex = MultMatriz(tranformed_vertex, self.View) 
        tranformed_vertex = MultMatriz(tranformed_vertex, self.Model) 
        tranformed_vertex = MultMatriz(tranformed_vertex, augmented_vertex)

        #simulador de un vector de 3
        tranformed_vertex = [
        (tranformed_vertex[0][0]),
        (tranformed_vertex[1][0]),
        (tranformed_vertex[2][0])
        ]
        return V3(*tranformed_vertex)
    #Las paramaetricas de la mayoria de los vectores son V3, ya no listas
    def load(self, filename, translate=(0,0,0), scale=(1,1,1), rotate=(0,0,0)):
        self.loadModelMatrices(translate, scale, rotate)
        model = Obj(filename)
        vertex_bufferObjects = []
        #light = V3(0,0,1)
        #normal = V3(0,0,0)
        #self.shape = shape
        for face in model.faces:
            vcount = len(face)
            if vcount == 3:
                for facepart in face:
                    vertex = self.transform(V3(*model.vertices[facepart[0]-1]))
                    vertex_bufferObjects.append(vertex)

                if self.textures:
                    for facepart in face:
                        tvertex = V2(*model.textcoords[facepart[1]-1])
                        vertex_bufferObjects.append(tvertex)

                    for facepart in face:
                        nvertex = V3(*model.normals[facepart[2]-1])
                        vertex_bufferObjects.append(nvertex)

                #normal = cross(sub(b, a), sub(c, a))
                #intensity = dot(norm(normal), norm(light))
                #grey = round(255 * intensity)
                #if grey < 0:
                 #   continue

                #intensity_color = color(grey, grey, grey)
                
            elif vcount == 4:
                #se divide el cuadrado en 2
                #primer triangulo
                for faceindex in [0,1,2]:
                    facepart = face[faceindex]
                    vertex = self.transform(V3(*model.vertices[facepart[0]-1]))
                    vertex_bufferObjects.append(vertex)
                try:
                    if self.textures:
                        for faceindex in range(0,3):
                            facepart = face[faceindex]
                            tvertex = V2(*model.textcoords[facepart[1]-1])
                            vertex_bufferObjects.append(tvertex)

                        for faceindex in range(0,3):
                            facepart = face[faceindex]
                            nvertex = V3(*model.normals[facepart[2]-1])
                            vertex_bufferObjects.append(nvertex)

                    #segundo triangulo que forma el cuadrado
                    for faceindex in [3,0,2]:
                        facepart = face[faceindex]
                        vertex = self.transform(V3(*model.vertices[facepart[0]-1]))
                        vertex_bufferObjects.append(vertex)

                    if self.textures:
                        for faceindex in [3,0,2]:
                            facepart = face[faceindex]
                            tvertex = V2(*model.textcoords[facepart[1]-1])
                            vertex_bufferObjects.append(tvertex)

                        for faceindex in [3,0,2]:
                            facepart = face[faceindex]
                            nvertex = V3(*model.normals[facepart[2]-1])
                            vertex_bufferObjects.append(nvertex)
                except:
                    pass  
        self.vertex_arrays = iter(vertex_bufferObjects)

    def loadModelMatrices(self, translate = (0,0,0), scale = (1,1,1), rotate = (0,0,0)):
        translate = V3(*translate)
        scale = V3(*scale)
        rotate = V3(*rotate)

        translation_matrix = [
        [1, 0, 0, translate.x],
        [0, 1, 0, translate.y],
        [0, 0, 1, translate.z],
        [0, 0, 0, 1],
        ]


        a = rotate.x
        rotation_matrix_x = [
        [1, 0, 0, 0],
        [0, math.cos(a), -math.sin(a), 0],
        [0, math.sin(a),  math.cos(a), 0],
        [0, 0, 0, 1]
        ]

        a = rotate.y
        rotation_matrix_y = [
        [math.cos(a), 0,  math.sin(a), 0],
        [     0, 1,       0, 0],
        [-math.sin(a), 0,  math.cos(a), 0],
        [     0, 0,       0, 1]
        ]

        a = rotate.z
        rotation_matrix_z = [
        [math.cos(a), -math.sin(a), 0, 0],
        [math.sin(a),  math.cos(a), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
        ]

        rotation_matrix = MultMatriz(rotation_matrix_x, rotation_matrix_y)
        rotation_matrix = MultMatriz(rotation_matrix, rotation_matrix_z)

        scale_matrix = [
        [scale.x, 0, 0, 0],
        [0, scale.y, 0, 0],
        [0, 0, scale.z, 0],
        [0, 0, 0, 1],
        ]

        MultMatrizodelo = MultMatriz(translation_matrix, rotation_matrix) 
        self.Model = MultMatriz(MultMatrizodelo, scale_matrix)

    def loadViewMatrix(self, x, y, z, center):
        M = [
        [x.x, x.y, x.z,  0],
        [y.x, y.y, y.z, 0],
        [z.x, z.y, z.z, 0],
        [0,     0,   0, 1]
        ]

        O = [
        [1, 0, 0, -center.x],
        [0, 1, 0, -center.y],
        [0, 0, 1, -center.z],
        [0, 0, 0, 1]
        ]

        self.View = MultMatriz(M, O)

    def loadProjectionMatrix(self, coeff):
        self.Projection =  [
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, coeff, 1]
        ]

    def loadViewportMatrix(self, x = 0, y = 0):
        self.Viewport =  [
        [self.windowWidth/2, 0, 0, x + self.windowWidth/2],
        [0, self.windowHeight/2, 0, y + self.windowHeight/2],
        [0, 0, 128, 128],
        [0, 0, 0, 1]
        ]

    def lookAt(self, eye, center, up):
        z = norm(sub(eye, center))
        x = norm(cross(up, z))
        y = norm(cross(z, x))
        self.loadViewMatrix(x, y, z, center)
        self.loadProjectionMatrix(-1 / length(sub(eye, center)))
        self.loadViewportMatrix()

    def draw_arrays(self, polygon):
        if polygon == 'TRIANGLES':
            try:
                while True:
                    self.triangle()
            except StopIteration:
                print('Modelo ya hecho.')
    

    def glFinish(self, filename):
        f = open(filename, 'bw')
        # file header
        f.write(char('B'))
        f.write(char('M'))

        f.write(dword(14 + 40 + self.windowWidth * self.windowHeight * 3))

        f.write(dword(0))

        f.write(dword(14 + 40))

        # image header 
        f.write(dword(40))
        f.write(dword(self.windowWidth))
        f.write(dword(self.windowHeight))
        f.write(word(1))
        f.write(word(24))
        f.write(dword(0))
        f.write(dword(self.windowWidth * self.windowHeight * 3))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))

        # pixel data
        
        #ESTA COSA ERA MI ERROR, HABIA COLOCADO MAL LAS COORDENADAS 
        for x in range(self.windowHeight):
            for y in range(self.windowWidth):
                f.write(self.framebuffer[x][y])
        f.close()
"""
    def inundation(self, x, y, color1, color2):
        current_color = self.framebuffer[y][x]
        if (current_color != color1 and current_color != color2):
            self.point(x,y)
            #self.inundation(x+1,y,color1,color2)
            self.inundation(x,y+1,color1,color2)
            self.inundation(x-1,y,color1,color2)
            self.inundation(x,y-1,color1,color2)
"""


"""
    def Line(self,x0,y0,x1,y1):
        #self.x0 = x0
        #self.x1 = x1
        #self.y0 = y0
        #self.y1 = y1
        #dy = abs(y1 - y0)
        #dx = abs(x1 - x0)
        #dy > dx
        
        steep = abs(y1 - y0) > abs(x1 - x0)
        if steep:
            x0, y0 = y0, x0
            x1, y1 = y1, x1
        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0
        
        dy = abs(y1 - y0)
        dx = abs(x1 - x0)
        
        offset  = 0
        
        threshold = dx 
       
        y = y0
        # y = y1 - m * (x1 - x)
        for x in range(x0, x1):

            #self.point(self.y,self.x)
            
            if steep:
                 #render.point(round(x), round(y))
                self.point(y, x)

            else:
                #render.point(x), round(y))
                self.point(x,y)
                
            offset += dy * 2
            if offset >= threshold:
                y += 1 if y0 < y1 else -1
                threshold += dx * 2
"""