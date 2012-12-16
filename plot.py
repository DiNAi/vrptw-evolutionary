from matplotlib import pyplot as plt

def plot(data, title, file):
    plt.clf()

    plt.ylabel('Score')
    plt.xlabel('Iteration')

    for line in data:
        plt.plot(line[0], line[1])

    plt.title(title)
#    plt.yscale('log')

    plt.savefig(file)
    
    print 'Graph output saved to %s' % file
