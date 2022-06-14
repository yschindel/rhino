import rhinoscriptsyntax as rs
import scriptcontext as sx
import random

# get selected object
selection = rs.SelectedObjects()

x = rs.GetReal("Type maximum x scale")
y = rs.GetReal("Type maximum y scale")
z = rs.GetReal("Type maximum z scale")

for i in selection:
    point = rs.BlockInstanceInsertPoint(i)
    s_x = random.uniform(1, x)
    s_y = random.uniform(1, y)
    s_z = random.uniform(1, z)
    rs.ScaleObject(i, point, (s_x, s_y, s_z))
