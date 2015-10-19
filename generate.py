from facilities import clinics_by_province, province_codes, district_codes

MEDICINES = [
    ('Abacavir 20 mg/mL solution (240 mL)',),
    ('Adrenaline 1 mg/ml injection (1 mL ampoule)',),
    ('Amoxicillin 125 mg/5ml suspension (75 or 100 mL)', 'amosus'),
    ('Amoxicillin 250 mg or 500 mg capsules (15 capsules)', 'amocap'),
    ('Beclomethasone 50 mcg or 100 mcg inhaler (200 inhalations)',),
    ('Carbamazepine 200 mg tablets (28, 56 or 84 tablets)',),
    ('Cefixime 400 mg capsules (1 capsule)', 'cef'),
    ('Ceftriaxone injection 250 mg or 500 mg (vial)', 'cex'),
    ('DTaP-IPV/Hib (Pentavalent) Vaccine (EPI)',),
    ('Hydrochlorothiazide 12.5 or 25 mg tablets (28 tablets)',),
    ('Insulin soluble 100IU/ml injection (10 mL vial)',),
    ('Isoniazid 300 mg tablet (28 tablets)',),
    ('Lamivudine 10 mg/mL solution (240 mL)',),
    ('Medroxyprogesterone injection 150 mg (1 mL vial)',),
    ('Metformin 500 mg or 850 mg tablets (56 or 84 tablets)',),
    ('Paracetamol 500 mg tablets (10 or 20 tablets)', 'partab'),
    ('Paracetamol syrup 120 mg/5mL (50 mL or 100 mL)', 'parsyr'),
    ('Rifampicin 150 mg, isoniazid 75 mg, pyrazinamide 400 mg and ethambutol 275 mg tablets  (28, 56 or 84 tablets)', 'rif150'),
    ('Rifampicin 60mg and isoniazid 60 mg dispersible tablet (28 or 56 tablets)', 'rif60'),
    ('Sodium chloride 0.9% 1L',),
    ('Tetanus toxoid vaccine (10 doses)',),
    ('Tenofovir 300 mg, emtricitabine 200 mg, efavirenz 600 mg tablet, 28 tablets  (FDC)',),
]


def medicine_elements():
    rows = []
    count = len(MEDICINES)

    for i, med in enumerate(MEDICINES):
        if len(med) > 1:
            name, code = med
        else:
            name = med[0]
            code = name.lower()[0:3]

        rows.append((code, 'begin group', '%d/%d: %s' % (i + 1, count, name)))
        rows.append(('%s-in_stock' % code, 'select_one yes_no', 'Is the medicine in stock?', '', 'yes'))
        rows.append(('%s-stockout_reason' % code, 'select_one no_stock_detail', 'What are the details of the stockout?', '', 'yes', '', "${%s-in_stock} = 'no'" % code))
        rows.append(('%s-date_ordered' % code, 'date', 'When was the medicine ordered?', '', 'yes', '', "${%s-stockout_reason} = 'depot_order' or ${%s-stockout_reason} = 'per_patient_depot_order'" % (code, code)))
        rows.append(('', 'end group'))

    return rows


def facility_elements():
    rows = []

    for province in sorted(clinics_by_province.keys()):
        prov = province_codes[province]
        districts = clinics_by_province[province]

        for district in sorted(districts.keys()):
            dist = district_codes[district]

            for clinic in sorted(districts[district]):
                rows.append(('facilities', clinic, clinic, prov, dist))

            rows.append(('facilities', 'other', 'Other facility not listed', prov, dist))

    return rows


def province_elements():
    rows = []
    for province in sorted(province_codes.keys()):
        rows.append(('provinces', province_codes[province], province))
    return rows


def district_elements():
    rows = []
    for province in sorted(province_codes.keys()):
        prov = province_codes[province]

        for district in sorted(clinics_by_province[province].keys()):
            rows.append(('districts', district_codes[district], district, prov))
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
