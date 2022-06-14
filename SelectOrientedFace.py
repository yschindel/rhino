def _sel_orient_face():
    import rhinoscriptsyntax as rs
    
    """
    The VectorDotProduct of two parallel vectors is 1.
    The VectorDotProduct of two orthogonal vectors is 0.
    """
    
    user_selection = rs.SelectedObjects()
    rs.UnselectObjects(user_selection)
    selection = []
    for obj in user_selection:
        if rs.ObjectType(obj) == 8:
            selection.append(obj)
        else:
            print("selected object was not a surface and was not considered")
            
    vector_z = rs.CreateVector(0,0,1)
    user_input = rs.GetString("What do you want to select?", "Vertical", ["Vertical", "Horizontal"])
    
    rs.EnableRedraw(False)
    
    for srf in selection:
        srf_param = rs.SurfaceParameter(srf, (0.5, 0.5))
        srf_normal = rs.SurfaceNormal(srf, srf_param)
        vec_devitation = abs(rs.VectorDotProduct(vector_z, srf_normal))
        if user_input == "Vertical":
            if 0.5 > vec_devitation >= 0:
                rs.SelectObject(srf)
        elif user_input == "Horizontal":
            if 1 >= vec_devitation > 0.5:
                rs.SelectObject(srf)
    
    rs.EnableRedraw(True)
    
_sel_orient_face()