llst1 = [[1, 11, 5],
         [2, 6, 7],
         [3, 13, 9],
         [12, 7, 16],
         [14, 3, 25],
         [19, 18, 22],
         [23, 13, 29],
         [24, 4, 28],
         ]

llst = [[1, 11, 5],
        [2, 6, 7],
        [3, 13, 9],
        [12, 7, 16],
        [14, 3, 25],
        [19, 18, 22],
        [23, 13, 29],
        [24, 4, 28]]


def find(c):
    m = 100
    j = -1
    k = -1
    for i in range(len(llst)):
        if llst[i][0] < m and llst[i][0] > c:
            m = llst[i][0]
            j = i
            k = 0
        if llst[i][2] < m and llst[i][2] > c:
            m = llst[i][2]
            j = i
            k = 2
    if j != -1:
        return (j, k)
    return None


def fun(llst):
    ret = []
    c = (0, 0)
    d = find(llst[c[0]][c[1]])
    roof = None
    border = llst[0][2]
    while d:
        if llst[d[0]][d[1]] <= border:
            if c[1] == 0 and d[1] == 0:
                if roof:
                    if roof[1] < llst[c[0]][1]:
                        roof = llst[c[0]]
                        ret.append(llst[c[0]][0])
                        ret.append(llst[c[0]][1])
                else:
                    roof = llst[c[0]]
                    ret.append(llst[c[0]][0])
                    ret.append(llst[c[0]][1])
                border = max(border, llst[c[0]][2], llst[d[0]][2])
            elif c[1] == 2 and d[1] == 0:
                assert (roof)
                if roof[2] == llst[c[0]][2]:
                    roof = None
                if roof == None:
                    ret.append(llst[c[0]][2])
                    ret.append(0)
                border = max(border, llst[d[0]][2])
            elif c[1] == 0 and d[1] == 2:
                assert (roof)
                if roof[1] < llst[c[0]][1]:
                    roof = llst[c[0]]
                    ret.append(llst[c[0]][0])
                    ret.append(llst[c[0]][1])
                border = max(border, llst[c[0]][2])
            elif c[1] == 2 and d[1] == 2:
                assert (roof)
        else:
            ret.append(llst[c[0]][2])
            ret.append(0)
            border = llst[d[0]][2]
        c = d
        d = find(llst[c[0]][c[1]])
    return ret


for i in fun(llst):
    print i