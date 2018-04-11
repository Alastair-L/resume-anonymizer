import anonymize

def test_answer():
    assert anonymize.func(3) == 5

def test_load_resume():
    assert anonymize.load_resume("resume.tex") == True

def test_load_rules():
    assert anonymize.load_rules("rules.json") == True

def test_apply_rules():
    assert anonymize.apply_rules() == True

def test_write_resume():
    assert anonymize.write_resume("resume_anonymized.tex") == True

