#-*- coding:utf-8 -*-
import sys
import random
from problem import read_instance, evaluate

class SGA(object):

    def __init__(self, instance):
        self.instance = instance # (size, distances[][], time windows[][])
        self.best = None
        self.log = ([], [])

    def go(self, size, iterations, param_c, param_m):
        self.size = size
        population = self.random_population(size)
        self.evaluate_population(population)
        for i in xrange(iterations):
            self.i = i
            ps = self.crossover(population, param_c)
            if not ps:
                break
            population = self.mutation(ps, param_m)
            self.evaluate_population(population)

        print evaluate(instance, self.best[1], True), 
        return self.log

    def evaluate_population(self, population):
        weighted = sorted([(evaluate(self.instance, elem), elem) for elem in population])
        if not self.best or self.best[0] < weighted[0][0]:
            if self.best:
                print "improved from %d to %d (iter %d)" % (self.best[0], weighted[0][0], self.i)
                print "current best = ", evaluate(instance, self.best[1], True)
                self.log[0].append(self.i)
                self.log[1].append(abs(weighted[0][0]))
            self.best = weighted[0]
    
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
        while len(np) < self.size:
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
        for i in xrange(1, self.instance[0]):
            if i not in c1 or i not in c2:
                raise Exception("PMX assertion error %d" % i)
        return c1, c2
        
    def mutation(self, population, param_m):
        results = []
        for elem in population:
            if random.uniform(0, 1) < param_m:  # small probability of mutation
                ta, tb = self.random_divide()
                if random.uniform(0, 1) < 0.5:
                    # swap mutation
                    elem = elem[:ta] + elem[tb:tb+1] + elem[ta+1:tb] + elem[ta:ta+1] + elem[tb+1:]
                else:
                    # shift mutation
                    elem = elem[:ta] + elem[ta+1:tb] + elem[ta:ta+1] + elem[tb:]
            results.append(elem)

        return results 

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "USAGE: python sga.py <input filename>"
        exit(1)
    else:
        instance = read_instance(sys.argv[1])
        sga = SGA(instance)
        # params:
        # population size, iterations, crossover chance, mutation chance
        sga.go(1000, 1000, 0.99, 0.03)

#from matplotlib import pyplot as plt
#def plot(data, title, file):
    #plt.clf()

    #plt.ylabel('Score')
    #plt.xlabel('Iteration')

    #for line in data:
        #plt.plot(line[0], line[1])

    #plt.title(title)

    #plt.savefig(file)
    #print 'saved to %s' % file
#def test_sga():
    #logs = []
    #for i in xrange(10):
        #s = SGA(N, L, T)
        #logs.append(s.go(100, 0, 0))
    #return logs
# plot(test_sga(), 'SGA + PMX + Swap & Shift Mutations', 'out.png')

# TODO's:
# spowolnic przeszukiwanie
# rozgladac sie na boki
# parametr mutacji
# rodzaje mutacji
# rodzaje krzyzowania
# normalizacja score przy wybieraniu rodzicow
# wielkosc populacji
