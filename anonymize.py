#!/usr/bin/env python3

import sys
import os
import json
import xlrd 
import argparse

EXCEL_FILE_NAME = 'names_list.xlsx'
PATH_TO_RESUMES = './Input resumes'
PATH_TO_ANONYMIZED_RESUMES = './Anonymized resumes'


def create_rules():
    names = get_names_to_replace()
    rules = {
        'He': 'They',
        'She': 'They',
    }
    for fullname in names:
        for name in fullname.split(' '):
            rules[name] = "$PersonName"
    return rules


def create_anonymized_file(rules, resume_file):
    identifiable_resume = None
    anonymized_resume = None
    try:
        identifiable_resume = open(f"{PATH_TO_RESUMES}/{resume_file}", 'r')
        print(identifiable_resume)
        anonymized_resume = open(f"{PATH_TO_ANONYMIZED_RESUMES}/anonymized2_{resume_file}", 'w+')

        for line in identifiable_resume:
            print(line)
            anonymized_line = line
            for identifier, anonymizer in rules.items():
                anonymized_line = anonymized_line.replace(identifier, anonymizer)
            anonymized_resume.write(anonymized_line)

    finally:
        if identifiable_resume is not None: # would be better to check if it had this method
            identifiable_resume.close()
        if anonymized_resume is not None:
            anonymized_resume.close()

    return True

def get_names_to_replace():
    with xlrd.open_workbook(EXCEL_FILE_NAME) as data_file:
        sheet = data_file.sheet_by_index(0)
        names = [sheet.cell_value(index, 0) for index in range(sheet.nrows)]
    if len(names) == 0: print('Names not found, still applying other rules')
    return names
        

def main():
    filenames = os.listdir(PATH_TO_RESUMES)
    rules = create_rules()
    print(rules)

    for filename in filenames:
        status = create_anonymized_file(rules, filename)
        if status is True:
            print("rules applied; result written to " + anonymized_file(filename))
        else:
            print("some problem occurred while trying to produce " + anonymized_file(filename))

if __name__ == '__main__' : main()
