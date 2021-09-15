

# Create a string formatted as an acceptable entry to AZsPCs and store in a text file.
# This means that we concatenate the result strings and separate them with semicolons
# param path: string for where to store entry.
# param result_string: string representing the graph coloring
def write_entry(p, result_strings):
    content = ''
    for string in result_strings:
        content += string[:-2]
        content += '; '
    content = content[:-2]
    file = open(p, "w")
    file.write(content)
    file.close()


# numbers: list of numbers
# returns a list of solutions strings stored in results/n for n in N
def collect_results(numbers):
    result_strings = []
    for n in numbers:
        p = "results/" + str(n) + ".txt"
        try:
            file = open(p, "r")
            content = file.readlines()
            file.close()
            result_strings.append(content[1])

        except IOError:
            print('did not find file at path: ', p, '. Skipping this one')

    return result_strings


N = [17, 23, 27, 35, 39, 47, 59, 63, 75, 83, 87, 95, 107, 123, 135, 143, 147, 159, 167, 179, 183, 195, 203, 207, 215]
path = "entryResults.txt"
res_s = collect_results(N)
write_entry(path, res_s)
