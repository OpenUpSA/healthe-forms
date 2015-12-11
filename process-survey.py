from csv import DictReader, DictWriter
import sys
from copy import copy
import os.path
import arrow

from utils import MEDS, PROVINCES, DISTRICTS


def write_rows(fname, rows, fields=None):
    print "Writing %s" % fname
    if fields is None:
        fields = sorted(set(k for r in rows for k in r.keys()))

    with open(fname, 'w') as f:
        writer = DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for r in rows:
            writer.writerow(r)


def decorate(rows):
    for r in rows:
        # fold in clinic name
        if r['facility_details/facility'] == 'other':
            r['facility_details/facility'] = r['facility_details/facility_other']

        # province
        r['facility_details/province'] += ' - ' + PROVINCES[r['facility_details/province']]
        r['facility_details/district'] += ' - ' + DISTRICTS[r['facility_details/district']]


def generate_report(rows):
    decorate(rows)

    fields = ['end', 'facility_details/province', 'facility_details/district', 'facility_details/facility',
              'facility_details/contact', 'basics/_gps_latitude', 'basics/_gps_longitude', 'basics/monitor',
              'medicine', 'in_stock', 'no stock - not_used_phc', 'no stock - per_patient', 'no stock - depot_order',
              'no stock - per_patient_depot_order', 'date_ordered']

    output = [{f: r.get(f) for f in fields} for r in rows]
    return output, fields


def process_survey(fname, start_date):
    rows = []

    with open(fname, 'r') as f:
        reader = DictReader(f)
        for r in reader:
            # in range?
            if arrow.get(r['end'] + '00') < start_date:
                print 'Ignoring entry from %s because it is before %s' % (r['end'], start_date)
                continue

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

                # add extra columns for stockout details
                if row['in_stock'] != 'yes':
                    row['no stock - %s' % row['stockout_reason']] = 'yes'

                rows.append(row)
    return rows


def make_fname(fname, suffix):
    base, ext = os.path.splitext(fname)
    return ''.join([base, '-', suffix, ext])


def do_everything(fname, start_date):
    rows = process_survey(fname, arrow.get(start_date + 'T00:00:00+0200'))
    write_rows(make_fname(fname, 'processed'), rows)

    rows, fields = generate_report(rows)
    write_rows(make_fname(fname, 'report'), rows, fields)


if __name__ == '__main__':
    do_everything(sys.argv[1], sys.argv[2])
