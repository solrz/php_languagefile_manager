# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 17:26:37 2018

@author: kbpso
"""
import csv
import os
def importPHPtoCSV(arrayfile='Import/language.php',langfile_list=['en_US','zh_TW'],\
                   outputfile="lang_dict.csv"):
    def importPHPVarName(phpfile='importing.php'):
        with open(phpfile, 'r') as source:
            text = source.read()
            varnames = dict()
            for phpfile_line in text.split('\n'):
                if phpfile_line.find('$') == -1:
                    continue
                varnames[phpfile_line[phpfile_line.find("'")+1:-3]] = []
        return varnames
    
    def importPHPLang(phpfile,varlist):
        with open(phpfile, 'r',encoding = 'utf-8') as source:
            text = source.read()
            langnames = dict()
            for phpfile_line in text.split('\n'):
                if phpfile_line.find(',') == -1:
                    continue
                analysising_line = phpfile_line.replace('  ','').replace(',','').\
                replace("'",'').split(' => ')
                # print(analysising_line)
                langnames[analysising_line[0]] = analysising_line[1]
            
            for key, value in langnames.items():
                if not varlist.get(key):
                    varlist[key] = []
                try:
                    varlist[key].append(value)
                except:
                    print("[Warning] {} is not found in {}".format(key, phpfile))
        return varlist
        
    def createCSVFIle(csvfile,varlist,titles=('en_US','zh_TW')):
        header = ['varname']
        header.extend(titles)
        csvfilewriter = open(csvfile, 'w')
        csvwriter = csv.writer(csvfilewriter,delimiter='|')
        csvwriter.writerow(header)
        for varname, lang in varlist.items():
            writing_buffer = []
            writing_buffer.append(varname)
            writing_buffer.extend(lang)
            csvwriter.writerow(writing_buffer)
        return varlist
    # main
    varname = importPHPVarName(arrayfile)
    for lang_reading in langfile_list:
        varname = importPHPLang("Import/"+lang_reading, varname)
    createCSVFIle(outputfile,varname,langfile_list)

def exportCSVtoPHP(csvfile='lang_dict.csv'):
    def readFromCSV(csvfile):
        csvfileread = open(csvfile, 'r')
        vardicts = csv.DictReader(csvfileread,delimiter='|')
        return vardicts
    
    def analyzeLangList(vardicts):
        lang_list = list()
        for vardict in vardicts:
            for key, value in vardict.items():
                if key == "varname":
                    continue
                lang_list.append(key)
            break
        return lang_list
    
    def exportLanguagePHP(vardicts,phpfile='Export/language.php'):
        exporting = open(phpfile, 'w')
        exporting.write("<?php\nheader('content-type:text/html;charset=utf-8');\n")
        for var in vardicts:
            exporting.write("$lang_{} = $lang['{}'];\n".format(var['varname'],var['varname']))
        exporting.write("?>")
    
    def exportVarToLangPHP(vardicts,language='def'):
        phpfile= 'Export/'+language
        exporting = open(phpfile, 'w')
        exporting.write("<?php\nheader('content-type:text/html;charset=utf-8');\n$lang = array\n(\n")
        for var in vardicts:
            # print("    '{}' => '{}',\n".format(var['varname'],var[language]))
            exporting.write("    '{}' => '{}',\n".format(var['varname'],var[language]))
        exporting.write(");\n?>")
    
    vardicts = readFromCSV(csvfile)
    try:
        os.mkdir("./Export")
    except:
        pass
    langfile_list=analyzeLangList(vardicts)
    exportLanguagePHP(vardicts)
    for lang_reading in langfile_list:
        vardicts = readFromCSV(csvfile)
        exportVarToLangPHP(vardicts,lang_reading)

def getAllLangPHPFile(folder="./"):
    files = os.listdir(folder)
    available = list()
    for file in files:
        if file.find("_") != -1 and file.find(".php") != -1:
            available.append(file)
    return available

while True:
    print("1) import from existing PHP file")
    print("2) export CSV file to PHP file")
    print("3) Exit")
    option = input(">> Please enter the option: ")
    if option == "1":
        try:
            os.mkdir("./Import")
        except:
            pass
        print("Move all PHP file into folder \"Import\"")
        os.system("pause")
        importPHPtoCSV(langfile_list=getAllLangPHPFile(folder="./Import"))
        print("Import to file: lang_dict.csv\n")
    if option == "2":
        exportCSVtoPHP()
        print("Export to folder: \\Export\n")
    if option == "3":
        break
    
