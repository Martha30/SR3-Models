from gl3 import Renderer, V2, color

#Main

# Dimensiones
width = 1500
height = 740

# Instancia del renderer
r = Renderer(width, height)

# Cargando el  modelo OBJ
r.glLoadModel('./models/camera.obj',V2(width/2, 300), V2(-70,50))

# Finish
r.glFinish("camera.bmp")
