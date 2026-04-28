# Logs

`append_only_log.jsonl` is the project audit trail.

Rules:

- append entries only;
- never overwrite or delete prior entries;
- if an entry is wrong, add a correction entry referencing it;
- keep entries JSONL-compatible;
- use `08_APPEND_ONLY_LOG_SCHEMA.md` and `schemas/append_only_log.schema.json` as references.

Current state:

- contains an initial Stage 0 `changelog_entry` recording governance-package placement and post-Claude scaffold cleanup;
- contains no experiment data, residuals, validation results, or claim-tier assignments.
