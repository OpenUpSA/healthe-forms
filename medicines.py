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


def med_code(med):
    if len(med) > 1:
        name, code = med
    else:
        name = med[0]
        code = name.lower()[0:3]

    return name, code


MEDS = {}
for med in MEDICINES:
    name, code = med_code(med)

    MEDS[code] = name
