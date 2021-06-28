import numpy as np


# Makes a matrix representing the colored graph
def solver(n, r=None):
    m = np.zeros((n, n), dtype=int)
    if r:
        rm = np.random.randint(3, size=(n, n))
        print(rm)
        for i in range(1, n):
            for j in range(i):
                m[i, j] = rm[i, j]

    else:
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
    color_matrix = solver(n, r=True)
    # color_matrix = solver(n)
    print('solution matrix:')
    print(color_matrix)
    result = []

    for i in range(1, n):
        arcs = ''
        for j in range(i):
            arcs = arcs + str(color_matrix[i, j])
        result.append(arcs)

    mono_tris, tot_tris = counter(color_matrix)
    print('monochromatic triangles = ', mono_tris, ', total triangles = ', tot_tris)
    return result


res = main(7)
print('solution string: ', res)
