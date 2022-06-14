import rhinoscriptsyntax as rs

filename_base = "C:/temp/547_2105_CityGrid-Screenshot_"
n = 2
layer_colors = set()
layers_all = rs.LayerNames()
layers = []
for layer in layers_all:
    if len(layer.split('::')) > n+1:
        layers.append(layer)
        layer_colors.add(rs.LayerColor(layer))
   
rs.EnableRedraw(enable=False)
for layer in layers_all:
    rs.LayerVisible(layer, visible=True)
for color in layer_colors:
    output_name = str(color)
    layers_on = []
    layers_off = []
    for layer in layers:
        if rs.LayerColor(layer) == color:
            layers_on.append(layer)
        elif rs.LayerColor(layer) != color:
            if layer != 'Default':
                layers_off.append(layer)
            
    #print(layers_on)
    #print(layers_off)
    for layer in layers_on:
        rs.LayerVisible(layer, visible=True)
    for layer in layers_off:
        rs.LayerVisible(layer, visible=False)
    rs.Command('-_ViewCaptureToFile '+chr(34)+filename_base+output_name+'.jpg'+chr(34)+' _EnterEnd')
    
for layer in layers_all:
    rs.LayerVisible(layer, visible=True)
    
rs.EnableRedraw(enable=True)