import rhinoscriptsyntax as rs


class Element:

    world = [(0, 0, 0), (1, 0, 0), (0, 1, 0)]
    zDown = (0, 0, -1)
    hashGroups = set()
    instances = []
    
    def __init__(self, object=None):
        self.object = object
        self.local = [(0, 0, 0), (1, 0, 0), (0, 1, 0)]

    @staticmethod
    def makeBlock(object, blockName):
        if type(object) is not list:
            object = [object]
        rs.AddBlock(object, (0, 0, 0), name=blockName)

    def toBlock(self):
        if not self.hash:
            print('set hash!')
            return
        rs.DeleteObject(self.object)
        self.object = rs.InsertBlock(self.hash, (0, 0, 0))
        self.toLocal()

    def getFaces(self):
        if not self.object:
            print('set object!')
            return
        faces = rs.ExplodePolysurfaces(self.object)
        self.faces = faces
        
    def getPoints(self):
        if not self.faces:
            print('set faces!')
            return
        if not self.basePt:
            print('set base!')
            return
        self.points = []
        for face in self.faces:
            pt = rs.EvaluateSurface(face, 0.5, 0.5)
            if pt == self.basePt:
                continue
            self.points.append(pt)

    def getBase(self, select=False):
        if not self.faces:
            print('set faces!')
            return
        self.maxArea = 0
        for face in self.faces:
            normal = rs.SurfaceNormal(face, (0.5, 0.5))
            if rs.VectorDotProduct(self.zDown, normal) >= 0:
                faceArea = rs.SurfaceArea(face)[0]
                if faceArea > self.maxArea:
                    self.downVec = normal
                    self.maxArea = faceArea
                    self.baseSrf = face
        self.basePt = rs.EvaluateSurface(self.baseSrf, 0.5, 0.5)
        x = rs.EvaluateSurface(self.baseSrf, 1, 0.5)
        y = rs.EvaluateSurface(self.baseSrf, 0.5, 1)
        self.local = [self.basePt, x, y]
        if select == True:
            rs.SelectObject(self.baseSrf)

    def getDistance(self):
        if not self.points:
            print('set points!')
            return
        self.distance = 0
        for point in self.points:
            self.distance += rs.Distance(self.basePt, point)

    def getVolume(self):
        self.volume = rs.SurfaceVolume(self.object)[0]

    def getHash(self):
        if not self.maxArea:
            print('set maxArea!')
            return
        if not self.distance:
            print('set distance!')
            return
        distance = str(round(self.distance, 0))
        # volume = str(round(self.volume, 3))
        area = str(round(self.maxArea, 3))
        self.hash = distance + '-' + area
        Element.hashGroups.add(self.hash)

    def toLocal(self):
        rs.OrientObject(self.object, self.world, self.local)

    def toWorld(self):
        rs.OrientObject(self.object, self.local, self.world)
        pass

    def prepare(self):
        self.getFaces()
        self.getBase(select=False)
        self.getPoints()
        # self.getVolume()
        self.getDistance()
        self.getHash()

    def setObject(self, object):
        self.object = object

    def clean(self):
        rs.DeleteObjects(self.faces)


def run():
    selection = rs.SelectedObjects()
    rs.UnselectAllObjects()
    validTypes = [16, 1073741824]
    for object in selection:
        if rs.ObjectType(object) in validTypes:
            element = Element(object)
            element.prepare()
            Element.instances.append(element)

    print('prep success')
    # create block definitions for unique hashes
    for hash in Element.hashGroups:
        for element in Element.instances:
            if element.hash == hash:
                element.toWorld()
                Element.makeBlock(element.object, hash)
                break

    print('add block success')
    for element in Element.instances:
        element.toBlock()
        element.clean()


rs.EnableRedraw(False)
run()
rs.EnableRedraw(True)
