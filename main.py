import numpy as np
import time


# Greedy graph coloring algorithm that for each arc sets the smallest color
# it can without making a monochromatic triangle. Naive apporach
# Does not work well.
def greedy(n):
    m = np.zeros((n, n), dtype=int)
    for i in range(1, n):
        m[i, 0] = i % 3
        for j in range(1, i):
            penalty = [0, 0, 0]
            for x in range(j):
                if m[i - 1, x] == m[i, x]:
                    penalty[m[i - 1, x]] += 1
            m[i, j] = penalty.index(min(penalty))
    return m


# Improvement on greedy. This one also strives for tri-collored graphs and evenly distributed arcs to each node
def greedy2(n):
    m = np.zeros((n, n), dtype=int)
    p1 = 100
    p2 = 1
    p3 = 1
    number_count = [0, 0, 0]
    for i in range(1, n):
        m[i, 0] = (i-1) % 3
        for j in range(1, i):
            # i punkten (i, j) tittar jag i {(i, x), (j, x)}, x in [0:j-1]
            # om ix == jx så får färgen p=5. i alla fall får färgen vi tittade på p = 1
            penalty = [0, 0, 0]
            for x in range(j):
                if m[i, x] == m[j, x]:
                    penalty[m[i, x]] += p1
                else:
                    penalty[m[i, x]] += p2
                    penalty[m[j, x]] += p2
            # vi ska också kolla på de andra färgerna i punkten j. de ser vi i (j, y), y in [0:j-1]
            # och även (z, j), z in [j + 1, i - 1]
            for y in range(i):
                if y < j:
                    penalty[m[j, y]] += p3      # 3
                if y > j:
                    penalty[m[y, j]] += p3

            # m[i, j] = penalty.index(min(penalty))

            small = min(penalty)
            p = False
            if penalty[0] == penalty[1] and penalty[0] == penalty[2]:
                temp = number_count.index(min(number_count))

            elif penalty[0] == small and penalty[1] == small:
                temp = 0
                if number_count[0] > number_count[1]:
                    temp = 1

            elif penalty[1] == small and penalty[2] == small:
                temp = 1
                if number_count[1] > number_count[2]:
                    temp = 2

            elif penalty[0] == small and penalty[2] == small:
                temp = 0
                if number_count[0] > number_count[2]:
                    temp = 2

            else:
                temp = penalty.index(small)
                p = False

            if p:
                print('pen: ', penalty, '\nsat: ', number_count, '\ntemp: ', temp, '\n')
            m[i, j] = temp
            number_count[temp] += 1

            if j == -3:
                print(penalty)

    return m


# Divides nodes into 5 groups. Arcs between nodes in the same group is colored 0
# Arcs between neighbouring groups are colored 1, and 2 if the groups are not neighbouring
# This gives the optimal solution for n >= 20
def penta(n):
    m = np.zeros((n, n), dtype=int)
    for i in range(1, n):
        for j in range(0, i):
            if i % 5 == j % 5:          # Same group, leave the color as 0
                continue
            elif abs(i % 5 - j % 5) == 1 or abs(i % 5 - j % 5) == 4:
                m[i, j] = 1
            elif abs(i % 5 - j % 5) == 2 or abs(i % 5 - j % 5) == 3:
                m[i, j] = 2
            else:
                print('you are bad at math')

    return m


# Creates a fully connected tri-colored graph no monochromatic triangles for all n < 17
# by dividing nodes into three groups with an internal rang. In n = 16 the node is place in the middle.
# see https://upload.wikimedia.org/wikipedia/commons/5/51/K_16_partitioned_into_three_Clebsch_graphs.svg
# if n > 16 it will keep stacking nodes in the middle and will get many mono tris for n >> 16
# However this gives the optimal solution for n <= 17
def perfect16(n):
    m = np.zeros((n, n), dtype=int)
    for i in range(15):
        if i == n:
            break
        for j in range(i):
            im3 = i % 3
            id3 = int(i / 3)
            jm3 = j % 3
            jd3 = int(j / 3)
            diff = id3 - jd3

            if im3 == jm3:
                if im3 == 1:
                    if diff == 1 or diff == 4:
                        m[i, j] = 0
                    else:
                        m[i, j] = 2

                if im3 == 0:
                    if diff == 1 or diff == 4:
                        m[i, j] = 1
                    else:
                        m[i, j] = 0

                if im3 == 2:
                    if diff == 1 or diff == 4:
                        m[i, j] = 2
                    else:
                        m[i, j] = 1

                continue

            if diff == 0:
                m[i, j] = (im3 + jm3 - 1) % 3
            elif diff == 1 or diff == 4:
                m[i, j] = (im3 + jm3) % 3
            elif diff == 2 or diff == 3:
                m[i, j] = (im3 + jm3 + 1) % 3

    for i in range(15, n):
        for j in range(i):
            if j % 3 == 0:
                m[i, j] = 2
            if j % 3 == 1:
                m[i, j] = 1
            if j % 3 == 2:
                m[i, j] = 0

    return m


