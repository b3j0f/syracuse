import matplotlib.pyplot as plt
from math import log2


def chartoutput(fields, values, output=None):
    outputvalues = {}

    for field in fields:
        outputvalues[field] = []
    # values = []
    # pcts = []
    # lengths = []
    # oddlengths = []
    # nextevens = []
    # nextnextevens = []
    # diffs = []
    # pctnextevens = []
    # pctnextnextevens = []

    for value in values:
        for field in fields:
            outputvalues[field].append(getattr(value, field))

    fig, ax = plt.subplots()
    funcs = {
        'plot': ax.plot,
        'scatter': ax.scatter
    }

    x = list(range(len(values)))

    for field in fields:
        ax.plot(x, outputvalues[field], label=field)

    # binpows = []
    # for i in range(entries[0].value, entries[-1].value):
    #     val = 2 ** round(log2(i))
    #     midval = (val * 2 - val) / 2 + val
    #     if val not in binpows:
    #         binpows += [val, midval]
    #
    # binpows = binpows[:-1]
    # ax.scatter(binpows, binpows, label="binpows")

    ax.legend()

    # ax.setxlabel('values')
    if output:
        fig.savefig(output)

    else:
        plt.show()
