import rhinoscriptsyntax as rs
n = 2
selection = rs.SelectedObjects()
obj = selection[0]
origin_layer = rs.ObjectLayer(obj)
or_split_name = origin_layer.split('::')
or_reduced_name = or_split_name[n:]
or_search_name = '::'.join(or_reduced_name)
origin_color = rs.LayerColor(origin_layer)
layers = rs.LayerNames()
for layer in layers:
    split_name = layer.split('::')
    reduced_name = split_name[n:]
    search_name = '::'.join(reduced_name)
    if search_name == or_search_name:
        rs.LayerColor(layer, origin_color)