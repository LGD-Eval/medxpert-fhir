# MedXpert FHIR Terminology Package

Medical-device regulatory **bilingual (EN/ZH) terminology** exposed as **FHIR R5** resources — built from the [stevenzhao07/medxpert-skills](https://github.com/stevenzhao07/medxpert-skills) term base.

| | |
|---|---|
| **Namespace** | `https://stevenzhao07.github.io/medxpert-fhir/` |
| **FHIR version** | 5.0.0 |
| **Resources** | CodeSystem ×4, ValueSet ×4, ConceptMap ×2, ImplementationGuide ×1 (11 total) |
| **Schema validation** | FHIR R5 official JSON Schema — **11/11 PASS** (2026-10-28) |
| **Source data** | `termbase.tsv` (164 rows) + `mistranslations.tsv` (36 rows) |
| **License** | MIT |
| **Status** | draft · pre-submission review in progress |

## Resources

| Resource type | id | Description |
|---|---|---|
| CodeSystem | [medxpert-meddev-en](CodeSystem/medxpert-meddev-en.json) | 164 EN medical-device regulatory terms (source concepts) |
| CodeSystem | [medxpert-meddev-zh](CodeSystem/medxpert-meddev-zh.json) | 159 ZH canonical renderings |
| CodeSystem | [medxpert-meddev-mistranslations](CodeSystem/medxpert-meddev-mistranslations.json) | 36 mistranslation correction rules (bad→good, severity) |
| CodeSystem | [medxpert-designation-use](CodeSystem/medxpert-designation-use.json) | designation.use value set codes (keep-as-is / term / warning-level / modal-verb) |
| ValueSet | [vs-meddev-core-terms](ValueSet/vs-meddev-core-terms.json) | core term set (135) |
| ValueSet | [vs-meddev-keep-as-is](ValueSet/vs-meddev-keep-as-is.json) | keep-as-is terms (19) |
| ValueSet | [vs-meddev-warning-level](ValueSet/vs-meddev-warning-level.json) | warning-level terms (5) |
| ValueSet | [vs-meddev-modal-verbs](ValueSet/vs-meddev-modal-verbs.json) | modal verbs (5) |
| ConceptMap | [medxpert-en-zh](ConceptMap/medxpert-en-zh.json) | EN→ZH mapping (164) |
| ConceptMap | [medxpert-zh-mistranslation](ConceptMap/medxpert-zh-mistranslation.json) | ZH→mistranslation correction (36) |
| ImplementationGuide | [medxpert-meddev-terminology](ImplementationGuide/medxpert-meddev-terminology.json) | IG shell packaging all resources |

## Reproduction

```bash
python build_fhir.py          # termbase.tsv + mistranslations.tsv -> resources
python generate_ig.py         # builds the ImplementationGuide shell
python validate_all_schema.py # official R5 JSON Schema validation
```

`fhir.schema.json` (R5 official schema, draft-06) is not stored in this repo; download it from the FHIR build server or run the full validation at [validator.fhir.org](https://validator.fhir.org).

## Contribution

- [CONTRIBUTION.md](CONTRIBUTION.md) — submission note: authorship & originality statement, namespace decision, validation record, recommended channels (FHIR IG Registry `fhir-director@hl7.org`; HL7 China Committee `fhir@hl7.org.cn`).
- Pre-submission review (LGD gates G0–G6) in progress; see the review record in the source project.

## Known limitation

The IG shell ships as JSON only. A full human-readable IG (HTML pages per resource) requires the official HL7 IG publisher (Java-based); this environment has no Java, so the full IG build is deferred until submission tooling is available.
