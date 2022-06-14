def _expl_blck_user_attr():
    import rhinoscriptsyntax as rs
    import time

    time_start = time.time()
    user_selection = rs.SelectedObjects()
    rs.UnselectObjects(user_selection)
    selection = []
    for obj in user_selection:
        if rs.ObjectType(obj) == 4096:
            selection.append(obj)
        else:
            print("selected object was not a block and was not considered")

    rs.EnableRedraw(False)

    attr_blocks = 0

    for obj in selection:
        skey = rs.GetUserText(obj)
        if skey:
            attr_blocks += 1
            attributes = {}
            for key in skey:
                attributes[key] = rs.GetUserText(obj, key)
            new_objs = rs.ExplodeBlockInstance(obj)
            for obj in new_objs:
                for key, value in attributes.items():
                    rs.SetUserText(obj, key, value)
        else:
            new_objs = rs.ExplodeBlockInstance(obj)

    rs.EnableRedraw(True)

    time_end = time.time()
    time_total = time_end - time_start
    print("{number} blocks exploded in {time} seconds, {amount} had attributes."\
            .format(number = len(selection), time = time_total, amount = attr_blocks))


_expl_blck_user_attr()
