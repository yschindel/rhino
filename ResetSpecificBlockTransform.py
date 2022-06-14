import rhinoscriptsyntax as rs

selection = rs.GetObjects("Select block to query")

for obj in selection:
    if rs.IsBlockInstance(obj):
        arrMatrix = rs.BlockInstanceXform(obj)
        if arrMatrix is not None:
            inv_matrix = rs.XformInverse(arrMatrix)
            rs.TransformObject(obj, inv_matrix)
            new_matrix = arrMatrix
            new_matrix[0, 0] = round(arrMatrix[0, 0])
            new_matrix[0, 1] = round(arrMatrix[0, 1])
            new_matrix[0, 2] = 0
            new_matrix[1, 0] = round(arrMatrix[1, 0])
            new_matrix[1, 1] = round(arrMatrix[1, 1])
            new_matrix[1, 2] = 0
            new_matrix[2, 0] = 0
            new_matrix[2, 1] = 0
            new_matrix[2, 2] = round(arrMatrix[2, 2])
            rs.TransformObject(obj, new_matrix)
