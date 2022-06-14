import rhinoscriptsyntax as rs

class Extracted_Face:
    def __init__(self, origin_id, guid, z_coord, user_text):
        self.origin_id = origin_id
        self.guid = guid
        self.z_coord = z_coord
        self.user_text = user_text


def _user_object_selection(filter_dots = False):
    """
    asks user to select objects - takes selected objects - warns if nothing is selected
    """
    objs = rs.SelectedObjects()
    if not objs or len(objs)==0:
        objs = rs.GetObjects("Select Objects")

    if not objs or len(objs) == 0:
        rs.MessageBox("No objects selected.", 0, "Message")
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


def _extract_top_face():
    # classifies interior vs exterior elements
    import rhinoscriptsyntax as rs

    user_selection = _user_object_selection()

    rs.EnableRedraw(False)

    top_faces = []
    delete_objs = []
    for obj in user_selection:
        if rs.ObjectType(obj) in [16, 1073741824]:
            # get User text
            skey = rs.GetUserText(obj)
            if skey:
                attributes = {}
                for key in skey:
                    attributes[key] = rs.GetUserText(obj, key)
            # get geometry
            top_face_candidate = []
            expl_srfs = rs.ExplodePolysurfaces(obj)
            for srf in expl_srfs:
                delete_objs.append(srf)
                mid_point_list = rs.SurfaceAreaCentroid(srf)
                mid_point_z = mid_point_list[0][2]
                if not top_face_candidate:
                    top_face_candidate = Extracted_Face(obj, srf, mid_point_z, attributes)
                if top_face_candidate:
                    if top_face_candidate.z_coord < mid_point_z:
                        top_face_candidate = Extracted_Face(obj, srf, mid_point_z, attributes)
                    else:
                        continue
            top_faces.append(top_face_candidate)

    new_faces = []
    for face in top_faces:
        new_face = rs.CopyObject(face.guid)
        new_attributes = face.user_text
        for key, value in new_attributes.items():
            rs.SetUserText(new_face, key, value)
        new_faces.append(new_face)

    rs.DeleteObjects(delete_objs)
    rs.EnableRedraw(True)
    rs.SelectObjects(new_faces)



_extract_top_face()
