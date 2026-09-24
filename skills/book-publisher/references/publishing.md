# Publishing outputs

Read this reference only when producing release files or publishing externally.

## Source hierarchy

1. Approved Markdown in `manuscript/`
2. Project decisions in `brief.md` and `book-project.json`
3. Licensed project assets in `assets/`
4. Generated files in `dist/`

Never edit only an exported file. Apply content corrections to the approved manuscript and regenerate the affected output.

## Export checklist

- Title, author attribution, edition, and date are consistent.
- Contents, headings, internal links, footnotes, and page breaks work.
- Images have permission, captions, and useful alternative text where supported.
- Fonts render on a clean machine or are embedded with a compatible license.
- The output opens without repair warnings.
- A checksum is recorded in release evidence.

## Presentation checklist

- Audience and duration are explicit.
- The deck has a single narrative arc and a clear closing action.
- Slides remain readable at presentation distance.
- Speaker notes are natural speech and contain enough context to present without the manuscript.
- PPTX and PDF are checked independently.

## Website checklist

- The approved manuscript remains the content source.
- Keyboard navigation, contrast, mobile layout, metadata, and broken links are checked.
- Download links point to the current release.
- Secrets, drafts, private sources, and local absolute paths are absent.

Do not claim an external publication or deployment succeeded until the public URL has been opened and checked.
