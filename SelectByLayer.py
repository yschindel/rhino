import rhinoscriptsyntax as rs
import scriptcontext as sx

# get selected object
selection = rs.SelectedObjects()

print("Selected objects on layers:")
for i in selection:
    layer = rs.ObjectLayer(i)
    print(rs.LayerName(layer, False))
    rs.ObjectsByLayer(layer, True)
