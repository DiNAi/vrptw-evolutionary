import re

def read_instance(filename):
    with open(filename, 'r') as fl:
        size = int(fl.readline())
        distances = []
        for i in xrange(size):
            distances.append([float(x) for x in re.split('\s+', fl.readline()) if x])
        windows = []
        for i in xrange(size):
            windows.append([float(x) for x in re.split('\s+', fl.readline()) if x])
    return size, distances, windows

def evaluate(instance, solution, verbose=False):
    size, distances, windows = instance

    if len(solution) + 1 != size: raise Exception('Invalid permutation size')

    current = 0
    cost = 0
    violations = 0
    makespan = 0

    for node in solution + [0]:
        cost += distances[current][node]
        makespan = max(makespan + distances[current][node], windows[node][0])
        if makespan > windows[node][1]:
            violations += 1
        current = node

    if verbose:
        return violations, cost
    else:
        return -cost * (1 + violations * 10) ** 2

def test():
    instance = read_instance('instances/rc_201.1.txt')
    opt = [14, 18, 13, 9, 5, 4, 6, 8, 7, 16, 19, 11, 17, 1, 10, 3, 12, 2, 15]
    violations, distance = evaluate(instance, opt, True)
    assert violations == 0
    assert abs(444.542 - distance) < 0.001

if __name__ == '__main__': 
    test()
