from csv import DictReader, DictWriter
import sys
from copy import copy
import os.path
import arrow
from xlsxwriter.workbook import Workbook

from utils import MEDS, PROVINCES, DISTRICTS

HEADINGS_WHITE = ['Date', 'Province', 'District', 'Clinic Name', 'Clinic Contact', 'Latitute', 'Longitude', 'Monitor Name', 'Medicine Name',]
HEADINGS_GREEN = ['In Stock?', ]
HEADINGS_BLUE = ['No Stock - Not used at PHC', 'No Stock - Ordered per Patient', 'No Stock - Ordered at Depot', 'No Stock - Ordered per patient, ordered at Depot', ]
HEADINGS_ORANGE = ['No Stock - Order Date', 'No Stock - Depot out of Stock']


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

        r['date'] = r['end'].split('T', 2)[0]


def generate_report(rows):
    decorate(rows)

    fields = ['date', 'facility_details/province', 'facility_details/district', 'facility_details/facility',
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


def write_xlsx(fname, period_rows, report_rows, report_fields):
    """
    See http://stackoverflow.com/questions/32205927/xlsxwriter-and-libreoffice-not-showing-formulas-result
    """
    workbook = Workbook(fname)
    heading = workbook.add_format({
        'bold': True,
        'bottom': 1,
        'text_wrap': True,
        'font_name': 'Arial',
    })
    count = workbook.add_format({
        'bold': True,
        'top': 1,
        'font_name': 'Arial',
    })
    percent = workbook.add_format({
        'bold': True,
        'num_format': '0%',
        'font_name': 'Arial',
    })
    common = workbook.add_format({
        'font_name': 'Arial',
    })
    heading_green = workbook.add_format({
        'bold': True,
        'bottom': 1,
        'text_wrap': True,
        'font_name': 'Arial',
        'bg_color': 'b6d7a8',
    })
    heading_blue = workbook.add_format({
        'bold': True,
        'bottom': 1,
        'text_wrap': True,
        'font_name': 'Arial',
        'bg_color': '9fc5e8',
    })
    heading_orange = workbook.add_format({
        'bold': True,
        'bottom': 1,
        'text_wrap': True,
        'font_name': 'Arial',
        'bg_color': 'f9cb9c',
    })

    report_sheet = workbook.add_worksheet('Report')
    data_sheet = workbook.add_worksheet('Data')

    # Column headings
    for c, label in enumerate(HEADINGS_WHITE):
        report_sheet.write(0, c, label, heading)
    for c, label in enumerate(HEADINGS_GREEN):
        report_sheet.write(len(HEADINGS_WHITE), c, label, heading)
    for c, label in enumerate(HEADINGS_BLUE):
        report_sheet.write(c, c, label, heading)
    for c, label in enumerate(HEADINGS_ORANGE):
        report_sheet.write(c, c, label, heading)
    # adjust widths and height
    report_sheet.set_row(0, 65)
    report_sheet.set_column('A:B', 13)
    report_sheet.set_column('C:D', 25)
    report_sheet.set_column('E:H', 11)
    report_sheet.set_column('I:I', 50)
    report_sheet.set_column('J:P', 15)

    # Worsheet data
    for r, row in enumerate(report_rows, 1):
        for key, val in row.iteritems():
            report_sheet.write(r, report_fields.index(key), val, common)
    # Data copy
    data_fields = sorted(set(k for r in period_rows for k in r.keys()))
    for col, field_name in enumerate(data_fields):
        data_sheet.write(0, col, field_name, common)
    for r, row in enumerate(period_rows, 1):
        for key, val in row.iteritems():
            data_sheet.write(r, data_fields.index(key), val, common)

    # Totals
    total_row0 = len(report_rows) + 1
    formula = '=COUNTA('+colalpha(8)+'2:'+colalpha(8)+str(len(report_rows))+')'
    report_sheet.write_formula(total_row0, 8, formula, count)
    for col in range(9, 14):
        yes_count_cell(report_sheet, len(report_rows), total_row0, col, count)
    yes_count_cell(report_sheet, len(report_rows), total_row0, 15, count)
    formula = '='+colalpha(9)+str(total_row0+1)+'/'+colalpha(8)+str(total_row0+1)
    report_sheet.write_formula(total_row0+1, 9, formula, percent)

    workbook.close()


def yes_count_cell(sheet, rows, row, col, cellformat):
    formula = '=COUNTIF('+colalpha(col)+'2:'+colalpha(col)+str(rows)+', "=yes")'
    sheet.write_formula(row, col, formula, cellformat)


def colalpha(n):
    return chr(n + ord('a'))


def make_fname(fname, suffix):
    base, ext = os.path.splitext(fname)
    return ''.join([base, '-', suffix, ext])


def do_everything(fname, start_date):
    period_rows = process_survey(fname, arrow.get(start_date + 'T00:00:00+0200'))
    write_rows(make_fname(fname, 'processed'), period_rows)

    report_rows, fields = generate_report(period_rows)
    write_rows(make_fname(fname, 'report'), report_rows, fields)

    write_xlsx(make_fname(fname, 'report')+'.xlsx', period_rows, report_rows, fields)


if __name__ == '__main__':
    do_everything(sys.argv[1], sys.argv[2])
