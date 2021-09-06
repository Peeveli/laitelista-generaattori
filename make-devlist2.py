import pandas as pd
import numpy as np
import sys

def exportcsv():
    path1 = f"{sys.argv[1]}"
    path2 = f"{sys.argv[2]}"
    path3 = f"{sys.argv[3]}"
    columns =  ['Sticker Number','Laitemalli','Processor Name','SERIAL NUMBER'] #Pick specific columns
    columns2 =  ['sticker','school_id','organisation'] #Pick specific columns

    #READ DATA TO DATAFRAMES
    df = pd.read_csv(path1, sep=',', dtype='str') #Dataframe of maatti data form comparing
    puavo = pd.read_csv(path2, sep=',', usecols=columns2, dtype='str') #Dataframe of puavo data
    piip = pd.read_csv(path3, header=None, dtype='str') #Dataframe of piip data
    piip.columns = ['sticker'] #Add header

    #OMIT POSSIBLE ZEROS FROM PIIP DATA
    for i in piip['sticker']:
        if i[:2] == '00':
            piip['sticker'] = piip['sticker'].replace([i],i[2:])

    lista = map(str, piip['sticker'].tolist()) #Create a string type list of piip data

    #FIX THE MAATTI DATA HEADERS
    new_header = df.iloc[1]
    df = df[1:]
    df.columns = new_header #Actual headers in place
    df2 = df[columns].copy()

    #CHECK UNIQUES
    df3 = piip['sticker'][~piip['sticker'].isin(df2['Sticker Number'])].drop_duplicates().reset_index() #Check if uniques exists
    df3 = df3.drop(columns='index')
    df3.rename(columns={'sticker':'Sticker Number'}, inplace = True) #Rename header same as df2 for concat

    #COMPARE PIIP AND MAATTI DATA
    df2 = df2.loc[df2['Sticker Number'].isin(lista)]
    #FIX HEADER AND ADD UNIQUES IF THEY EXIST
    df2.rename(columns = {'Laitemalli':'Device Model'}, inplace = True)
    if (len(df3) < len(piip)):
        df2 = pd.concat([df2, df3])

    #Not 'sticker' even when it says so. When reading puavodata to dataframe, dataframe shifts headers of the puavo data by one
    puavo2 = puavo.loc[puavo['sticker'].isin(df2['SERIAL NUMBER'])].rename(columns={'sticker':'SERIAL NUMBER'})
    puavo2 = puavo2[puavo2['SERIAL NUMBER'].notna()]
    df2 = df2.merge(puavo2, on='SERIAL NUMBER', how='left')

    df2 = df2.append({'Sticker Number':''},ignore_index = True)
    df2 = df2.append({'Sticker Number':f"Devices: {len(df2.index)-2}"}, ignore_index = True)
    df2.rename(columns={'SERIAL NUMBER':'Serial','school_id':'Name','organisation':'School'}, inplace = True)
    df2 = df2.sort_values(by=['Name'], ignore_index = True) #Sort ascending by name
    df2.to_csv("dev-list.csv", index = False)

def main():

    if (len(sys.argv)) <4:
        print("NOT ENOUGH ARGUMENTS!\nUsage: python3 make-devlist2.py [maatti.csv] [puavolaitelista.csv] [piipattu(.txt/.csv)]")
    else:
        exportcsv()

if __name__ == "__main__":
    main()
