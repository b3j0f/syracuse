from sys import stdout
import csv


def csvoutput(fields, values, output=None):
    def write(file):
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for entry in entries:
            row = {}
            for field in fields:
                row[field] = getattr(entry, field)
            writer.writerow(row)

    if output is None:
        write(stdout)

    else:
        with open(output, 'w', newline='') as file:
            write(file)
