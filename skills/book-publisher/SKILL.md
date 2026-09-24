---
name: book-publisher
description: Plan and run an AI-assisted book workflow from project brief and manuscript drafting through editorial QA and publication, with optional presentation and website outputs. Use for creating, resuming, auditing, or publishing a book project; do not use for a one-off document edit.
---

# Book Publisher

Turn a book idea into a traceable publishing project. Preserve the author's intent, make editorial decisions explicit, and require evidence before marking a stage complete.

## Start or resume

1. Locate `book-project.json` in the project root.
2. If it does not exist, gather the minimum brief: working title, audience, purpose, language, writing style, publishing route, and desired outputs. Then run `python <skill-dir>/scripts/init_project.py <project-dir>` and update the generated files with the user's answers.
3. If it exists, run `python <skill-dir>/scripts/validate_project.py <project-dir>` before editing. Resume from the first incomplete stage; do not restart completed work.
4. Treat `book-project.json` as workflow state and `manuscript/` as the source of truth for book content.

Read [references/workflow.md](references/workflow.md) for stage gates. Read [references/project-schema.md](references/project-schema.md) when creating or repairing state. Read [references/publishing.md](references/publishing.md) only when export, slides, a website, or external publication is requested.

## Working rules

- Confirm facts, quotations, licenses, and current product details from primary sources. Mark unresolved claims in `qa/open-issues.md`; never invent citations.
- Separate drafting from review. A review pass must evaluate the manuscript against the brief, continuity, evidence, reader usefulness, and house style.
- Keep examples, references, and generated assets inside the user's project. Do not copy private material from another project.
- Preserve user edits. When generated and edited versions differ, reconcile them explicitly instead of overwriting the edited version.
- External upload, deployment, purchase, or publication requires the user's authorization at that step. Local drafts and validation do not.
- Optional outputs inherit content from the approved manuscript. Slides are a spoken narrative, not a chapter dump; websites are a reading interface, not a second manuscript.

## Completion

Run the validator after every stage transition. Report completed gates, remaining issues, output paths, and any external action still awaiting authorization. A project is complete only when all requested outputs are validated and `status` is `complete`.
