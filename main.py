import numpy as np
import time


# Greedy graph coloring algorithm that for each arc sets the smallest color
# it can without making a monochromatic triangle. Makes sense to me
# edit: it should aim to make tricolored graphs
def greedy(n):
    m = np.zeros((n, n), dtype=int)
    # m[2, 0] = 1
    # m[2, 1] = 2
    for i in range(1, n):
        m[i, 0] = i % 3
        for j in range(1, i):
            # i punkten (i, j) ska du titta i punkterna (i - 1, x) & (i, x) för alla x i [0, j - 1].
            # men hur ska jag sedan välja färg? välj färg att förbjuda? minuspoäng?
            penalty = [0, 0, 0]
            for x in range(j):
                if m[i - 1, x] == m[i, x]:
                    penalty[m[i - 1, x]] += 1
            m[i, j] = penalty.index(min(penalty))

    print(m)
    return m

# Now I want penalty 5 for mono and p 1 for non tricollor
def greedy2(n):
    m = np.zeros((n, n), dtype=int)
    for i in range(1, n):
        m[i, 0] = (i-1) % 3
        for j in range(1, i):
            # i punkten (i, j) tittar jag i {(i, x), (j, x)}, x in [0:j-1]
            # om ix == jx så får färgen p=5. i alla fall får färgen vi tittade på p =1
            penalty = [0, 0, 0]
            for x in range(j):
                if m[i, x] == m[j, x]:
                    penalty[m[i, x]] += 100
                else:
                    penalty[m[i, x]] += 1
                    penalty[m[j, x]] += 1
            for y in range(i):
                penalty[m[y,j]] += 5
            m[i, j] = penalty.index(min(penalty))
            # if j == 1:
                # print(penalty)

    print(m)
    return m


# Makes a matrix representing the colored graph
# param n: int representing the size of the graph
# param r: Bool for whether to use a random solver or not
# complexity = n2
def solver(n, r=None):
    # random solver
    if r:
        print('running random solver')
        m = np.zeros((n, n), dtype=int)
        rm = np.random.randint(3, size=(n, n))
        for i in range(1, n):
            for j in range(i):
                m[i, j] = rm[i, j]

    # non-random solver. Currently no algorithm in place
    else:
        print('running greedy algorithm')
        m = greedy2(n)
    return m


# counts the number of monochromatic triangles in the graph
# complexity = n3
def counter(m):
    n = len(m)
    count = 0

    for a in range(n):
        for b in range(a+1, n):
            for c in range(b+1, n):
                # print('looking at this triangle: ', a, b, c)
                if (m[b, a] == m[c, a]) and (m[b, a] == m[c, b]):
                    # print('adding onto current c. c = ', count)
                    count += 1

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
    color_matrix = solver(n, r=algo)
    # color_matrix = solver(n)
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


# make the code run for lists
start = time.time()
n = 17
iterations = 1
res = ''
score = 1e8
algo = False

for iter in range(iterations):
    r, s = main(n, algo)
    if s < score:
        score = s
        res = r

# res, score = main(n)
print('monochromatic triangles = ', score)

print('solution string: ', res)

store_results(n, res, score)
print('full procedure ran in ', time.time() - start, ' seconds')

trianglesingraph = int(n * (n - 1) * (n - 2) / 6)
arcsingrapgh = int(n * (n - 1) / 2)
totalstates = 3 ** arcsingrapgh

print('tris = ', trianglesingraph, ' arcs = ', arcsingrapgh, ' states = ', totalstates)