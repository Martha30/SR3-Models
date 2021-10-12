#Universidad del Valle de Guatemala
#Laurelinda Gómez 19501
#Ejercicio 1
#26/07/2021

import struct
from obj import Obj
from collections import namedtuple


V2 = namedtuple('Point2', ['x', 'y'])
def char(c):
    # 1 byte
    return struct.pack('=c', c.encode('ascii'))

def word(w):
    #2 bytes
    return struct.pack('=h', w)

def dword(d):
    # 4 bytes
    return struct.pack('=l', d)

# Guarda color
def color(r, g, b):
    # Acepta valores de 0 a 1
    return bytes([ int(b * 255), int(g* 255), int(r* 255)])

# Variables globales

BLACK = color(0,0,0)
WHITE = color(1,1,1)


class Renderer(object):
    #Constructor
    def __init__(self, width, height):
        # Renderer de color negro
        self.curr_color = WHITE
        self.clear_color = BLACK
        self.glCreateWindow(width, height)

    def glCreateWindow(self, width, height):
        self.width = width
        self.height = height
        self.glClear()
        self.glViewport(0,0, width, height)

    # Crea el viewport
    def glViewport(self, x, y, width, height):
        self.viewportX = int(x)
        self.viewportY = int(y)
        self.viewportWidth = int(width)
        self.viewportHeight = int(height)

    # color fondo
    def glClearColor(self, r, g, b):
        self.clear_color = color(r, g, b)

    def glClear(self):
        self.pixels = [[ self.clear_color for y in range(self.height)] for x in range(self.width)]

    def glViewportClear(self, color = None):
        for x in range(self.viewportX, self.viewportX + self.viewportWidth):
            for y in range(self.viewportY, self.viewportY + self.viewportHeight):
                self.glPoint(x,y, color)
    
    # Color 
    def glColor(self, r, g, b):
        self.curr_color = color(r,g,b)

    # Dibujar un punto
    def glPoint(self, x, y, color = None): 
        if x < self.viewportX or x >= self.viewportX + self.viewportWidth or y < self.viewportY or y >= self.viewportY + self.viewportHeight:
            return

        # enteros
        if (0 <= x < self.width) and (0 <= y < self.height):
            self.pixels[int(x)][int(y)] = color or self.curr_color

    
    def glPoint_NDC(self, x, y, color = None): 
        x = int( (x + 1) * (self.viewportWidth / 2) + self.viewportX )
        y = int( (y + 1) * (self.viewportHeight / 2) + self.viewportY)
        if x < self.viewportX or x >= self.viewportX + self.viewportWidth or y < self.viewportY or y >= self.viewportY + self.viewportHeight:
            return
        if (0 <= x < self.width) and (0 <= y < self.height):
            self.pixels[int(x)][int(y)] = color or self.curr_color

#Basado en lo que se realizó en clase
    def glLine(self, v0, v1, color = None):
        x0 = v0.x
        x1 = v1.x
        y0 = v0.y
        y1 = v1.y
        if x0 == x1 and y0 == y1:
            self.glPoint(x0,y1,color)
            return

        # Pendiente
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        steep = dy > dx 
        if steep:
            x0, y0 = y0, x0
            x1, y1 = y1, x1
        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)

        offset = 0
        limit = 0.5

        m = dy/dx
        y = y0
        
        for x in range(x0, x1 + 1):
            if steep:
                self.glPoint(y, x, color)
            else:
                self.glPoint(x, y, color)

            
            offset += m
            if offset >= limit:
                
                y += 1 if y0 < y1 else -1
                limit += 1

    #Se tomo de ejemplo lo realizado en clase
    def glLoadModel(self, filename, translate = V2(0.0,0.0), scale = V2(1.0,1.0)):
        
        model = Obj(filename)

        for face in model.faces:
            
            vertCount = len(face)

            for v in range(vertCount):
                
                index0 = face[v][0] - 1 
                index1 = face[(v + 1) % vertCount][0] - 1

                vert0 = model.vertices[index0]
                vert1 = model.vertices[index1]

                x0 = round(vert0[0] * scale.x + translate.x)
                y0 = round(vert0[1] * scale.y + translate.y)
                x1 = round(vert1[0] * scale.x + translate.x)
                y1 = round(vert1[1] * scale.y + translate.y)

                self.glLine(V2(x0,y0), V2(x1, y1))

    # Creación del Bitmap
    def glFinish(self, filename):
        # archivo BMP 
        with open(filename, "wb") as file:
            # Header
            file.write(bytes('B'.encode('ascii')))
            file.write(bytes('M'.encode('ascii')))
            # Por cada pixel se tienen 3 Bytes
            file.write(dword(14 + 40 + (self.width * self.height * 3)))
            file.write(dword(0))
            file.write(dword(14 + 40))

            # InfoHeader
            file.write(dword(40))
            file.write(dword(self.width))
            file.write(dword(self.height))
            file.write(word(1))
            file.write(word(24))
            file.write(dword(0))
            file.write(dword(self.width * self.height * 3))
            file.write(dword(0))
            file.write(dword(0))
            file.write(dword(0))
            file.write(dword(0))

            # Color Table
            for y in range(self.height):
                for x in range(self.width):
                    file.write(self.pixels[x][y])
                    