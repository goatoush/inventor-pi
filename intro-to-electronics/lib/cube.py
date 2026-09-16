import math

class Point3D:
    def __init__(self, x = 0, y = 0, z = 0):
        self.x, self.y, self.z = x, y, z

    def rotateX(self, angle):
        """ Rotates this point around the X axis the given number of degrees. """
        rad = angle * math.pi / 180
        cosa = math.cos(rad)
        sina = math.sin(rad)
        y = self.y * cosa - self.z * sina
        z = self.y * sina + self.z * cosa
        return Point3D(self.x, y, z)

    def rotateY(self, angle):
        """ Rotates this point around the Y axis the given number of degrees. """
        rad = angle * math.pi / 180
        cosa = math.cos(rad)
        sina = math.sin(rad)
        z = self.z * cosa - self.x * sina
        x = self.z * sina + self.x * cosa
        return Point3D(x, self.y, z)

    def rotateZ(self, angle):
        """ Rotates this point around the Z axis the given number of degrees. """
        rad = angle * math.pi / 180
        cosa = math.cos(rad)
        sina = math.sin(rad)
        x = self.x * cosa - self.y * sina
        y = self.x * sina + self.y * cosa
        return Point3D(x, y, self.z)

    def project(self, win_width, win_height, fov, viewer_distance):
        """ Transforms this 3D point to 2D using a perspective projection. """
        factor = fov / (viewer_distance + self.z)
        x = self.x * factor + win_width / 2
        y = -self.y * factor + win_height / 2
        return Point3D(x, y, self.z)

class Cube:
    def __init__(self, scaleX=1, scaleY=1, scaleZ=1, width=128, height=64, fov=64, distance=4):
        self.vertices = [
            Point3D(-1 * scaleX, 1 * scaleY,-1 * scaleZ),
            Point3D( 1 * scaleX, 1 * scaleY,-1 * scaleZ),
            Point3D( 1 * scaleX,-1 * scaleY,-1 * scaleZ),
            Point3D(-1 * scaleX,-1 * scaleY,-1 * scaleZ),
            Point3D(-1 * scaleX, 1 * scaleY, 1 * scaleZ),
            Point3D( 1 * scaleX, 1 * scaleY, 1 * scaleZ),
            Point3D( 1 * scaleX,-1 * scaleY, 1 * scaleZ),
            Point3D(-1 * scaleX,-1 * scaleY, 1 * scaleZ)
        ]
        
        # Define the edges, the numbers are indices to the vertices above.
        self.edges  = [
            # Back
            (0, 1), (1, 2), (2, 3), (3, 0),
            # Front
            (5, 4), (4, 7), (7, 6), (6, 5),
            # Front-to-back
            (0, 4), (1, 5), (2, 6), (3, 7),
        ]
        # Dimensions
        self.projection = [width, height, fov, distance]

    def draw(self, display, angleX=0, angleY=0, angleZ=0, clear_display=True, show_display=True):
        t = []
        for v in self.vertices:
            # Rotate the point around X axis, then around Y axis, and finally around Z axis.
            r = v.rotateX(angleX).rotateY(angleY).rotateZ(angleZ)
            # Transform the point from 3D to 2D
            p = r.project(*self.projection)
            # Put the point in the list of transformed vertices.
            t.append(p)
            
        if clear_display:
            display.fill(0)
        for e in self.edges:
            display.line(int(t[e[0]].x), int(t[e[0]].y), int(t[e[1]].x), int(t[e[1]].y), 1)
        if show_display:
            display.show()
