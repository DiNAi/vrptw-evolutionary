import random
import sys
from problem import read_instance, evaluate

def random_solution(n):
    solution = range(1, n)
    random.shuffle(solution)
    return solution

def go_rand(iters):
    berr, bdist = None, None
    for i in xrange(iters):
        err, dist = evaluate(instance, random_solution(instance[0]), True)
        if not berr or (err <= berr and dist <= bdist):
            berr, bdist = err, dist
    print berr, bdist

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "USAGE: python sga.py <input filename>"
        exit(1)
    else:
        instance = read_instance(sys.argv[1])
        go_rand(1000 * 100)
