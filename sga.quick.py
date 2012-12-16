#-*- coding:utf-8 -*-
import sys
import math
from plot import plot
import random
from problem import read_instance, evaluate

class SGA(object):

    def __init__(self, instance):
        self.instance = instance # (size, distances[][], time windows[][])
        self.best = None
        self.i = 0
        self.log = ([], [])

    def go(self, size, iterations, M, param_c, param_m):
        self.param_m = param_m
        self.size = size
        self.M = M
        self.T = 100000.
        self.Tn = 0.97
        population = self.random_population(size)
        self.evaluate_population(population)
        for i in xrange(1, iterations):
            self.i = i
            ps = self.crossover(population, param_c)
            if not ps:
                break
            childs = self.mutation(ps, self.param_m)
            population = self.replacement(population, childs)
            #print population[0]
            #print evaluate(self.instance, population[0])
            self.evaluate_population(population)

        print evaluate(instance, self.best[1], True), self.i
        return self.log, evaluate(instance, self.best[1], True)

    def replacement(self, population, childs):
        l = population + childs
        weighted = sorted([(evaluate(self.instance, elem), elem) for elem in l])
        new_population = weighted[len(childs):]
        return map((lambda (w, e): e), new_population)

    def evaluate_population(self, population):
        weighted = sorted([(evaluate(self.instance, elem), elem) for elem in population])
        self.log[0].append(self.i)
        self.log[1].append(abs(weighted[0][0]))
        uniq = len(set([w for w, x in weighted])) # prints number of unique elements in population
        ratio = 1. * uniq / self.size
        self.param_m = max(0.05, (1. - ratio) / 4.)

        if not self.best or self.best[0] < weighted[0][0]:
            #if self.best:
                #print "improved from %d to %d (iter %d, T=%f)" % (self.best[0], weighted[0][0], self.i, self.T)
            self.best = weighted[0]
        self.T = self.T * self.Tn

    def random_population(self, k):
        population = []
        for i in xrange(0, k):
            x = range(1, self.instance[0])
            random.shuffle(x)
            population.append(x)
        return population

    def lower_bound(self, roulette, k=None):
        if not k:
            k = random.uniform(0, 1)
        if len(roulette) == 1:
            return roulette[0][1]
        elif len(roulette) == 2:
            if roulette[0][0] > k:
                return roulette[0][1]
            else:
                return roulette[1][1]
        else:
            l = len(roulette) / 2
            (w, x) = roulette[l]
            if w >= k:
                return self.lower_bound(roulette[:l+1], k)
            else:
                return self.lower_bound(roulette[l:], k)
         
    def crossover(self, population, param_c):
        weighted = [(evaluate(instance, elem), elem) for elem in population]

        # exponential scaling
        results = [(math.exp(w / self.T), x) for (w, x) in weighted]

        min_f = min([w for (w, x) in weighted])
        sum_f = 0.
        for w in weighted:
            sum_f += w[0] - min_f

        if sum_f == 0.0:
            print "Population has 1 unique element"
            return []
        results = [((w-min_f)/sum_f, x) for (w, x) in weighted]

        roulette = []
        s = 0
        for w, x in results:
            s += w
            roulette.append((s, x))
        
        np = []
        while len(np) < self.M:
            parents = []
            while len(parents) < 2:
                parents.append(self.lower_bound(roulette))
            if random.uniform(0, 1) < param_c:
                c1, c2 = self.pmx(parents[0], parents[1])
            else:
                c1, c2 = parents[0], parents[1]     # small probability of no crossover

            np.append(c1)
            np.append(c2)
        return np

    def random_divide(self):
        ta = random.randrange(0, self.instance[0] - 1)
        tb = ta
        while tb == ta:
            tb = random.randrange(0, self.instance[0] - 1)
        ta, tb = min(ta, tb), max(ta, tb)
        return ta, tb

    def pmx(self, pa, pb):
        if len(pa) != len(pb):
            raise Exception("PMX assertion failed")
        k, m = self.random_divide()

        (la, lb, lc) = (pa[:k], pb[k:m], pa[m:])
        (ra, rb, rc) = (pb[:k], pa[k:m], pb[m:])

        map_a = {}
        map_b = {}
        for i in xrange(len(lb)):
            map_a[lb[i]] = rb[i]
            map_b[rb[i]] = lb[i]
        for (key, value) in map_a.items():
            origin = value
            while value in map_a and origin != map_a[value] and value != map_a[value]:
                value = map_a[value]
            map_a[key] = value 
        for (key, value) in map_b.items():
            origin = value
            while value in map_b and origin != map_b[value] and value != map_a[value]:
                value = map_b[value]
            map_b[key] = value 

        la = [map_a[x] if x in map_a else x for x in la]
        lc = [map_a[x] if x in map_a else x for x in lc]
        ra = [map_b[x] if x in map_b else x for x in ra]
        rc = [map_b[x] if x in map_b else x for x in rc]

        c1 = la + list(lb) + lc
        c2 = ra + list(rb) + rc

        # verify assertion 
        #for i in xrange(1, self.instance[0]):
            #if i not in c1 or i not in c2:
                #raise Exception("PMX assertion error %d" % i)
        return c1, c2

    def mutation(self, population, param_m):
        results = []
        for elem in population:
            if random.uniform(0, 1) < param_m:  # small probability of mutation
                ta, tb = self.random_divide()
                x = random.uniform(0, 1)
                if x < 0.2:
                    # swap mutation
                    elem = elem[:ta] + elem[tb:tb+1] + elem[ta+1:tb] + elem[ta:ta+1] + elem[tb+1:]
                elif x < 0.5:
                    # shift mutation
                    elem = elem[:ta] + elem[ta+1:tb] + elem[ta:ta+1] + elem[tb:]
                else:
                    # reverse mutation
                    elem = elem[:ta+1] + elem[tb:ta:-1] + elem[tb+1:]

            results.append(elem)

        return results

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "USAGE: python sga.py <input filename>"
        exit(1)
    else:
        scores = []
        results = []
        iters = 1 if len(sys.argv) == 2 else 10
        instance = read_instance(sys.argv[1])
        for i in xrange(iters):
            sga = SGA(instance)
            # go() params:
            # population size, iterations, crossover chance, mutation chance
            logs, (err, score) = sga.go(500, 2000, 450, 0.9, 0.05)
            results.append(logs)
            scores.append((err, score))
        scores.sort()
        print "Best score: ", scores[0]
        print "Average score:", 1. * sum([e for e, s in scores]) / len(scores),
        print 1. * sum([s for e, s in scores]) / len(scores)
        if len(sys.argv) > 2:
            inst = sys.argv[1].split('/')[-1]
            plot(results, 'SGA + PMX + Swap & Shift Mutations (instance: %s)'
                 % (inst), '%s_%s' % (inst, sys.argv[2]))
