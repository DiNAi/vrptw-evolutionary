#-*- coding:utf-8 -*-
import sys
import math
import random
from problem import read_instance, evaluate

class SA(object):

    def __init__(self, instance):
        self.instance = instance

    def go(self, iters, temp, modif):
        vect = self.random_perm()
        best = vect, abs(evaluate(self.instance, vect))
        solution, score = best
        for i in xrange(iters):
            if temp == 0: break
            nsolution, nscore = self.get_neighbour(solution)

            if nscore < best[1]:
                best = nsolution, nscore

            if nscore < score or math.exp((score - nscore) / temp) > random.random():
                solution, score = nsolution, nscore

            temp = temp * modif

        return best[1], evaluate(self.instance, best[0], True)

    def get_neighbour(self, solution):
        ls = len(solution)
        c1 = c2 = random.randrange(0, ls)
        excl = [c1, ls - 1 if c1 == 0 else c1 - 1, 0 if c1 == ls - 1 else c1 + 1]
        while c2 in excl:
            c2 = random.randrange(0, ls)
        c1, c2 = min(c1, c2), max(c1, c2)
        solution = solution[:c1+1] + solution[c2:c1:-1] + solution[c2+1:]
        return solution, abs(evaluate(self.instance, solution))

    def random_perm(self):
        x = range(1, self.instance[0])
        random.shuffle(x)
        return x

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "USAGE: python sa.py <input filename>"
        exit(1)
    else:
        instance = read_instance(sys.argv[1])
        bs1, bs2 = None, None
        for i in xrange(500):
            sa = SA(instance)
            s1, s2 = sa.go(5000, 500000., 0.89)
            if not bs1 or s2 < bs2:
                print s1, s2
                bs1, bs2 = s1, s2

        print bs1, bs2

