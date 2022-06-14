import rhinoscriptsyntax as rs

PARENT_OBJ_ID = "parent_ID"

def ExtractSurface():
    """
    extracts a subsurface as a copy onto a mirror image layer structure.
    Joins all surfaces that have the same parent object
    """
    if rs.SelectedObjects():
        # check preselection for valid geometry
        is_subsurface = False
        rs.UnselectAllObjects()
    else:
        # when no valid geometry was found selection contains a subsurface
        is_subsurface = True

    obj_ref = rs.GetObject("Surface to extract", 8, is_subsurface, False, None, True)
    if not obj_ref: return

    # collect data about parent object
    parent_obj_id = obj_ref.Object().Id
    parent_obj_layer = rs.ObjectLayer(parent_obj_id)
    layer_color = rs.LayerColor(parent_obj_layer)
    
    # isolate top most parent layer from string to replace it
    parent_layer = parent_obj_layer.split("::")[0]
    new_layer = parent_obj_layer.replace(parent_layer, "NEW_MODEL")

    rs.AddLayer(new_layer)
    rs.LayerColor(new_layer, layer_color)

    surface_index = obj_ref.GeometryComponentIndex.Index

    if surface_index >= 0:
        srf = rs.ExtractSurface(parent_obj_id, surface_index, copy=True)
        if srf:
            rs.ObjectLayer(srf, layer=new_layer)
            rs.SetUserText(srf, PARENT_OBJ_ID, value=parent_obj_id)
            # get all objects on same layer
            layer_objs = rs.ObjectsByLayer(new_layer)
            match_ids = []
            for obj in layer_objs:
                # check if they have the same parent id for joining
                obj_id = rs.GetUserText(obj, PARENT_OBJ_ID)
                if obj_id == str(parent_obj_id):
                    match_ids.append(obj)
            if len(match_ids) > 1:
                # when other surfaces with same parent id where found then join
                joined_polysrf = rs.JoinSurfaces(match_ids, delete_input=True)
                rs.SetUserText(joined_polysrf, PARENT_OBJ_ID, parent_obj_id)
                rs.SelectObject(joined_polysrf)
                rs.ObjectLayer(joined_polysrf, layer=new_layer)
            else:
                rs.SelectObject(srf)


ExtractSurface()
