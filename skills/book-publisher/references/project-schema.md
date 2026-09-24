# Project state

book-project.json is a small, portable workflow record. Required fields:

~~~json
{
  "schema_version": 1,
  "title": "Working title",
  "language": "en",
  "audience": "Who this book serves",
  "purpose": "What changes for the reader",
  "writing_style": "Describe the voice and conventions",
  "publishing_route": "local-files",
  "outputs": {
    "manuscript": true,
    "presentation": false,
    "website": false
  },
  "status": "in_progress",
  "stages": {
    "brief": "in_progress",
    "research": "not_started",
    "plan": "not_started",
    "draft": "not_started",
    "qa": "not_started",
    "release": "not_started"
  },
  "evidence": {
    "brief": [],
    "research": [],
    "plan": [],
    "draft": [],
    "qa": [],
    "release": []
  }
}
~~~

Allowed status values are not_started, in_progress, blocked, and complete. Keep evidence paths relative to the project root so the project can move between machines.

Each evidence key is required and contains relative paths to files that prove the corresponding stage result. A stage marked complete must have at least one existing evidence file:

- brief: approved brief or scope decision
- research: source ledger or research report
- plan: table of contents or chapter plan
- draft: manuscript file; manuscript/ must contain at least one Markdown file
- qa: editorial report; the generated qa/open-issues.md alone does not count
- release: release manifest or output file; dist/ must contain at least one file

Set project status to complete only when every requested output exists and its release checks have passed. Optional presentation and website work belong to the release stage; their absence is valid when the corresponding output is false.
