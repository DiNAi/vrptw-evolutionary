
def next_permutation(permutation):
    n = len(permutation)
    permutation = map((lambda x: x - 1), permutation)
    a = 1
    for i in xrange(0, n):
        permutation[i] += a
        for j in xrange(0, i):
            if permutation[j] == permutation[i]:
                permutation[i] += 1
        a = permutation[i] / 10
        permutation[i] %= n

    permutation = map((lambda x: x + 1), permutation)
    return permutation

def silnia(n):
    if n == 1 :
        return 1
    else:
        return n * silnia(n-1)

print silnia(14)
print silnia(20)

x = [1,2,3, 4]
for i in xrange(10):
    print x 
    x = next_permutation(x)