# Makes a matrix representing the colored graph
# param n: int representing the size of the graph
# param a: algorithm used to collor graph. defaults to random
# complexity = n2
def solver(n, a=None):
    if a == 'greedy':
        # print('running greedy algorithm')
        m = greedy(n)
    elif a == 'greedy2':
        # print('running improved greedy algorithm')
        m = greedy2(n)
    elif a == 'penta':
        m = penta(n)
    elif a == 'perfect16':
        m = perfect16(n)
    else:
        print('running random solver')
        m = np.zeros((n, n), dtype=int)
        rm = np.random.randint(3, size=(n, n))
        for i in range(1, n):
            for j in range(i):
                m[i, j] = rm[i, j]

    return m


# counts the number of monochromatic triangles in the graph
# complexity = n3
def counter(m):
    n = len(m)
    count = 0
    coords = []
    for a in range(n):
        for b in range(a+1, n):
            for c in range(b+1, n):
                if (m[b, a] == m[c, a]) and (m[b, a] == m[c, b]):
                    count += 1
                    coords.append((a, b, c))

    # print(coords)
    return count


# Takes a list of strings and concatenates them to one string, each element separated by ', '
def to_string(list_of_strings):
    concat_string = ''
    for l in list_of_strings:
        concat_string += l + ', '
    return concat_string


# Stores a result file at path. First line is number of monotris. Second line is the result string of the colored graph.
# If there is already a file at path it will be overwritten.
# param path: string for where to store results. "results/X.txt" where X is the size of the Graph
# param result_string: string representing the graph coloring
# param mcts: int representing the number of monochromatic triangles in the colored graph
def my_write(path, result_string, mcts):
    content = str(mcts) + '\n' + to_string(result_string)
    file = open(path, "w")
    file.write(content)
    file.close()


# If the number of monotris is lower than the recorded number for the given size the
# result_string number of monotris is saved to file named 'size'.txt in the results folder
def store_results(size, result_string, monotris):
    path = "results/" + str(size) + ".txt"

    try:
        file = open(path, "r")
        content = file.readlines()
        file.close()

        if len(content) == 2:
            ref = int(content[0])
            if monotris < ref:
                print('found new best score of: ', monotris, ' for size: ', n)
                my_write(path, result_string, monotris)
            else:
                print('did not beat old solution of: ', ref, ' for size: ', n)
        else:
            print('Weird file at path: ', path)
    except IOError:
        print('did not find file at path: ', path, '. Creating a new one')
        my_write(path, result_string, monotris)


def main(n, algo):
    startsolve = time.time()
    color_matrix = solver(n, a=algo)
    # print('solution matrix:')
    # print(color_matrix)
    result = []
    solvetime = time.time()

    for i in range(1, n):
        arcs = ''
        for j in range(i):
            arcs = arcs + str(color_matrix[i, j])
        result.append(arcs)
    startcount = time.time()
    mono_tris = counter(color_matrix)
    counttime = time.time()
    # print('monochromatic triangles = ', mono_tris, ', total triangles = ', tot_tris)
    # print('time to solve = ', solvetime - startsolve, 'time to count = ', counttime - startcount)

    return result, mono_tris


start = time.time()
N = [17]
# N = [17, 23, 27, 35]
# N = [17, 23, 27, 35, 39, 47, 59, 63, 75, 83, 87, 95, 107, 123, 135, 143, 147, 159, 167, 179, 183, 195, 203, 207, 215]
# algo = 'greedy2'
algo = 'perfect16'

for n in N:
    r, s = main(n, algo)
    print('monochromatic triangles = ', s)
    # print('solution string: ', r)

    store_results(n, r, s)

    trianglesingraph = int(n * (n - 1) * (n - 2) / 6)
    arcsingrapgh = int(n * (n - 1) / 2)
    # totalstates = 3 ** arcsingrapgh

    # print('tris = ', trianglesingraph, ' arcs = ', arcsingrapgh, '\n')
    print('\n')

print('full procedure ran in ', time.time() - start, ' seconds')
