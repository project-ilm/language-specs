# <Language> <HostLanguage> Language Specification

## 1. Scope
This document specifies <Language><HostLanguage>, a <Language> lexical form of <HostLanguage> by token
equivalence. A translation unit denotes the corresponding <HostLanguage> translation unit; its meaning is the
meaning of that unit under the selected <HostLanguage> standard.

## 2. Normative relationship
Except where a localized spelling is defined here, syntax and semantics are those of <HostLanguage>.

## 3. Token equivalence
| <Language> | <HostLanguage> |
| --- | --- |
| <native_keyword> | <host_keyword> |
<!-- generate the full table from the keyword registry: construct,native_keyword,romenagri -->

## 4. Conformance
A conforming program uses only defined tokens where the corresponding host tokens are valid, and has a
well-formed corresponding <HostLanguage> translation unit.

## 5. Diagnostics / undefined behavior
As <HostLanguage>, via the corresponding translation unit.
