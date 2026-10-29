# -*- coding: utf-8 -*-
"""
MedXpert termbase -> FHIR R5 terminology resources builder.

Reads:
  - termbase.tsv       (en, zh, note, kind) 164 rows
  - mistranslations.tsv(bad, good, reason, severity) 36 rows
Writes 9 FHIR resources under ./fhir-contribution/
"""
import csv, json, os, collections

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "fhir-contribution")
os.makedirs(OUT, exist_ok=True)

NS = "https://stevenzhao07.github.io/medxpert-fhir"
VERSION = "1.0.0-draft"

def read_tsv(name):
    with open(os.path.join(BASE, name), encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f, delimiter="\t"))
    return [r for r in rows if any((r.get(k) or "").strip() for k in r)]

STD_USE = "http://terminology.hl7.org/CodeSystem/designation-usage"
MXP_USE = f"{NS}/CodeSystem/medxpert-designation-use"

def use_code(system, code):
    """Designation.use as Coding (official FHIR R5 schema requires Coding)."""
    return {"system": system, "code": code}

def dump(res):
    p = os.path.join(OUT, f"{res['resourceType']}-{res['id']}.json")
    with open(p, "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=2)
    print(f"  {res['resourceType']:12s} {res['id']:45s} concepts={res.get('count', res.get('total', '-'))}")

terms = read_tsv("termbase.tsv")
mis   = read_tsv("mistranslations.tsv")
print(f"termbase rows: {len(terms)} | mistranslations rows: {len(mis)}")

kinds = collections.Counter(r["kind"] for r in terms)
print("kinds:", dict(kinds))

# ---------- 1. CodeSystem: EN (code = EN term) ----------
en_concepts = []
for r in terms:
    en, zh, note, kind = r["en"].strip(), r["zh"].strip(), (r.get("note") or "").strip(), r["kind"].strip()
    designation = [
        {"language": "zh", "use": use_code(STD_USE, "display"), "value": zh},
        {"language": "en", "use": use_code(STD_USE, "display"), "value": en},
    ]
    if note:
        designation.append({"language": "zh", "use": use_code(MXP_USE, "note"), "value": note})
    c = {"code": en, "display": zh, "designation": designation,
         "property": [{"code": "kind", "valueCode": kind}]}
    en_concepts.append(c)

cs_en = {
    "resourceType": "CodeSystem",
    "id": "medxpert-meddev-en",
    "url": f"{NS}/CodeSystem/medxpert-meddev-en",
    "version": VERSION,
    "name": "MedXpertMedicalDeviceTerminologyEN",
    "title": "MedXpert 医械法规术语库（英文术语）",
    "status": "draft",
    "experimental": True,
    "publisher": "MedXpert (stevenzhao07)",
    "description": "Medical device regulatory bilingual terminology (EN codes). Codes are English terms; zh display/designation carry the canonical Chinese rendering. Kinds: keep-as-is / term / warning-level / modal-verb.",
    "copyright": "MIT License; source https://github.com/stevenzhao07/medxpert-skills",
    "content": "complete",
    "count": len(en_concepts),
    "property": [{"code": "kind", "type": "code", "description": "Term category: keep-as-is | term | warning-level | modal-verb"}],
    "concept": en_concepts,
}
dump(cs_en)

# ---------- 2. CodeSystem: ZH (code = canonical zh rendering, deduped) ----------
zh_first = {}
for r in terms:
    zh = r["zh"].strip()
    if zh not in zh_first:
        zh_first[zh] = {"en": [r["en"].strip()], "kind": r["kind"].strip()}
    else:
        zh_first[zh]["en"].append(r["en"].strip())
zh_concepts = []
for zh, info in zh_first.items():
    designation = [{"language": "zh", "use": use_code(STD_USE, "display"), "value": zh}]
    for en in info["en"]:
        designation.append({"language": "en", "use": use_code(MXP_USE, "designation"), "value": en})
    zh_concepts.append({"code": zh, "display": zh, "designation": designation})
cs_zh = {
    "resourceType": "CodeSystem",
    "id": "medxpert-meddev-zh",
    "url": f"{NS}/CodeSystem/medxpert-meddev-zh",
    "version": VERSION,
    "name": "MedXpertMedicalDeviceTerminologyZH",
    "title": "MedXpert 医械法规术语库（中文规范译法）",
    "status": "draft",
    "experimental": True,
    "publisher": "MedXpert (stevenzhao07)",
    "description": "Canonical Chinese renderings of medical device regulatory terms (deduplicated; 1:1 and 1:N EN->ZH relations are expressed in ConceptMap medxpert-en-zh).",
    "copyright": "MIT License; source https://github.com/stevenzhao07/medxpert-skills",
    "content": "complete",
    "count": len(zh_concepts),
    "concept": zh_concepts,
}
dump(cs_zh)
print(f"  ZH dedup: {len(terms)} EN -> {len(zh_first)} unique ZH; dup zh: {[z for z,i in zh_first.items() if len(i['en'])>1]}")

# ---------- 3. CodeSystem: mistranslations (code = bad rendering) ----------
mis_concepts = []
for r in mis:
    bad, good, reason, sev = r["bad"].strip(), r["good"].strip(), (r.get("reason") or "").strip(), r["severity"].strip()
    designation = [{"language": "zh", "use": use_code(STD_USE, "display"), "value": bad},
                   {"language": "zh", "use": use_code(MXP_USE, "good-rendering"), "value": good}]
    if reason:
        designation.append({"language": "zh", "use": use_code(MXP_USE, "reason"), "value": reason})
    mis_concepts.append({"code": bad, "display": bad, "designation": designation,
                         "property": [{"code": "severity", "valueCode": sev}]})
cs_mis = {
    "resourceType": "CodeSystem",
    "id": "medxpert-meddev-mistranslations",
    "url": f"{NS}/CodeSystem/medxpert-meddev-mistranslations",
    "version": VERSION,
    "name": "MedXpertMedicalDeviceMistranslations",
    "title": "MedXpert 医械常见误译对照",
    "status": "draft",
    "experimental": True,
    "publisher": "MedXpert (stevenzhao07)",
    "description": "Common mistranslations in medical device regulatory Chinese documents. Codes are the WRONG renderings; designation use 'good-rendering' gives the canonical one. Severity: error | info.",
    "copyright": "MIT License; source https://github.com/stevenzhao07/medxpert-skills",
    "content": "complete",
    "count": len(mis_concepts),
    "property": [{"code": "severity", "type": "code", "description": "error = must fix; info = style/consistency"}],
    "concept": mis_concepts,
}
dump(cs_mis)

# ---------- 4. ValueSets by kind ----------
kind_labels = {
    "keep-as-is": "vs-meddev-keep-as-is",
    "term": "vs-meddev-core-terms",
    "warning-level": "vs-meddev-warning-level",
    "modal-verb": "vs-meddev-modal-verbs",
}
kind_titles = {
    "keep-as-is": "医械标准/机构名不译清单",
    "term": "医械法规核心术语",
    "warning-level": "警示强度用语",
    "modal-verb": "规范情态动词",
}
by_kind = collections.defaultdict(list)
for r in terms:
    by_kind[r["kind"].strip()].append({"code": r["en"].strip(), "display": r["zh"].strip()})

for kind, vsid in kind_labels.items():
    vs = {
        "resourceType": "ValueSet",
        "id": vsid,
        "url": f"{NS}/ValueSet/{vsid}",
        "version": VERSION,
        "name": "MedXpert" + "".join(w.capitalize() for w in kind.replace("-", " ").split()),
        "title": kind_titles[kind],
        "status": "draft",
        "experimental": True,
        "publisher": "MedXpert (stevenzhao07)",
        "description": f"MedXpert terminology subset: kind = {kind} ({len(by_kind[kind])} concepts).",
        "compose": {"include": [{"system": cs_en["url"],
                                 "concept": by_kind[kind]}]},
    }
    dump(vs)

# ---------- 5. ConceptMap: EN -> ZH ----------
cm_en_zh = {
    "resourceType": "ConceptMap",
    "id": "medxpert-en-zh",
    "url": f"{NS}/ConceptMap/medxpert-en-zh",
    "version": VERSION,
    "name": "MedXpertENtoZH",
    "title": "MedXpert 医械术语英中映射",
    "status": "draft",
    "experimental": True,
    "publisher": "MedXpert (stevenzhao07)",
    "description": "Maps 164 English medical-device regulatory terms to their canonical Chinese renderings.",
    "sourceScopeCanonical": cs_en["url"],
    "targetScopeCanonical": cs_zh["url"],
    "group": [{
        "source": cs_en["url"],
        "target": cs_zh["url"],
        "element": [{"code": r["en"].strip(),
                     "target": [{"code": r["zh"].strip(), "relationship": "equivalent"}]}
                    for r in terms],
    }],
}
dump(cm_en_zh)

# ---------- 6. ConceptMap: mistranslation (bad) -> canonical zh (good) ----------
cm_mis = {
    "resourceType": "ConceptMap",
    "id": "medxpert-zh-mistranslation",
    "url": f"{NS}/ConceptMap/medxpert-zh-mistranslation",
    "version": VERSION,
    "name": "MedXpertMistranslationFix",
    "title": "MedXpert 医械误译纠正映射",
    "status": "draft",
    "experimental": True,
    "publisher": "MedXpert (stevenzhao07)",
    "description": "Maps 36 common WRONG Chinese renderings (source) to canonical renderings (target) with severity error|info.",
    "sourceScopeCanonical": cs_mis["url"],
    "targetScopeCanonical": cs_zh["url"],
    "group": [{
        "source": cs_mis["url"],
        "target": cs_zh["url"],
        "element": [{"code": r["bad"].strip(),
                     "target": [{"code": r["good"].strip(), "relationship": "equivalent"}]}
                    for r in mis],
    }],
}
dump(cm_mis)

# ---------- 7. CodeSystem: custom designation-use codes ----------
cs_du = {
    "resourceType": "CodeSystem",
    "id": "medxpert-designation-use",
    "url": MXP_USE,
    "version": VERSION,
    "name": "MedXpertDesignationUse",
    "title": "MedXpert 自定义 designation use 编码",
    "status": "draft",
    "experimental": True,
    "publisher": "MedXpert (stevenzhao07)",
    "description": "Custom designation.use codes used by MedXpert resources: note / good-rendering / reason / designation.",
    "content": "complete",
    "count": 4,
    "concept": [
        {"code": "note", "display": "注释"},
        {"code": "good-rendering", "display": "规范译法"},
        {"code": "reason", "display": "误译原因"},
        {"code": "designation", "display": "来源英文术语"},
    ],
}
dump(cs_du)

print(f"\nDone. {len(terms)} terms, {len(mis)} mistranslation rules -> {OUT}")
