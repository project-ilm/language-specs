<!-- context: https://ilm.codes/context/ -->
# Shaili Specification — Hindi (hi)
**Family:** Brahmi (Devanagari) · **Source of truth:** Hindawi Indic Programming System (A. Choudhary, 2003-2006, GPL-2.0-or-later) · **Status:** Reference
## Abstract
The Hindi realization is **not** a reinvented keyword list: it is the Hindawi mapping itself. The package ships the
original bidirectional lex transducers (`toolchain/h2c.uhin` Hindi→C and `toolchain/c2h.uhin` C→Hindi) which carry the
complete coverage — full C library, headers (e.g. मानकपन.स ↔ stdio.h), preprocessor (#समावेश ↔ #include), escape
sequences (\न ↔ \n) and hundreds of identifiers — and the working sample programs in `samples/` that compile and run
via `hincc`. `keywords/<host>.tsv` is the extracted canonical↔native table for tooling; the lexers remain authoritative.
Reversibility is a property of the transducer pair, not of this table.
## 1. Scope  ## 2. Normative references (host standards by citation; Hindawi as prior art)  ## 3. Keyword mapping (keywords/, generated from toolchain/)  ## 4. Conformance (h2c∘c2h round-trip)  ## 5. IP & licensing
GPL-2.0-or-later (Hindawi lineage) / CC-BY-4.0 · © 2003-2026 Abhishek Choudhary.