import rhinoscriptsyntax as rs

LOCATION = "Location"
INTERIOR = "Interior"
EXTERIOR = "Exterior"

def _user_object_selection(filter_dots = False):
    """
    asks user to select objects - takes selected objects - warns if nothing is selected
    """
    objs = rs.SelectedObjects()
    if not objs or len(objs)==0:
        objs = rs.GetObjects("Select Objects")

    if not objs or len(objs) == 0:
        rs.MessageBox("No objects selected.", 0, "HdM BIM LIGHT")
        return None

    rs.UnselectAllObjects()

    rel_objs = []
    if filter_dots == True:
        for obj in objs:
            if TEMP in rs.GetUserText(obj):
                continue
            else:
                rel_objs.append(obj)
    else:
        rel_objs = objs

    return rel_objs


def _assign_location():
    # classifies interior vs exterior elements
    import rhinoscriptsyntax as rs

    print("Selection 1: Objects to classify")
    user_selection_1 = _user_object_selection()

    print("Selection 2: Enclosing volume")
    user_selection_2 = _user_object_selection()
    if len(user_selection_2) > 1:
        print("More than one enclosing volume selected.")

    rs.EnableRedraw(False)

    selection_1 = []
    for obj in user_selection_1:
        if rs.ObjectType(obj) == 8:
            selection_1.append(obj)
        elif rs.ObjectType(obj) == 1073741824:
            expl_srfs = rs.ExplodePolysurfaces(obj)
            amount = len(expl_srfs)
            rs.DeleteObjects(expl_srfs)
            if amount <= 1:
                selection_1.append(obj)
            else:
                print("{id} was not a surface and was not considered".format(id = obj))
        else:
            print("{id} was not a surface and was not considered".format(id = obj))

    selection_2 = []
    for vol in user_selection_2:
        if (rs.ObjectType(vol) in [16, 1073741824]) and rs.IsPolysurfaceClosed(vol):
            selection_2.append(vol)
        else:
            print("Enclosing volume was not closed, calculation aborted.")
            return None
    encl_vol = selection_2[0]

    for srf in selection_1:
        mid_point_list = rs.SurfaceAreaCentroid(srf)
        mid_point = mid_point_list[0]
        if rs.IsPointInSurface(encl_vol, mid_point):
            rs.SetUserText(srf, LOCATION, INTERIOR)
        else:
            rs.SetUserText(srf, LOCATION, EXTERIOR)

    rs.EnableRedraw(True)

_assign_location()
