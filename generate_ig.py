# -*- coding: utf-8 -*-
"""Generate an ImplementationGuide shell that packages all MedXpert FHIR resources."""
import json, glob, os

DIR = r'C:\Users\SZYL\Doubao\chats\2026-10-28\new-chat-3\fhir-contribution'
NS = "https://stevenzhao07.github.io/medxpert-fhir"
VERSION = "1.0.0-draft"

resources = []
for p in sorted(glob.glob(DIR + r'\*.json')):
    if 'CONTRIBUTION' in p or 'ImplementationGuide' in p:
        continue
    with open(p, encoding='utf-8') as f:
        res = json.load(f)
    ref = "%s/%s" % (res["resourceType"], res["id"])
    resources.append({
        "reference": {"reference": ref},
        "name": res.get("title", res["id"]),
        "description": res.get("description", "")[:200],
        "isExample": True,
    })

manifest_resources = [{"reference": {"reference": r["reference"]["reference"]}} for r in resources]

ig = {
    "resourceType": "ImplementationGuide",
    "id": "medxpert-meddev-terminology",
    "url": NS + "/ImplementationGuide/medxpert-meddev-terminology",
    "version": VERSION,
    "name": "MedXpertMedicalDeviceTerminologyIG",
    "title": "MedXpert 医械法规术语 IG（draft）",
    "status": "draft",
    "experimental": True,
    "publisher": "MedXpert (stevenzhao07)",
    "description": "MedXpert medical-device regulatory bilingual terminology: 164 EN terms, 159 canonical ZH renderings, 36 mistranslation rules, exposed as FHIR R5 CodeSystems, ValueSets and ConceptMaps. Draft package for the FHIR IG Registry / HL7 China FHIR IG contribution.",
    "copyright": "MIT License; source https://github.com/stevenzhao07/medxpert-skills",
    "fhirVersion": ["5.0.0"],
    "definition": {"resource": resources},
    "manifest": {
        "rendering": NS + "/",
        "resource": manifest_resources,
    },
}

with open(os.path.join(DIR, "ImplementationGuide-medxpert-meddev-terminology.json"), "w", encoding="utf-8") as f:
    json.dump(ig, f, ensure_ascii=False, indent=2)
print("IG written with", len(resources), "definition resources")
