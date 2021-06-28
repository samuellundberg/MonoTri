import numpy as np


# Makes a matrix represtenting the colored graph
def solver(n):
    m = np.zeros((n, n), dtype=int)
    m[1, 0] = 2
    return m


# counts the number of monochromatic triangles in the graph
def counter(m):
    n = len(m)
    count = 0
    tot = 0

    for a in range(n):
        for b in range(a+1, n):
            for c in range(b+1, n):
                tot += 1
                # print('looking at this triangle: ', a, b, c)
                if (m[b, a] == m[c, a]) and (m[b, a] == m[c, b]):
                    # print('adding onto current c. c = ', count)
                    count += 1

    return count, tot


def main(n):
    colorMatrix = solver(n)
    print('solution matrix:\n', colorMatrix)
    result = []

    for i in range(1, n):
        arcs = ''
        for j in range(i):
            arcs = arcs + str(colorMatrix[i, j])
        result.append(arcs)

    monoTris, totTris = counter(colorMatrix)
    print('monotris = ', monoTris, 'tottris = ', totTris)
    # print('est tris: ', ???)
    return result


res = main(7)
print('solution string: ', res)
