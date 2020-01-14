from sys import stdout


def stdoutput(fields, values, output=None):
    def write(file):
        file.write('({0}):'.format(', '.join(fields)))
        outputvalues = []
        for value in values:
            outputval = []
            for field in fields:
                outputval.append(getattr(value, field))
            outputvalues.append(outputval)
        file.write('{0}\n'.format(outputvalues))

    if output:
        with open('w', output) as file:
            write(file)

    else:
        write(stdout)
