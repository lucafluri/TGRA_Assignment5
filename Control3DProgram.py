
from OpenGL.GL import *
from OpenGL.GLU import *
from math import *

import pygame
from pygame.locals import *

import sys
import time

from Shaders import *
from Matrices import *

import obj_3D_loading

class GraphicsProgram3D:

    def __init__(self):

        pygame.init() 
        pygame.display.set_caption('TGRA Assignment 5 -- Luca Fluri')

        pygame.display.set_mode((800,600), pygame.OPENGL|pygame.DOUBLEBUF)

        self.shader = Shader3D()  
        self.shader.use()


        self.model_matrix = ModelMatrix()

        self.view_matrix = ViewMatrix()

        self.view_matrix.look(Point(1, 0, 4), Point(10, 0, 4), Vector(0, 0, 1))

        self.shader.set_view_matrix(self.view_matrix.get_matrix())

        self.projection_matrix = ProjectionMatrix()
        self.fov = 90
        # self.projection_matrix.set_orthographic(-2, 2, -2, 2, 0.5, 10)
        self.projection_matrix.set_perspective(120, 800/600, 0.001, 10 )
        self.shader.set_projection_matrix(self.projection_matrix.get_matrix())

        # Turn left
        # self.view_matrix.yaw(90)


        self.cube = Cube()

        self.sphere = OptimizedSphere(24, 48)

        self.obj_model = obj_3D_loading.load_obj_file(sys.path[0] + "/models", "smooth_sphere.obj")

        self.clock = pygame.time.Clock()
        self.clock.tick()

        self.angle = 0


        self.texture_id01 = self.load_texture("/textures/tex01.png")
        self.texture_id02 = self.load_texture("/textures/tex02.jpg")
        self.texture_id03 = self.load_texture("/textures/wall.jpg")
        self.texture_id04 = self.load_texture("/textures/mars.jpg")

        self.fr_ticker = 0
        self.fr_sum = 0

        self.startTime = time.time()

    def load_texture(self, path_string):
        # Loading and Binding Texture
        surface = pygame.image.load(sys.path[0] + path_string)
        tex_string = pygame.image.tostring(surface, "RGBA", 1)
        width = surface.get_width()
        height = surface.get_height()
        tex_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, tex_id)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, tex_string)
        return tex_id

    def lerp(self, a, b, t):
        return a.__mul__(1-t) + b.__mul__(t)

    def getCurrentTime(self):
        # Calc current Program time
        return time.time() - self.startTime
    
    def getT(self, startT, endT):
        # Calc current Program time
        current = self.getCurrentTime()
        if current < startT:
            return 0
        elif current > endT:
            return 1
        else:
            return (current - startT) / (endT - startT)

  
    # Recursive Bezier Function
    # takes an array of vectors 
    def bezier(self, vectors, t):
        vectors_new = []
        if(len(vectors) > 2):
            for i in range(len(vectors) - 1):
                vectors_new.append(self.lerp(vectors[i], vectors[i + 1], t))
            return self.bezier(vectors_new, t)
        else:
            return self.lerp(vectors[0], vectors[1], t)
        
    def bezierSpline(self, vectors, t):
        # Build Segments
        # Add first 4 points
        arrays = [vectors[:4]]
        vectors = vectors[4:]

        # Add subsequent 2 points
        for _ in range((int) (len(vectors) / 2)):
            arrays.append(vectors[:2])
            vectors = vectors[2:]
        arrays.append(vectors)


        for i in range(len(arrays)):
            if i == 0:
                continue
            if(len(arrays[i]) == 0):
                continue
            arrays[i].insert(0, arrays[i-1][3])
            arrays[i].insert(1, arrays[i][0] + (arrays[i-1][3] - arrays[i-1][2]))

        # Flatten List
        flat = []
        for arr in arrays:
            flat += arr

        return self.bezier(flat, t)


    





    def update(self):
        delta_time = self.clock.tick() / 1000.0
        self.fr_sum += delta_time
        self.fr_ticker += 1
        if self.fr_sum > 1.0:
            # print(self.fr_ticker / self.fr_sum)
            self.fr_sum = 0
            self.fr_ticker = 0
        print(self.getCurrentTime())


        self.angle += (pi * delta_time) * 180.0/pi
        # if self.angle > 180:
        #     self.angle -= 180

    

    def display(self):
        t = self.getCurrentTime()


        glEnable(GL_DEPTH_TEST)  ### --- NEED THIS FOR NORMAL 3D BUT MANY EFFECTS BETTER WITH glDisable(GL_DEPTH_TEST) ... try it! --- ###


        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)  ### --- YOU CAN ALSO CLEAR ONLY THE COLOR OR ONLY THE DEPTH --- ###

        glViewport(0, 0, 800, 600)

        self.projection_matrix.set_perspective(self.fov, 800/600, 0.001, 50 )

        self.shader.set_projection_matrix(self.projection_matrix.get_matrix())
        self.shader.set_view_matrix(self.view_matrix.get_matrix())
        self.shader.set_eye_position(self.view_matrix.eye)


        # Textures
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.texture_id01)
        glActiveTexture(GL_TEXTURE1)
        glBindTexture(GL_TEXTURE_2D, self.texture_id02)
        glActiveTexture(GL_TEXTURE2)
        glBindTexture(GL_TEXTURE_2D, self.texture_id03)
        glActiveTexture(GL_TEXTURE3)
        glBindTexture(GL_TEXTURE_2D, self.texture_id04)

        # Move Camera to end of wall
        bezCamera1 = self.bezierSpline([Vector(-1, -1, 0), Vector(5,-2, 0), Vector(10, -5, 2), Vector(15, -3, 0), Vector(17, -1, 0), Vector(20, 8, 5)], self.getT(0, 15))
        self.view_matrix.eye = Point(bezCamera1.x, bezCamera1.y, bezCamera1.z)

        lerpYaw1 = self.lerp(Vector(20, 0, 0), Vector(0, 0, 0), self.getT(1, 6))
        self.view_matrix.look(self.view_matrix.eye, lerpYaw1, Vector(0, 0, 1))
        
        # Camera Cut
        if(t > 15):
            bezCamera2 = self.bezierSpline([Vector(3, 5, 5), Vector(3, -4, 3)], self.getT(15, 25))
            self.view_matrix.eye = Point(bezCamera2.x, bezCamera2.y, bezCamera2.z)
            self.view_matrix.look(self.view_matrix.eye, Vector(8, 0, 5), Vector(0, 0, 1))
            
        if(t>25):
            lerp01 = self.lerp(0.0, 1.0, self.getT(25, 30))
            lerp10 = self.lerp(1.0, 0.0, self.getT(25, 30))
            self.view_matrix.look(self.view_matrix.eye, Vector(8, 0, 5), Vector(0, lerp01, lerp10))
        if(t>30):
            lerp01 = self.lerp(0.0, 1.0, self.getT(30, 35))
            lerp10 = self.lerp(1.0, 0.0, self.getT(30, 35))
            self.view_matrix.look(self.view_matrix.eye, Vector(8, 0, 5), Vector(0, lerp10, lerp01))
        

        #LIGHTS
        self.shader.set_global_ambient(Color(0.01, 0.01, 0.01))
    
        self.shader.set_light1_position(self.view_matrix.eye, 1.0)
        # self.shader.set_light1_position(Point(0.0, 0.0, 50.0), 0.0)
        self.shader.set_light1_diffuse(Color(0.5, 0.5, 0.5))
        self.shader.set_light1_specular(Color(0.25, 0.25, 0.25))
        self.shader.set_light1_ambient(Color(0.15, 0.15, 0.15))

        self.shader.set_light2_position(Point(self.lerp(0.01, 5.0, self.getT(20, 25)), 0, 1), 0.0)
        color2 = Color(self.lerp(0.1, 0.5, self.getT(20, 25)), 0.025, 0.02)
        self.shader.set_light2_diffuse(color2)
        self.shader.set_light2_specular(color2*0.5)
        self.shader.set_light2_ambient(color2*0.25)

        if(t>15):
            bezLight3 = self.bezierSpline([Vector(0, 0, 1), Vector(10, 0, 10), Vector(0, 10, 10), Vector(-10, 0, 10), Vector(0, -10, -10), Vector(10, 0, -10)], self.getT(15, 25))
            self.shader.set_light3_position(bezLight3, 0.0)
            # self.shader.set_light3_position(Point(0.0, 0.0, 50.0))
            color3 = Color(0.05, 0.4, 0.05)
            self.shader.set_light3_diffuse(color3*1.2)
            self.shader.set_light3_specular(color3*0.5)
            self.shader.set_light3_ambient(color3*0.25)

            bezLight4 = self.bezierSpline([Vector(10, 0, -10), Vector(0, -10, -10), Vector(-10, 0, 10), Vector(0, 10, 10), Vector(10, 0, 10), Vector(0, 0, 1)], self.getT(15, 25))
            self.shader.set_light4_position(bezLight4, 0.0)
            # self.shader.set_light4_position(Point(0.0, 0.0, 50.0))
            color4 = Color(0.05, 0.05, 0.4)
            self.shader.set_light4_diffuse(color4*1.2)
            self.shader.set_light4_specular(color4*0.5)
            self.shader.set_light4_ambient(color4*0.25)
        



        self.shader.set_material_specular(Color(1.0, 1.0, 1.0))
        self.shader.set_material_shininess(5.0)


        self.model_matrix.load_identity()

        self.shader.set_material_diffuse(Color(1.0, 1.0, 0.0))

        self.cube.set_vertices(self.shader)
        # self.sphere.set_vertices(self.shader)


        
        # Mid Wall
        self.shader.set_specular_tex(2)
        self.shader.set_diffuse_tex(2)
        self.shader.set_material_diffuse(Color(0.25, 0.25, 0.25))
        self.shader.set_material_specular(Color(0.5, 0.5, 0.5))
        self.shader.set_material_shininess(0.25)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(10.0, 8.0 , 4.0)  
        self.model_matrix.add_scale(20, 1, 8)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.cube.draw(self.shader)
        self.model_matrix.pop_matrix()




        
        # 2 Cubes with textures
        self.shader.set_diffuse_tex(0)
        self.shader.set_specular_tex(1)        
        self.shader.set_material_diffuse(Color(1.0, 1.0, 1.0))
        self.shader.set_material_shininess(10)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(8.0, 0.0 , 3.0)  
        self.model_matrix.add_scale(1, 1, 1)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.cube.draw(self.shader)
        self.model_matrix.pop_matrix()

        self.shader.set_diffuse_tex(1) 
        self.shader.set_specular_tex(1) 
        self.shader.set_material_diffuse(Color(1.0, 1.0, 1.0))
        self.shader.set_material_shininess(10)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(8.0, 0.0 , 5.0)  
        self.model_matrix.add_scale(1, 1, 1)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.cube.draw(self.shader)
        self.model_matrix.pop_matrix()

        # MARS BALL
        bez = self.bezierSpline([Vector(1, 0, 0), Vector(3,0, 0), Vector(3, 0, 5), Vector(4, 3, 5), Vector(9, 0, 0), Vector(8, 0, 8), Vector(5, 0, 2), Vector(0, 0, -2), Vector(0, 0, -4), Vector(8, -3, 0), Vector(10, 0-3, 0)], self.getT(4, 15))

        self.shader.set_diffuse_tex(3)
        self.shader.set_specular_tex(3)
        self.shader.set_material_diffuse(Color(1.0, 1.0, 1.0))
        self.shader.set_material_shininess(10)

        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(bez.x, bez.y, bez.z)  
        self.model_matrix.add_scale(1, 1, 1)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.sphere.draw(self.shader)
        self.model_matrix.pop_matrix()


        # Rotating Ring at (7, -3, 0)
        for i in range(8):
            self.model_matrix.push_matrix()
            self.model_matrix.add_translation(0, -3, 0)
            self.model_matrix.add_rotation_x(self.angle * 0.74324 + i * 45)
            
            if(t>30):
                self.model_matrix.add_translation(8, self.lerp(4.0, 2.0, self.getT(30, 35)), 0)
            else:
                self.model_matrix.add_translation(8, self.lerp(2.0, 4.0, self.getT(20, 25)), 0)
            self.model_matrix.add_rotation_x(-self.angle * 0.74324 + i * 45)
            self.model_matrix.add_scale(1.0, 1.0, 1.0)
            self.shader.set_model_matrix(self.model_matrix.matrix)

            self.shader.set_material_diffuse(Color(1.0, 1.0, 1.0))
            self.obj_model.draw(self.shader)
            self.model_matrix.pop_matrix()


        pygame.display.flip()

        

    def program_loop(self):
        exiting = False
        while not exiting:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("Quitting!")
                    exiting = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == K_ESCAPE:
                        print("Escaping!")
                        exiting = True
                        
            
            self.update()
            self.display()

        #OUT OF GAME LOOP
        pygame.quit()

    def start(self):
        self.program_loop()

if __name__ == "__main__":
    GraphicsProgram3D().start()