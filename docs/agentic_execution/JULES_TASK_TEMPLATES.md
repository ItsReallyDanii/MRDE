# Jules Task Templates

These are standard prompt templates to be used when orchestrating Jules for MRDE tasks. They ensure Jules operates strictly within authorized bounds.

## 1. Doc-Only Patch
**Prompt:**
```markdown
Jules, please perform a documentation update.
- **Goal:** [Describe doc update goal]
- **Target Files:** [List specific .md files]
- **Constraint:** Do not modify pipeline code, data files, or schemas.
- **Constraint:** Respect the Claim Language Gate; do not use `SUPPORTED`, `VALIDATED`, `PROVEN`, or `DISCOVERED`.
- **Output:** Prepare a PR with the updated markdown and summarize your changes.
```

## 2. Schema/Test Patch
**Prompt:**
```markdown
Jules, please update tests or schema definitions.
- **Goal:** [Describe test/schema goal]
- **Target Files:** [List test or schema files]
- **Constraint:** Do not modify pipeline logic or data files.
- **Constraint:** After modifying, run the MRDE Test Runner wrapper and ensure all tests pass.
- **Output:** Prepare a PR with the diff and the deterministic output of the test run.
```

## 3. Audit-Only Run
**Prompt:**
```markdown
Jules, perform an audit-only review of the repository state.
- **Goal:** Check for adherence to MRDE boundaries and schemas.
- **Target Scope:** [Define directory or file scope]
- **Constraint:** This is a read-only task. Do not modify any files.
- **Output:** Provide a structured, deterministic summary of any violations found.
```

## 4. Diff Review
**Prompt:**
```markdown
Jules, perform a Diff Scope Gate review on the current branch/PR.
- **Target:** Branch `[Branch Name]` or PR `[PR Number]`
- **Constraint:** Check if any files modified fall outside the original task scope (e.g., pipeline modifications in a doc-only patch).
- **Constraint:** Flag any unauthorized changes.
- **Output:** A deterministic list of files modified and a pass/fail flag for scope adherence.
```

## 5. Log Summary
**Prompt:**
```markdown
Jules, summarize the provided experiment/test logs.
- **Target Logs:** [Path to log files]
- **Constraint:** Use the Log Summarizer pattern. Provide only objective metrics (e.g., pass/fail counts, extracted error messages).
- **Constraint:** Do not infer, interpret, or summarize any scientific narrative. Do not use prohibited claim terms.
- **Output:** A structured JSON or bulleted markdown summary of the logs.
```
