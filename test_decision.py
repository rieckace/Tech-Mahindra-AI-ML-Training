"""Assert-based regression tests. Run: python test_decision.py"""
import csv
from tempfile import TemporaryDirectory
from pathlib import Path
from decision import *

def run_tests():
    expected = ['No AI (rules/code)', 'Classical ML', 'Generative AI', 'Deep Learning', 'No AI (rules/code)', 'Classical ML', 'Generative AI', 'No AI (rules/code)', 'Analytics/BI', 'Classical ML']
    assert len(REQUIREMENTS) == 10
    for r, category in zip(REQUIREMENTS, expected):
        d = classify(r)
        assert d.category == category, (r.name, d.category)
        assert all((d.reasons, d.risks, d.first_next_step))
        stages = lifecycle(r)
        if category in AI_CATEGORIES:
            assert [s['stage'] for s in stages] == list(STAGES)
            assert all(s['task'] and s['role'] for s in stages)
        else: assert stages == []
    assert classify(REQUIREMENTS[-1]).readiness == 'Blocked: data missing'
    assert classify(Requirement('Unclear')).readiness == 'Needs clarification'
    assert classify(Requirement('Generate reply', generation=True, data_available=False)).category == 'Generative AI'
    assert len(lifecycle(Requirement('Predict faults', learning=True))) == 5
    for kwargs in [{'name':''}, {'name':'bad','learning':'yes'}, {'name':'bad','fixed_rules':True,'learning':True}, {'name':'bad','complex_perception':True}, {'name':'bad','historical_summary':True,'generation':True}]:
        try: Requirement(**kwargs)
        except ValueError: pass
        else: raise AssertionError(f'Invalid requirement accepted: {kwargs}')
    with TemporaryDirectory() as folder:
        export_reports(REQUIREMENTS, folder)
        with (Path(folder)/'decision_report.csv').open(encoding='utf-8-sig') as f: assert len(list(csv.DictReader(f))) == 10
        with (Path(folder)/'lifecycle_map.csv').open(encoding='utf-8-sig') as f: assert len(list(csv.DictReader(f))) == 30
    print('PASS: all 10 classifications, lifecycle stages, readiness, validation and CSV exports.')

if __name__ == '__main__': run_tests()
