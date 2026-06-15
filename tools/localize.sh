#!/usr/bin/env bash
# localize.sh — DISABLED. The previous version piped whole markdown through `trans` with no language pair,
# which translated heading words (e.g. "Abstract") into dictionary dumps and corrupted hi/ur/fa.
# A markup-safe localizer (translate prose only; protect headings/code/proper-nouns; trans -b en:<lang>)
# is pending. Refuse to run until then. context: https://ilm.codes/context/
echo "localize.sh is intentionally disabled pending a markup-safe rewrite. See language-specs/en/ masters." >&2
exit 2
