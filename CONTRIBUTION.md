# MedXpert Medical Device Terminology — FHIR Contribution Package

**Status: READY FOR EXTERNAL REVIEW / SUBMISSION (draft)**
**Version:** 1.0.0-draft · **Date:** 2026-10-28
**Origin:** https://github.com/stevenzhao07/medxpert-skills (MIT License)
**Contact:** stevenzhao07 (GitHub) — external submission mailbox to be confirmed

---

## 1. What this package is

A machine-readable, standards-based export of the MedXpert medical-device
regulatory **bilingual terminology base (164 terms)** and **translation QA rules
(36 mistranslation rules)** as **FHIR R5 terminology resources**, wrapped in an
**ImplementationGuide shell** for registration.

It is the strongest reusable asset MedXpert can contribute to the HL7/FHIR
ecosystem: a **systematic English↔Chinese medical-device regulatory terminology
and mistranslation-correction set**, which currently has no direct equivalent in
the public FHIR terminology space.

## 2. Package contents (10 content resources + 1 ImplementationGuide shell = 11 files)

| # | Resource | id | Size |
|---|----------|-----|------|
| 1 | CodeSystem (EN codes) | `medxpert-meddev-en` | 164 concepts |
| 2 | CodeSystem (ZH canonical codes, deduped) | `medxpert-meddev-zh` | 159 concepts |
| 3 | CodeSystem (common mistranslations) | `medxpert-meddev-mistranslations` | 36 concepts |
| 4 | CodeSystem (custom designation-use) | `medxpert-designation-use` | 4 concepts |
| 5 | ValueSet — standard names kept as-is | `vs-meddev-keep-as-is` | 19 |
| 6 | ValueSet — core regulatory terms | `vs-meddev-core-terms` | 135 |
| 7 | ValueSet — warning-level signal words | `vs-meddev-warning-level` | 5 |
| 8 | ValueSet — modal verbs | `vs-meddev-modal-verbs` | 5 |
| 9 | ConceptMap EN → ZH | `medxpert-en-zh` | 164 maps |
| 10 | ConceptMap mistranslation → canonical ZH | `medxpert-zh-mistranslation` | 36 maps |
| + | ImplementationGuide shell | `medxpert-meddev-terminology` | 10 definition resources |

Scope: ISO 13485 / ISO 14971 / IEC 62304 / IEC 60601 / ISO 10993 families,
EU MDR (EU) 2017/745, US 510(k)/PMA/UDI, NMPA terminology, SaMD/cybersecurity,
labeling, risk management, clinical evaluation, sterilization.

Each CodeSystem concept carries designations (en/zh/note) and a `kind` property
(`keep-as-is | term | warning-level | modal-verb`). Mistranslation concepts carry
`severity` (`error | info`) and a `good-rendering` designation.

## 3. Validation status (honest record)

- **FHIR R5 official JSON Schema: 11/11 resources PASS** (2026-10-28, jsonschema
  Draft6 against https://hl7.org/fhir/R5/fhir.schema.json). The ImplementationGuide
  shell is included; it was repaired this round (R4-style `exampleBoolean` → R5
  `isExample`; `manifest.resource` reference type prefixes corrected to the real
  resource types). Cross-resource consistency (counts, duplicate codes, dangling
  references, TSV reconciliation 164/36) also passes.
- **HL7 official validator_cli (java): NOT RUN** — no Java runtime on the build
  machine. Before any external submission, re-verify all resources at
  https://validator.fhir.org (official online validator) or with validator_cli.
- **External review: NOT DONE.** Recommended before registration.

## 4. Namespace decision

**DECIDED (2026-10-28, pre-publish review):** all canonical URLs use
**`https://stevenzhao07.github.io/medxpert-fhir/`** as the namespace
(e.g. `…/CodeSystem/medxpert-meddev-en`), published via GitHub Pages
(repository already has `has_pages=true`). The earlier placeholder
`https://medxpert.skills/fhir/` was abandoned because the domain is not
registered. URLs must be frozen at first public publication — they are
permanent identifiers.

## 5. Authorship & originality statement

- **Original compilation.** The selection, categorization (`kind`), semantic
  notes ("validation vs confirmation", "warning strength must not be weakened"),
  and the 36 mistranslation rules are original MedXpert work, authored by the
  project (MIT).
- **Term renderings trace to public standards.** The EN→ZH renderings are based
  on published official terminology of ISO (Chinese editions), GB/T national
  standards, NMPA regulations, EU MDR/IMDRF documents and FDA guidance. They are
  factual standard terms, not third-party copyrighted text; no external
  termbase content was copied verbatim.
- **License:** MIT; source data at https://github.com/stevenzhao07/medxpert-skills.

## 6. Submission channels (recommendation)

| Priority | Channel | Action | Status |
|----------|---------|--------|--------|
| 1 | A. FHIR IG Registry | Register IG via PR to the registry repo or email `fhir-director@hl7.org` | IG shell ready; external review pending |
| 2 | B. HL7 China Committee | Offer term base as input to China FHIR recommended IG (in preparation) | Official notice lists `fhir@hl7.org.cn`; verify against `sec@hl7.org.cn` before sending (recommend sending to both) |
| 3 | C. FHIR Connectathon | Participate with a terminology server implementing the package | Needs runnable server (future work) |

## 7. Reproduction

```bash
python build_fhir.py          # termbase.tsv + mistranslations.tsv -> 10 resources
python generate_ig.py         # builds the ImplementationGuide shell
python validate_all_schema.py # official R5 JSON Schema validation
```

Inputs: `termbase.tsv` (164 rows), `mistranslations.tsv` (36 rows), from
`https://github.com/stevenzhao07/medxpert-skills` (skill folder
`skills/skills-medxpert-termbase-master-*/`; data files at `references/termbase.tsv`
and `references/mistranslations.tsv`, verified via raw.githubusercontent.com on
2026-10-28).
