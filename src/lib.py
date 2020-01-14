from collections import namedtuple
from math import log2

Entry = namedtuple(
    'Entry', [
        'value',
        'pct', 'length', 'oddlength',
        'nexteven', 'nextnexteven',
        'pctnexteven', 'pctnextnexteven'
    ]
)

_cache = {}  # cache of entries


def freecache():
    _cache = {}


DEGREE = 3  # default degree


def syr(value, degree=DEGREE):
    return int(value / 2 if value % 2 == 0 else degree * value + 1)


def pct(v):
    return 0 if v is None else log2(v) - int(log2(v))


Term = namedtuple(
    'Term',
    ['value', 'pos', 'poseven', 'posmid']
)


def poseven(value, n):
    isp = n & 1 == 0
    minpos = 2 ** (n - (0 if isp else 1))
    maxpos = 2 ** (n + (2 if isp else 1))

    return (value - minpos) * 100 / (maxpos - minpos)


def posmid(value, n):
    mid = (2 ** n + 2 ** (n - 1))

    if value > mid:
        minpos = mid
        maxpos = (2 ** (n + 1))
    else:
        minpos = 2 ** n
        maxpos = mid

    return (value - minpos) * 100 / (maxpos - minpos)


def getterm(value):
    pos = log2(value)
    n = int(pos)
    vposmid = posmid(value, n)
    vposeven = poseven(value, n)

    return Term(value, (pos - n) * 100, vposeven, vposmid)


def getserie(value, degree=DEGREE):
    result = [getterm(value)]
    v = value

    while v != 1:
        v = syr(v, degree=degree)
        result.append(getterm(v))

    return result


def getentry(value, degree=DEGREE, cache=True):
    if cache:
        if degree in _cache:
            if value in _cache[degree]:
                return _cache[degree][value]
        else:
            _cache[degree] = {}

    nexteven = None
    nextnexteven = None
    length = 0
    oddlength = 0

    v = syr(value, degree=degree)

    while v != 1:
        length += 1
        if v & 1 == 1:
            oddlength += 1
            if nexteven is None:
                nexteven = v
            elif nextnexteven is None:
                nextnexteven = v

        if cache and v in _cache[degree]:
            entry = _cache[degree][v]
            length += 1 + entry.length
            oddlength += entry.oddlength
            if nexteven is None:
                nexteven = entry.nexteven
            elif nextnexteven is None:
                nextnexteven = entry.nextnexteven
            break

        v = syr(v, degree=degree)

    entry = Entry(
        value,
        pct(value), length, oddlength,
        nexteven, nextnexteven, pct(nexteven), pct(nextnexteven)
    )

    if cache:
        _cache[degree][value] = entry

    return entry


def getoddvalues(min, max):
    return (
        value for value in range(min, max + 1)
        if value & 1 == 1
    )


def getentries(min, max, degree=DEGREE, cache=True):
    values = getoddvalues(min=min, max=max)

    return (getentry(value, degree=degree, cache=cache) for value in values)
