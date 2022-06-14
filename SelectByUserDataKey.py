

def SelectUserDataKey():

    import rhinoscriptsyntax as rs
    
    selection = rs.SelectedObjects()
    rs.UnselectObjects(selection)
    keys_raw = []
        
    for obj in selection:
        skey = rs.GetUserText(obj)
        #print skey
        for k in skey:
            keys_raw.append(k)
     
    keys = list(set(keys_raw))

    key = rs.GetString("Type key to search for", keys[0], keys)
    
    rs.EnableRedraw(False)

    for obj in selection:
        obj_keys = rs.GetUserText(obj)
        if key in obj_keys:
            rs.SelectObject(obj)

    rs.EnableRedraw(True)
    
    
SelectUserDataKey()
