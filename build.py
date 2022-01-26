import pandas as pd
import csv

def buildPat(row,key):
    if key == "extension.valueAddress.city":
        return row.A01_DESC_LUOGO_NASCITA
    elif key == "identifier.value":
        return row.A01_ID_PERSONA
    elif key == "name.family":
        return row.A01_COGNOME
    elif key == "name.given":
        return row.A01_NOME
    elif key == "gender":
        if row.A01_SESSO=='M':
            return 'male'
        elif row.A01_SESSO=='F':
            return 'female'
        else:
            return 'unknown'
    elif key == "birthDate":
        if isinstance(row.A01_DATA_NASCITA,str):
            return row.A01_DATA_NASCITA[:10]
        else:
            return row.A01_DATA_NASCITA.strftime("%Y-%m-%d")
    elif key == "contact.relationship.coding.code":
        if row.A02_DESC_TELEFONO1 in ("MAMMA","PAPA'","MADRE","PADRE"):
            return 'PRN'
        elif row.A02_DESC_TELEFONO1 == "ZIA":
            return 'AUNT'
        elif row.A02_DESC_TELEFONO1 == "ZIO":
            return 'UNCLE'
        else:
            return ''
    elif key == "contact.relationship.coding.display":
        if row.A02_DESC_TELEFONO1 in ("MAMMA","PAPA'","MADRE","PADRE"):
            return 'parent'
        elif row.A02_DESC_TELEFONO1 == "ZIA":
            return 'aunt'
        elif row.A02_DESC_TELEFONO1 == "ZIO":
            return 'uncle'
        else:
            return ''
    elif key == "contact.telecom.emailvalue":
        return row.A02_EMAIL
    elif key == "contact.telecom.phonevalue":
        return row.A02_NUM_TELEFONO1
    elif key == "contact.relationship.coding.code2":
        if row.A02_DESC_TELEFONO2 in ("MAMMA","PAPA'","PAPA","MADRE","PADRE"):
            return 'PRN'
        elif row.A02_DESC_TELEFONO2 == "ZIA":
            return 'AUNT'
        elif row.A02_DESC_TELEFONO2 == "ZIO":
            return 'UNCLE'
        else:
            return ''
    elif key == "contact.relationship.coding.display2":
        if row.A02_DESC_TELEFONO2 in ("MAMMA","PAPA'","PAPA","MADRE","PADRE"):
            return 'parent'
        elif row.A02_DESC_TELEFONO2 == "ZIA":
            return 'aunt'
        elif row.A02_DESC_TELEFONO2 == "ZIO":
            return 'uncle'
        else:
            return ''
    elif key == "contact.telecom.phonevalue2":
        return row.A02_NUM_TELEFONO2

def buildCond(row,key):
    if key == "extension.valueDateTime":
        if isinstance(row.DT_REGISTRAZIONE,str):
            return row.DT_REGISTRAZIONE[:10]
        else:
            return row.DT_REGISTRAZIONE.strftime("%Y-%m-%d")
    elif key == "bodySite.coding.code":
        if row.TITOLO_LIV2 == "Sottosede":
            return row.CODICE_LIV2
    elif key == "bodySite.text":
        if row.TITOLO_LIV2 == "Sottosede":
            return row.DESC_LIV2
    elif key == "stage.summary.text":
        if row.TITOLO_LIV2 == "Stadio":
            stadio = row.CODICE_LIV2.split()[1]
            return stadio
    elif key == "subject.reference":
        return "Patient/"+row.ID_PAZIENTE
    elif key == "recordedDate":
        if isinstance(row.DT_REGISTRAZIONE,str):
            return row.DT_REGISTRAZIONE[:10]
        else:
            return row.DT_REGISTRAZIONE.strftime("%Y-%m-%d")
    elif key == "description":
        return row.DESC_LIV2