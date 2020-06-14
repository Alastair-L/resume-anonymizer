#!/usr/bin/env python3

import sys
import os
import json
import xlrd 
import argparse

EXCEL_FILE_NAME = 'names_list.xlsx'
PATH_TO_RESUMES = './Input Resumes'


def create_rules(rule_file):
    try:
        with open(rule_file) as data_file:
            try:
                data = json.load(data_file)
                return data
            except json.JSONDecodeError:
                return None
            except IOError:
                return None
    except FileNotFoundError:
        return None

def anonymized_file(resume_file):
    original_dir = os.path.dirname(resume_file)
    original_base = os.path.basename(resume_file)
    anonymized_base = 'anonymized_' + original_base

    return os.path.join(original_dir, anonymized_base)

def create_anonymized_file(rules, resume_file):
    identifiable_resume = None
    anonymized_resume = None
    try:
        identifiable_resume = open(resume_file, 'r')
        anonymized_resume = open(anonymized_file(resume_file), 'w+')

        for line in identifiable_resume:
            anonymized_line = line
            for rule in rules:
                for identifier, anonymizer in rule.items():
                    anonymized_line = anonymized_line.replace(identifier, anonymizer)
            anonymized_resume.write(anonymized_line)

    except OSError as ose:
        print(ose)
        return False

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
    names = get_names_to_replace()
    print("loaded names:", filenames)

    rules = create_rules()

    for filename in filenames:
        status = create_anonymized_file(rules, filename)
        if status is True:
            print("rules applied; result written to " + anonymized_file(filename))
        else:
            print("some problem occurred while trying to produce " + anonymized_file(filename))

if __name__ == '__main__' : main()
