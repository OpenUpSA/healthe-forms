# healthe-forms
Generates Health-E forms and post-processes collected data.

# setup

* virtualenv --no-site-packages env
* source env/bin/activate
* pip install -r requirements.txt

# generating forms

We generate the forms mostly so that we can generate the corresponding lists automatically, since
there are many health facilities and many medicines.

    python generate.py

# processing a survey

* download as CSV
* run `python process-survey.py CSV-FILE START-DATE`

For more detail see https://docs.google.com/document/d/1D6baIDar7KotHe_qH1rbgd55xfxwBZz-5YQJ5BLtxhQ/edit

