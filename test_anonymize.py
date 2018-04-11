#!/usr/bin/env python3

import anonymize

def test_load_rules():
    assert isinstance(anonymize.load_rules("rules.json"), list)

def test_apply_rules():
    rules = anonymize.load_rules("rules.json")
    assert anonymize.apply_rules(rules, "resume.tex") == True
