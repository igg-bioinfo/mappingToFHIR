import csv
import json
import os
import pandas as pd
import cx_Oracle
import collections
import timeit
from datetime import datetime
from patient import func_dictPat
from condition import func_dictCond
from sendPostman import postman
from colorama import Fore, Back, Style

#COLOR SETTINGS
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

#RESOURCES FLAGS
pat_flag = 1
cond_flag = 1

print(f"{bcolors.WARNING}{bcolors.BOLD}Resources to be created:{bcolors.ENDC}")
if pat_flag == 1:
    print(f"{bcolors.OKGREEN}- PATIENT{bcolors.ENDC}")
if cond_flag == 1:
    print(f"{bcolors.OKGREEN}- CONDITION{bcolors.ENDC}")
if pat_flag == 0 and cond_flag == 0:
    print(f"{bcolors.FAIL}no resource to create -> Set the resource flag to 1 for the resources to be created{bcolors.ENDC}")

#DATA EXTRACTION METHOD (1: Oracle server | 2: csv file)
extraction_mode = ["Oracle server","csv file"]
extraction = 2
print(f"{bcolors.OKCYAN}Extraction from: "+extraction_mode[extraction-1]+f"{bcolors.ENDC}")
print("---------------")
print()

if extraction == 1:
    dsn_tns = cx_Oracle.makedsn('XXXXXXXXXX', 'XXXXXXXXXX', service_name='XXXXXXXXXX') # if needed, place an 'r' before any parameter in order to address special characters such as '\'.
    conn = cx_Oracle.connect(user=r'XXXXXXXXXX', password='XXXXXXXXXX', dsn=dsn_tns) # if needed, place an 'r' before any parameter in order to address special characters such as '\'. For example, if your user name contains '\', you'll need to place 'r' before the user name: user=r'User Name'
    c = conn.cursor()

elif extraction == 2:
    path_in_Pat = '/home/.../V_ANAGRAFE_PAZIENTI_REAL.csv' 
    path_in_Cond = '/home/.../V_PAZIENTI_DIAGNOSI.csv' 

##PATIENT
if pat_flag == 1:
    print(f"{bcolors.WARNING}building Patients...{bcolors.ENDC}\n")
    start = timeit.default_timer() 
    if extraction == 1:
        c.execute("SELECT * FROM V_ANAGRAFE_PAZIENTI_REAL")
        names = [col[0] for col in c.description]
        c.rowfactory = collections.namedtuple("V_ANAGRAFE_PAZIENTI_REAL",names)
        df = pd.DataFrame(c)

    elif extraction == 2:
        df = pd.DataFrame()
        with open(path_in_Pat) as csvFile:
            csvReader = csv.DictReader(csvFile)
            df = pd.DataFrame(csvReader)

    pats = []

    itopen = 0
    for r in range(0,len(df.index)):
        row = df.iloc[r]
        
        primaryKey = [row.A01_ID_PERSONA]
        
        #select all records of this patient in this date
        if primaryKey not in pats:
            pats.append(primaryKey)
            path_out_Pat = 'Patients/P_'+str(primaryKey[0])+'.json'

            if extraction == 1:
                c2 = conn.cursor()
                c2.execute('SELECT * FROM V_ANAGRAFE_PAZIENTI_REAL WHERE A01_ID_PERSONA = :key1', key1 = primaryKey[0])

                names2 = [col2[0] for col2 in c2.description]
                c2.rowfactory = collections.namedtuple("V_ANAGRAFE_PAZIENTI_REAL",names2)

                df2 = pd.DataFrame(c2)

            elif extraction == 2:
                df2 = pd.DataFrame()
                with open(path_in_Pat) as csvFile2:
                    csvReader2 = csv.DictReader(csvFile2)
                    df2 = pd.DataFrame(csvReader2)
                    df2 = df2[df2.A01_ID_PERSONA==primaryKey[0]]

            dictPat = func_dictPat(df2)

            postman(dictCond)
            itopen += 1
            with open(path_out_Pat, 'w') as json_fileP:
                json.dump(dictPat, json_fileP, indent=2)

    print("Printed jsons: ",itopen)
    stop = timeit.default_timer()
    print('TIME SPENT: ', stop - start)            

#CONDITION
if cond_flag ==1:
    print(f"{bcolors.WARNING}building Conditions...{bcolors.ENDC}\n")
    start = timeit.default_timer() 
    if extraction == 1:
        c.execute('SELECT * FROM V_PAZIENTI_DIAGNOSI')
        names = [col[0] for col in c.description]
        c.rowfactory = collections.namedtuple("V_PAZIENTI_DIAGNOSI",names)
        df = pd.DataFrame(c)

    elif extraction == 2:
        df = pd.DataFrame()
        with open(path_in_Cond) as csvFile:
            csvReader = csv.DictReader(csvFile)
            df = pd.DataFrame(csvReader)

    conds = []

    itopen = 0
    for r in range(0,len(df.index)):
        row = df.iloc[r]
        
        primaryKey = [row.ID_PAZIENTE,row.DT_REGISTRAZIONE]

        #select all records of this patient in this date
        if primaryKey not in conds:
            conds.append(primaryKey)

            if extraction == 1:
                path_out_Cond = 'Conditions/C_'+str(primaryKey[0])+'_'+str(primaryKey[1].strftime("%Y-%m-%d"))+'.json'
                c2 = conn.cursor()
                c2.execute('SELECT * FROM V_PAZIENTI_DIAGNOSI WHERE ID_PAZIENTE = :key1 AND DT_REGISTRAZIONE = :key2', key1 = primaryKey[0], key2 = primaryKey[1])

                names2 = [col2[0] for col2 in c2.description]
                c2.rowfactory = collections.namedtuple("V_PAZIENTI_DIAGNOSI",names2)

                df2 = pd.DataFrame(c2)
            
            elif extraction == 2:
                path_out_Cond = 'Conditions/C_'+str(primaryKey[0])+'_'+str(primaryKey[1])[:10]+'.json'
                df2 = pd.DataFrame()
                with open(path_in_Cond) as csvFile2:
                    csvReader2 = csv.DictReader(csvFile2)
                    df2 = pd.DataFrame(csvReader2)
                    df2 = df2[df2.ID_PAZIENTE==primaryKey[0]][df2.DT_REGISTRAZIONE==primaryKey[1]]

            dictCond = func_dictCond(df2)

            postman(dictCond)
            itopen += 1
            with open(path_out_Cond, 'w') as json_fileC:
                json.dump(dictCond, json_fileC, indent=2)

    print("Printed jsons: ",itopen)
    stop = timeit.default_timer()
    print('TIME SPENT: ', stop - start) 

    if extraction == 1:
        conn.close()

#END
