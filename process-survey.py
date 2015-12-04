from csv import DictReader, DictWriter
import sys
from copy import copy

from medicines import MEDS


def print_rows(rows):
    writer = DictWriter(sys.stdout, fieldnames=sorted(rows[0].keys()))

    writer.writeheader()
    for r in rows:
        writer.writerow(r)


def parse_file(fname):
    rows = []

    with open(fname, 'r') as f:
        reader = DictReader(f)
        for r in reader:
            template = copy(r)

            # remove medicines from template
            for code in MEDS.iterkeys():
                for k in template.keys():
                    # eg. aba/aba-in_stock
                    if k.startswith(code + '/'):
                        del template[k]

            # transfrom medicine results from columns into rows
            for code, name in MEDS.iteritems():
                row = copy(template)
                row['medicine'] = name

                for k, v in r.iteritems():
                    if k.startswith(code + '/'):
                        # eg. aba/aba-in_stock - > in_stock
                        after = k[len(code) * 2 + 2:]
                        row[after] = v

                rows.append(row)

    print_rows(rows)


if __name__ == '__main__':
    parse_file(sys.argv[1])
