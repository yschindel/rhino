import rhinoscriptsyntax as rs
import scriptcontext as sx
import Rhino as r

sx.doc = r.RhinoDoc.ActiveDoc

# get selected object
selection = rs.SelectedObjects()

for sel in selection:
    # get block name
    name = rs.BlockInstanceName(sel)
    # get all blockinstances with the same name
    blockInstances = rs.BlockInstances(name)
    rs.SelectObjects(blockInstances)
