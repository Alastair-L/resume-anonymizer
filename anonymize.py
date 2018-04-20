#!/usr/bin/env python3

import sys
import json

def load_rules(rule_file):
    with open(rule_file) as data_file:
        try:
            data = json.load(data_file)
            return data
        except json.JSONDecodeError:
            return None

def anonymized_file(resume_file):
    return 'anonymized_' + resume_file

def apply_rules(rules, resume_file):
    try:
        identifiable_resume = open(resume_file, 'r')
        anonymized_resume = open(anonymized_file(resume_file), 'w+')

        for line in identifiable_resume:
            anonymized_line = line
            for rule in rules:
                for identifier, anonymizer in rule.items():
                    anonymized_line = anonymized_line.replace(identifier, anonymizer)
            anonymized_resume.write(anonymized_line)

    except OSError:
        return False

    finally:
        identifiable_resume.close()
        anonymized_resume.close()

    return True

def verify_args(args):
    for arg in args:
        try:
            f = open(arg, 'r')
            f.close()
        except OSError:
            return False

    return True

def main():
    if len(sys.argv) < 2:
        print("usage: " + sys.argv[0] + " file1.tex file2.tex ...")

    filenames = sys.argv[1:]
    if verify_args(filenames) is not True:
        print("one of the arguments is not a valid file")

    rules = load_rules("rules.json")
    if rules is not None:
        for filename in filenames:
            status = apply_rules(rules, filename)
            if status is True:
                print("rules applied; result written to " + anonymized_file(filename))
            else:
                print("some problem occurred while trying to produce " + anonymized_file(filename))
    else:
        print("I could not parse the rules data; is it valid JSON?")

if __name__ == '__main__' : main()
