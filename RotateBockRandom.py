import rhinoscriptsyntax as rs
import scriptcontext as sx
import random

# get selected object
selection = rs.SelectedObjects()
amount = len(selection)

for i in selection:
    point = rs.BlockInstanceInsertPoint(i)
    #print(point)
    rs.RotateObject(i, point, random.uniform(0, 359))
