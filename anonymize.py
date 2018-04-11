import json

def load_resume(x):
    return False

def load_rules(rule_file):
    with open(rule_file) as data_file:
        try:
            data = json.load(data_file)
            return data
        except json.JSONDecodeError:
            return None

def apply_rules(rules, resume_file):
    identifiable_resume = open(resume_file, 'r')
    anonymized_resume = open('anonymized_' + resume_file, 'w+')

    for line in identifiable_resume:
        anonymized_line = line;
        for rule in rules:
            for identifier, anonymizer in rule.items():
                anonymized_line = anonymized_line.replace(identifier, anonymizer)
        anonymized_resume.write(anonymized_line)

    identifiable_resume.close()
    anonymized_resume.close()

    return True

def main():
    rules = load_rules("rules.json")
    apply_rules(rules, "resume.tex")

main()
