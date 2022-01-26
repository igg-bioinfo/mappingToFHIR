# mappingToFHIR

This repository allows to perform a mapping of clinical data extracted from EMRs of cancer patients in FHIR (https://www.hl7.org/fhir/).

In the main.py file you can set the flags for the automatic generation of the Patient and Condition FHIR-compliant resources starting from the data extracted from the medical record. The latter can come directly from the database server or from a .csv file exported from it.

The generated .json files are finally sent to the server which converts them into FHIR resources.
