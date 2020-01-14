from src.lib import getentries, DEGREE
from argparse import ArgumentParser

from src.output.chart import chartoutput
from src.output.csv import csvoutput
from src.output.std import stdoutput


def parseargs():
    parser = ArgumentParser()
    parser.add_argument("range", help="[min:]maximal value")
    parser.add_argument(
        "-o", "--output", help="output file (default stdout)"
    )
    parser.add_argument(
        "-d", "--degree",
        help="degree (if value is odd, then next value is value * degree + 1)",
        default=DEGREE, type=int
    )
    parser.add_argument(
        "-p", "--points", help="point results", action="store_true"
    )
    parser.add_argument(
        "-c", "--csv", help="csv results", action="store_true"
    )
    return parser.parse_args()


VIEWS = {
    'points': chartoutput,
    'csv': csvoutput
}

FIELDS = [
    # 'value',
    'pct',
    # 'length',
    'oddlength',
    # 'nexteven',
    # 'nextnexteven',
    # 'pctnexteven',
    # 'pctnextnexteven'
]


def getstats(entries):
    maxEntry = None
    minEntry = None

    for entry in entries:
        if maxEntry is None:
            maxEntry = entry
            minEntry = entry
        else:
            if maxEntry.oddlength < entry.oddlength:
                maxEntry = entry
            if minEntry.oddlength > entry.oddlength:
                minEntry = entry

    print("max: {0}, min: {1}".format(maxEntry, minEntry))


def main():
    args = parseargs()

    r = args.range.split(':')
    min = 1
    if len(r) > 1:
        min, max = tuple(int(v) for v in r)
    else:
        max = int(r[0])

    entries = list(getentries(min=min, max=max, degree=args.degree))

    getstats(entries)

    viewed = False
    for view in VIEWS:
        if getattr(args, view):
            viewed = True
            VIEWS[view](FIELDS, entries, args.output)

    if not viewed:
        stdoutput(FIELDS, entries, args.output)


if __name__ == '__main__':
    main()
