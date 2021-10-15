def cal_nx(dimension, a, b):

    if (a, b) == (0, 0) or (a, b) == (0, dimension - 1) or (a, b) == (dimension - 1, dimension - 1) or \
                                                                                           (a, b) == (dimension - 1, 0):
        return 3

    elif (a == 0) or a == (dimension-1) or b == 0 or b == (dimension-1):
        return 5

    else:
        return 8
