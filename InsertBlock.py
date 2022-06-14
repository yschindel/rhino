import rhinoscriptsyntax as rs
import scriptcontext as sx
import random

# get selected object
selection = rs.SelectedObjects()

blnames = rs.BlockNames()
names = rs.MultiListBox(blnames,"select block names","select block names")
amount = len(names)
print(amount)

for i in selection:
    angle = random.uniform(0, 359)
    if amount == 1:
        rs.InsertBlock(names[0], i, (1,1,1), angle, (0,0,1))
    elif amount >= 1:
        rs.InsertBlock(names[random.uniform(0, amount)], i, [1,1,1], angle, (0,0,1))
    else:
        pass
