from build import buildCond
from cleaning import remove_empty_from_dict

def func_dictCond(df):
    bodySite_coding_code = ""
    bodySite_text = ""
    stage_summary_text = ""
    description = ""

    for r in range(0,len(df.index)):
        row = df.iloc[r]
        if row.TITOLO_LIV2 == "Sottosede":
            bodySite_coding_code = buildCond(row, "bodySite.coding.code")
            bodySite_text = buildCond(row, "bodySite.text")
        elif row.TITOLO_LIV2 == "Stadio":
            stage_summary_text = buildCond(row, "stage.summary.text")
        elif row.TITOLO_LIV2 == "Istologia" or row.TITOLO_LIV2 == "Testo libero":
            description = buildCond(row, "description")
        recordedDate = buildCond(row, "recordedDate")
        subject_reference = buildCond(row, "subject.reference")
    
    dictCond = {
        "resourceType" : "Condition",
        "meta" : {
            "profile" : [
            "http://hl7.eu/fhir/ig/pcsp/StructureDefinition/Condition-primaryCancer-eu-pcsp"
            ]
        },
        "bodySite" : [
            {
            "coding" : [
                {
                "system" : "http://terminology.hl7.org/CodeSystem/icd-o-3",
                "code" : bodySite_coding_code
                }
            ],
            "text": bodySite_text
            }
        ],
        "valueCodeableConcept": {
		    "text": description
	    },
        "recordedDate": recordedDate,
        "subject" : {
            "reference" : subject_reference
        },
        "stage" : [
            {
            "summary" : {
                "text" : stage_summary_text
            }
            }
        ],
    }

    #### AUTOMATIC CLEANING ####
    dictCond = remove_empty_from_dict(dictCond)
    
    #### MANUAL CLEANING ####
    # # if dictCond['extension'][0]['valueDateTime'] == "":
    # #     del(dictCond['extension'])

    # if dictCond['bodySite'][0]['coding'][0]['code'] == "":
    #     del(dictCond['bodySite'])
    # elif dictCond['bodySite'][0]['text'] == "":
    #     del(dictCond['bodySite'][0]['text'])
    # if dictCond['recordedDate'] == "":
    #     del(dictCond['recordedDate'])  
    # if dictCond['valueCodeableConcept']['text'] == "":
    #     del(dictCond['valueCodeableConcept'])
    # if dictCond['subject']['reference'] == "":
    #     del(dictCond['subject'])
    # if dictCond['stage'][0]['summary']['text'] == "":
    #     del(dictCond['stage'])

    return dictCond