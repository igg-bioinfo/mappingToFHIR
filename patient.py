from build import buildPat
from cleaning import remove_empty_from_dict

def func_dictPat(df):
    extension_valueAddress_city = ""
    identifier_value = ""
    name_family = ""
    name_given = ""
    gender = ""
    birthDate = ""
    contact_relationship_coding_code = ""
    contact_relationship_coding_display = ""
    contact_telecom_emailvalue = ""
    contact_telecom_phonevalue = ""
    contact_relationship_coding_code2 = ""
    contact_relationship_coding_display2 = ""
    contact_telecom_phonevalue2 = ""

    for r in range(0,len(df.index)):
        row = df.iloc[r]
        extension_valueAddress_city = buildPat(row, "extension.valueAddress.city")
        identifier_value = buildPat(row, "identifier.value")
        name_family = buildPat(row, "name.family")
        name_given = buildPat(row, "name.given").split()
        gender = buildPat(row, "gender")
        birthDate = buildPat(row, "birthDate")
        contact_relationship_coding_code = buildPat(row, "contact.relationship.coding.code")
        contact_relationship_coding_display = buildPat(row, "contact.relationship.coding.display")
        contact_telecom_emailvalue = buildPat(row, "contact.telecom.emailvalue")
        contact_telecom_phonevalue = buildPat(row, "contact.telecom.phonevalue")
        contact_relationship_coding_code2 = buildPat(row, "contact.relationship.coding.code2")
        contact_relationship_coding_display2 = buildPat(row, "contact.relationship.coding.display2")
        contact_telecom_phonevalue2 = buildPat(row, "contact.telecom.phonevalue2")

    dictPat = {
        'resourceType': 'Patient',
        "meta" : {
            "profile" : [
                "http://hl7.eu/fhir/ig/pcsp/StructureDefinition/Patient-eu-pcsp"
            ]
        },
        "extension" : [
        {
            "url" : "http://hl7.org/fhir/StructureDefinition/patient-birthPlace",
            "valueAddress" : {
                "city" : extension_valueAddress_city,
            }
        }
        ],
        "identifier" : [
        {
            "system" : "jdbc:oracle:thin",
            "value" : identifier_value
        }
        ],
        'name': [
        {  
            'family': name_family,
            'given': name_given 
        }
        ],
        'gender': gender,
        'birthDate': birthDate,
        'contact': [
        {
            "relationship": [
            {
                "coding": [
                {
                    "system": "http://terminology.hl7.org/CodeSystem/v3-RoleCode",
                    "code": contact_relationship_coding_code,
                    "display": contact_relationship_coding_display
                }
                ]
            }
            ],
            'telecom': [
            {
                "system": "email",
                "value": contact_telecom_emailvalue
            },
            {
                "system": "phone",
                "value": contact_telecom_phonevalue
            }
            ]
        },
        {
            "relationship": [
            {
                "coding": [
                {
                    "system": "http://terminology.hl7.org/CodeSystem/v3-RoleCode",
                    "code": contact_relationship_coding_code2,
                    "display": contact_relationship_coding_display2
                }
                ]
            }
            ],
            'telecom': [
            {
                "system": "phone",
                "value": contact_telecom_phonevalue2
            }
            ]
        }
        ]
    }

    # ***POSSIBLE MODIFICATION***
    # we could manage the emptiness of the fields by doing for example:
    # "value": contact_telecom_phonevalue if contact_telecom_phonevalue != "" else "NOT AVAILABLE"

    #### AUTOMATIC CLEANING ####
    dictPat = remove_empty_from_dict(dictPat)
    
    #### MANUAL CLEANING ####
    # if dictPat['extension'][0]['valueAddress']['city'] == "":
    #     del(dictPat['extension'])
    # if dictPat['name'][0]['family'] == "":
    #     del(dictPat['name'][0]['family'])
    # if dictPat['name'][0]['given'][0] == "":
    #     del(dictPat['name'][0]['given'])
    # if dictPat['gender'] == "":
    #     del(dictPat['gender'])
    # if dictPat['birthDate'] == "":
    #     del(dictPat['birthDate'])  

    # if dictPat['contact'][0]['relationship'][0]['coding'][0]['code'] == "":
    #     del(dictPat['contact'][0]['relationship'])
    # if dictPat['contact'][0]['telecom'][0]['value'] == "":
    #     del(dictPat['contact'][0]['telecom'][0])
    #     if dictPat['contact'][0]['telecom'][0]['value'] == "":
    #         del(dictPat['contact'][0]['telecom'][0])
    # elif dictPat['contact'][0]['telecom'][1]['value'] == "":
    #     del(dictPat['contact'][0]['telecom'][1])

    # if dictPat['contact'][1]['relationship'][0]['coding'][0]['code'] == "":
    #     del(dictPat['contact'][1]['relationship'])
    # if dictPat['contact'][1]['telecom'][0]['value'] == "":
    #     del(dictPat['contact'][1]['telecom'])
    # if not dictPat['contact'][1]:
    #     del(dictPat['contact'][1])
    
    return dictPat