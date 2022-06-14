import rhinoscriptsyntax as rs

"""
use forward slash for file paths -> '/'
"""

filename_base = "C:/temp/"

prefix = 'export_'

layers_all = rs.LayerNames()
named_views = rs.NamedViews()

export_views = []
for view in named_views:
    if view.startswith(prefix):
        export_views.append(view)
        
rs.EnableRedraw(enable=False)

for layer in layers_all:
    rs.LayerVisible(layer, visible=False)

for layer in layers_all:
    if layer.startswith(prefix):
        rs.LayerVisible(layer, visible=True)
        for view in export_views:
            output_name = str(layer).replace(prefix, '') + '_' + str(view).replace(prefix, '')
            rs.RestoreNamedView(view)
            rs.Command('-_ViewCaptureToFile '+chr(34)+filename_base+output_name+'.jpg'+chr(34)+' _EnterEnd')
        rs.LayerVisible(layer, visible=False)
    
rs.EnableRedraw(enable=True)