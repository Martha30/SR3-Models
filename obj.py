class Obj(object):
    def __init__(self, filename):
        with open(filename) as f:
            self.lines = f.read().splitlines()
        
        self.vertices = []
        self.texcoords = []
        self.normals = []
        self.faces = []
        self.read()
          
    
    def read(self):
        for line in self.lines:
            if line: 
                prefix, value  = line.split(' ', 1)
                if prefix == 'v':
                    self.vertices.append(list(map(float, value.split(' '))))
                #Texture Coordinates
                elif prefix == 'vt': 
                    self.texcoords.append(list(map(float, value.split(' '))))
                #Normales
                elif prefix == 'vn': 
                    self.normals.append(list(map(float, value.split(' '))))
                elif prefix == 'f':
                    self.faces.append([list(map(int, face.split('/'))) for face in value.split(' ')])            
    

