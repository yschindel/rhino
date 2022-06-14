import rhinoscriptsyntax as rs
import scriptcontext as sx
import Rhino as r
import random

sx.doc = r.RhinoDoc.ActiveDoc

# get selected object
selection = rs.SelectedObjects()

value = rs.GetReal("Type percentage to keep")

num_of_items = len(selection)
print("Original count: " + str(num_of_items))

num_of_items_to_keep = int(num_of_items * (value / 100))
print("Reduced count: " + str(num_of_items_to_keep))
reduced_selection = random.sample(selection, num_of_items_to_keep)

rs.UnselectAllObjects()

rs.SelectObjects(reduced_selection)
