# -*- coding: utf-8 -*-
"""MedXpert FHIR terminology — schema validation (FIXED, repo-reproducible).

Drop-in replacement for validate_all_schema.py. Fixes the audit findings:
  * no hardcoded absolute Windows paths (SCHEMA/DIR/REPORT are argparse/env,
    defaulting to repo-relative + auto-download of the official R5 schema);
  * walks all resource JSON under the repo (CodeSystem/ValueSet/ConceptMap/
    ImplementationGuide), not a single flat folder;
  * prints the real per-resource error count so "11/11" is reproducible in CI.

Usage (local):
    python medxpert_validate_fixed.py                 # validates this repo, auto schema
    python medxpert_validate_fixed.py --schema /path/fhir.schema.json
    python medxpert_validate_fixed.py --dir . --out schema_report.txt

CI:
    - uses: actions/checkout@...
    - run: python medxpert_validate_fixed.py           # fails the build on any error
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.request

from jsonschema import Draft6Validator

# Official FHIR R5 JSON Schema (draft-06). Vendored or downloaded on first run.
R5_SCHEMA_URL = "https://hl7.org/fhir/R5/fhir.schema.json"
RESOURCE_DIRS = ("CodeSystem", "ValueSet", "ConceptMap", "ImplementationGuide")


def load_schema(path: str) -> dict:
    if not os.path.exists(path):
        print("schema not found locally; downloading R5 schema from %s" % R5_SCHEMA_URL)
        req = urllib.request.Request(R5_SCHEMA_URL, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=120) as r:
            data = r.read()
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        with open(path, "wb") as f:
            f.write(data)
        print("downloaded schema: %d bytes" % len(data))
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def main() -> int:
    here = os.path.dirname(os.path.abspath(__file__))
    ap = argparse.ArgumentParser()
    ap.add_argument("--schema", default=os.path.join(here, "fhir.schema.json"),
                    help="path to fhir.schema.json (downloaded if missing)")
    ap.add_argument("--dir", default=here, help="repo root to scan for resource JSON")
    ap.add_argument("--out", default=os.path.join(here, "schema_report.txt"))
    args = ap.parse_args()

    schema = load_schema(args.schema)
    defs = schema.get("definitions", {})

    total = 0
    lines = []
    n = 0
    for root, dirs, files in os.walk(args.dir):
        if ".git" in root:
            continue
        for fn in sorted(files):
            if not fn.endswith(".json"):
                continue
            p = os.path.join(root, fn)
            try:
                res = json.load(open(p, encoding="utf-8"))
            except Exception as e:
                lines.append("%s PARSE_ERROR %s" % (p, e))
                total += 1
                continue
            rt = res.get("resourceType")
            if not rt or rt not in defs:
                continue  # not a top-level FHIR resource we validate here
            n += 1
            sub = {"$ref": "#/definitions/" + rt, "definitions": defs}
            try:
                errs = list(Draft6Validator(sub).iter_errors(res))
            except Exception as e:
                lines.append("%-12s %-45s REF_ERROR %s" % (rt, res.get("id"), e))
                total += 1
                continue
            total += len(errs)
            lines.append("%-12s %-45s errors=%d" % (rt, res.get("id"), len(errs)))
            for e in errs[:6]:
                lines.append("   - %s: %s" % ("/".join(str(x) for x in e.path), e.message[:200]))
            if len(errs) > 6:
                lines.append("   ... (+%d more)" % (len(errs) - 6))
    lines.append("RESOURCES CHECKED: %d" % n)
    lines.append("TOTAL ERRORS: %d" % total)
    lines.append("RESULT: %s" % ("SCHEMA VALIDATION PASS" if total == 0 else "HAS ERRORS"))
    with open(args.out, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print("\n".join(lines))
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())
