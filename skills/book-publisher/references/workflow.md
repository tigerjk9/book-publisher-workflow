# Workflow and gates

Use only the stages needed by the requested outputs. Before changing a stage to complete, add at least one existing relative file path under its evidence key in book-project.json. See [project-schema.md](project-schema.md) for the required evidence and artifact checks.

## 1. Brief

Define the reader, their problem, the promised change, scope boundaries, voice, format, and outputs. Completion evidence: brief.md has no placeholder fields and the table of contents supports the promise.

## 2. Research

Build a source ledger in research/sources.md. Separate source facts, author interpretation, and examples. Completion evidence: claims needing support have a source or appear in qa/open-issues.md.

## 3. Plan

Create chapter briefs with one outcome, up to three core ideas, examples, and dependencies. Completion evidence: every planned chapter serves the book promise and has an observable reader outcome.

## 4. Draft

Write in manuscript/, one chapter per Markdown file. Put concepts near examples and exercises. Completion evidence: all planned chapters exist, cross-references resolve, and no scaffold placeholders remain.

## 5. Editorial QA

Run separate passes for structure, reader experience, factual support, continuity, language, and asset rights. Record findings in qa/. Completion evidence: blocking findings are resolved; accepted limitations are explicit.

## 6. Release

Create requested formats from the approved manuscript. Keep generated files in dist/ and record their paths and checksums as evidence. Completion evidence: files open correctly, navigation works, and text/assets match the approved manuscript.

## Optional presentation

Design a talk arc for a specified audience and duration. Each slide should carry one idea and speaker notes should provide a natural spoken bridge, example, and action. Validate slide legibility and exported PDF separately.

## Optional website

Choose a static or hosted approach that fits the user's environment. Validate responsive reading, navigation, metadata, accessibility, asset licenses, and links. Deployment is a separate authorized action.

## Stage status

Use not_started, in_progress, blocked, or complete. A stage may be blocked only with a concrete reason and next action in qa/open-issues.md.
