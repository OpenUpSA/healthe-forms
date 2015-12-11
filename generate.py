from facilities import clinics_by_province
from utils import MEDS, DISTRICT_CODES, PROVINCE_CODES


def medicine_elements():
    rows = []
    count = len(MEDS)

    for i, med in enumerate(MEDS.items()):
        code, name = med
        rows.append((code, 'begin group', '%d/%d: %s' % (i + 1, count, name)))
        rows.append(('%s-in_stock' % code, 'select_one yes_no', 'Is the medicine in stock?', '', 'yes'))
        rows.append(('%s-stockout_reason' % code, 'select_one no_stock_detail', 'What are the details of the stockout?', '', 'yes', '', "${%s-in_stock} = 'no'" % code))
        rows.append(('%s-date_ordered' % code, 'date', 'When was the medicine ordered?', '', 'yes', '', "${%s-stockout_reason} = 'depot_order' or ${%s-stockout_reason} = 'per_patient_depot_order'" % (code, code)))
        rows.append(('', 'end group'))

    return rows


def facility_elements():
    rows = []

    for province in sorted(clinics_by_province.keys()):
        prov = PROVINCE_CODES[province]
        districts = clinics_by_province[province]

        for district in sorted(districts.keys()):
            dist = DISTRICT_CODES[district]

            for clinic in sorted(districts[district]):
                rows.append(('facilities', clinic, clinic, prov, dist))

            rows.append(('facilities', 'other', 'Other facility not listed', prov, dist))

    return rows


def province_elements():
    rows = []
    for province in sorted(PROVINCE_CODES.keys()):
        rows.append(('provinces', PROVINCE_CODES[province], province))
    return rows


def district_elements():
    rows = []
    for province in sorted(PROVINCE_CODES.keys()):
        prov = PROVINCE_CODES[province]

        for district in sorted(clinics_by_province[province].keys()):
            rows.append(('districts', DISTRICT_CODES[district], district, prov))
    return rows


#rows = medicine_elements()
#print '\n'.join('"' + '","'.join(r) + '"' for r in rows)

print "\n\n------\n\n"

rows = province_elements()
#print '\n'.join('"' + '","'.join(r) + '"' for r in rows)

print "\n\n------\n\n"

rows = district_elements()
#print '\n'.join('"' + '","'.join(r) + '"' for r in rows)

print "\n\n------\n\n"

rows = facility_elements()
print '\n'.join('"' + '","'.join(r) + '"' for r in rows)
