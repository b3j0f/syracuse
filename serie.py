from src.lib import getserie, DEGREE
from argparse import ArgumentParser

from src.output.chart import chartoutput
from src.output.csv import csvoutput
from src.output.std import stdoutput


def parseargs():
    parser = ArgumentParser()
    parser.add_argument("value", help="value", type=int)
    parser.add_argument(
        "-e", "--even", help="add even steps", action="store_true"
    )
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
    parser.add_argument(
        "-l", "--large", help="show large pos (2n-2n+2, n even)",
        action="store_true"
    )
    parser.add_argument(
        "-m", "--mid", help="show mid pos (2n,2n+1)", action="store_true"
    )
    parser.add_argument(
        "-t", "--tiny", help="show tiny pos (2n,2n+2n+1)", action="store_true"
    )

    return parser.parse_args()


VIEWS = {
    'points': chartoutput,
    'csv': csvoutput
}

FIELDS = [
    # 'value',
    # 'pos',
    # 'poseven',
    # 'posmid'
]


def getstats(serie):
    print('length: ', len(serie))


def main():
    args = parseargs()

    serie = getserie(args.value, degree=args.degree)

    if not args.even:
        serie = list(term for term in serie if term.value & 1 == 1)

    getstats(serie)

    fields = []
    if args.tiny:
        fields.append('posmid')
    if args.mid:
        fields.append('pos')
    if args.large:
        fields.append('poseven')

    viewed = False
    for view in VIEWS:
        if getattr(args, view):
            viewed = True
            VIEWS[view](fields, serie, args.output)

    if not viewed:
        stdoutput(FIELDS, serie, args.output)


if __name__ == '__main__':
    main()
