# -*- coding: utf-8 -*-
"""Validate all 10 resources against official FHIR R5 schema, write report to file."""
import json, glob
from jsonschema import Draft6Validator, validators

SCHEMA = r'C:\Users\SZYL\Doubao\chats\2026-10-28\new-chat-3\fhir.schema.json'
DIR = r'C:\Users\SZYL\Doubao\chats\2026-10-28\new-chat-3\fhir-contribution'
REPORT = r'C:\Users\SZYL\Doubao\chats\2026-10-28\new-chat-3\schema_report.txt'

with open(SCHEMA, encoding='utf-8') as f:
    schema = json.load(f)

lines = []
total = 0
for p in sorted(glob.glob(DIR + r'\*.json')):
    with open(p, encoding='utf-8') as f:
        res = json.load(f)
    rt = res.get('resourceType')
    v = Draft6Validator({'$ref': '#/definitions/' + rt}, resolver=validators._RefResolver('', schema))
    errs = list(v.iter_errors(res))
    total += len(errs)
    lines.append('%-10s %-40s errors=%d' % (rt, res.get('id'), len(errs)))
    for e in errs[:6]:
        lines.append('   - %s: %s' % ('/'.join(str(x) for x in e.path), e.message[:220]))
    if len(errs) > 6:
        lines.append('   ... (+%d more)' % (len(errs) - 6))
lines.append('TOTAL ERRORS: %d' % total)
lines.append('RESULT: %s' % ('SCHEMA VALIDATION PASS' if total == 0 else 'HAS ERRORS'))
with open(REPORT, 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines) + '\n')
print('report written:', REPORT)
