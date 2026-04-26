Figma UI spec — frame plan continuation (sermon intelligence enhancements)
This document extends the earlier frame plan (foundations, Desktop / home, search, repository, pipeline, sermon-detail). It adds new frames, new/updated components, and Figma file structure so the Make → Design handoff stays aligned with a sermon intelligence platform (not a generic transcript tool).

No code — layout, naming, and component instructions only.

1. Updates to Figma file hierarchy (sidebar)
Add these pages after existing 04 — Screens / Desktop (or merge if you prefer one desktop page):

New page	Contents
04b — Screens / Enhancements — Now
Sermon detail, Search (intelligence), Metadata patterns, DS shell refresh
04c — Screens / Enhancements — Next
Library / repository v2, Pipeline visibility v2
04d — Screens / Enhancements — Later
Scripture block, timestamps on results, advanced ops, density modes
Optional:

Page	Contents
02b — Components / Sermon domain
All new DS / Sermon / … and DS / Intel / … compositions (keeps primitives under 02 — Components)
2. Naming convention additions
Frames (unchanged pattern):
Desktop / [route or feature] / [state]

New route labels for Figma (match product language; URLs can stay implementation-specific in dev notes):

Product frame	Dev note (annotation only)
home
/
ask
/search
library
/repository
pipeline
/pipeline
sermon-detail
/video/<id>
New component prefixes (avoid cluttering generic DS / Data):

DS / Sermon / … — anything that displays sermon identity or body content.
DS / Intel / … — search, RAG, index readiness, relevance.
DS / Ops / … — pipeline, queue, API health, errors.
3. Token / style additions (define early on 01 — Foundations)
Add semantic intents beyond the base plan:

Token group	Purpose
Intent / Index-ready
Semantic index available (distinct from generic “success”)
Intent / Index-missing
Transcript exists but not indexed
Intent / Processing
Pipeline running
Intent / Source
External “watch sermon” (e.g. red/brand link, not primary button blue)
Text / Scripture (optional, Later)
Distinct from body for references
Typography: add Type / Scripture or use Type / Body small + semibold until Later.

4. Shared component inventory — additions
DS / Sermon (new)
Component	Variants / props	Notes
DS / Sermon / Title block
Has series, Has speaker, Has date booleans
Primary title + secondary meta line
DS / Sermon / Metadata chips
Chip count via nested instances
Date, series, speaker, campus
DS / Sermon / Scripture chips
Later
Parsed refs
DS / Sermon / Section card
Elevation
Wraps summary, takeaways, quotes
DS / Sermon / Takeaway item
Number
Numbered insight
DS / Sermon / Quote callout
`Style = Gold
Neutral`
DS / Sermon / Transcript panel
`State = Collapsed
Expanded`
DS / Sermon / Watch link
State
External sermon recording
DS / Intel (new)
Component	Variants / props	Notes
DS / Intel / Index status
`Ready
Partial
DS / Intel / RAG answer card
Length demo only in examples
Grounded answer
DS / Intel / Source result row
`Mode = Semantic
Keyword`
DS / Intel / Search empty
—
No query
DS / Intel / Search no-results
—
Query + zero hits
DS / Intel / Index nudge
Intent = Warning
Points to Library
DS / Ops (new)
Component	Variants / props	Notes
DS / Ops / Pipeline banner
`Idle
Running
DS / Ops / Stage step
Stage, State
Queued → … → Extract
DS / Ops / Queue row
Has error
Id + link + optional title
DS / Ops / API status card
`OK
Error`
DS / Ops / Progress bar
Percent
Batch progress
Chrome refresh (extend existing)
Component	Change
DS / Chrome / App shell
Slot for ministry name + product name (not generic “YouTube…”)
DS / Nav / Primary
Items: **Home
5. Frame plan by enhancement area
Each subsection lists new or updated frames, size, regions, components, variants, responsive, reusable vs page-specific.

A. Sermon detail page (Now)
Frame name	Size	Purpose
Desktop / sermon-detail / default
1440 × 4200
Full content + long transcript
Desktop / sermon-detail / no-transcript
1440 × 2400
Omit transcript region
Desktop / sermon-detail / minimal-metadata
1440 × 2400
Title + date only (missing series/speaker)
Major regions

R1 App shell + Nav (sermon-detail has no active nav item or highlight Library if entered from library — use variant Active = None | Library)
R2 Breadcrumb: Home → Library → Sermon title (truncate)
R3 Sermon header: Title block, Metadata chips, description excerpt, Watch link
R4 Summary — Sermon / Section card
R5 Takeaways — list of Takeaway item
R6 Quotable lines — Quote callout stack
R7 Transcript — Transcript panel (if applicable)
Suggested variants

Transcript panel: Collapsed / Expanded on separate frames or component variant
Metadata chips: show/hide series, speaker, campus
Responsive

Chips wrap; transcript keeps inner max-height + scroll on desktop; mobile single column, full width.
Reusable vs page-specific

Reusable: all DS / Sermon/*, shell, breadcrumb pattern.
Page-specific: sermon copy, counts, optional scripture (Later).
B. Semantic search workflow — “Ask” (Now)
Frame name	Size	Purpose
Desktop / ask / no-query
1440 × 1400
Entry + index status
Desktop / ask / results-semantic
1440 × 3200
Answer + many sources
Desktop / ask / results-keyword
1440 × 2600
Chips + different answer tone
Desktop / ask / no-results
1440 × 1800
Query + empty
Desktop / ask / index-partial
1440 × 2000
Index status + Index nudge + still allow search
Major regions

R1 Shell + Nav (Active = Ask)
R2 Page header + Intel / Index status (right cluster)
R3 Search bar (ministry-oriented placeholder) + short Inline help (grounded in archive)
R4 Intel / RAG answer card (conditional)
R5 Sources — stack of Intel / Source result row (Mode=Semantic or Keyword)
R6 Empty / no-results — Intel / Search empty or Search no-results
Suggested variants

Source result row: Mode, optional Show relevance %, optional Show date under title
Index status: Ready | Partial | None | Unknown
Responsive

Answer text: optional inner max-width (720–800) for readability inside 1280 column — annotate as “prose column” auto-layout.
Source rows: stack; relevance on second line on narrow.
Reusable vs page-specific

Reusable: all Intel components + search bar.
Page-specific: mock Q&A and result copy.
C. Sermon library / repository (Next)
Frame name	Size	Purpose
Desktop / library / default
1440 × 3000
Full table
Desktop / library / empty
1440 × 1600
No sermons
Desktop / library / row-generating-index
1440 × 2200
One row in “generating” state (hero crop)
Desktop / library / advanced-path
Same as default + toggle in annotations
Path disclosure expanded vs collapsed
Major regions

R1 Shell + Nav (Active = Library)
R2 Page header (sermon library, not “insight files” in final copy)
R3 Stat row — extend existing tiles: add Index-ready count (new tile or replace one — annotate)
R4 Optional “Advanced” collapsible: path (Mono) — use Card + disclosure pattern
R5 Table: header + Library table row (rename from generic Table row in spec)
Library table row — composition

Col1: Sermon / Title block (compact) + mono id subline
Col2: takeaway / quote counts
Col3: Artifact pill set (transcript, audio, chunks, embeddings)
Col4: size, modified
Col5: actions — Open sermon, View JSON, Download, Generate index (states)
Suggested variants

Row: Embeddings = Yes | No | Generating | No transcript
Table: Density = Comfortable | Compact
Responsive

Tablet: horizontal scroll for table or sticky first column (annotate).
Mobile: card stack using same row content in Library / Card instance (new component or variant of row “layout=Card”).
Reusable vs page-specific

Reusable: pills, row, stats.
Page-specific: numbers, file names in preview tree.
D. Processing pipeline visibility (Next)
Frame name	Size	Purpose
Desktop / pipeline / idle-empty-queue
1440 × 2000
Desktop / pipeline / idle-queue-ready
1440 × 2400
CTA visible
Desktop / pipeline / running
1440 × 3600
Banner + per-sermon stepper + detail module
Desktop / pipeline / api-error
1440 × 2200
Desktop / pipeline / row-error
1440 × 2800
At least one Queue row with error
Major regions

R1 Shell + Nav (Active = Pipeline)
R2 Page header
R3 Ops / Pipeline banner + optional Ops / Progress bar
R4 Ops / API status card
R5 Ingest — tabs + forms (reuse existing tab pattern; align naming to “Add sermons”)
R6 Running only: Per-sermon panel: Queue row + horizontal or vertical Stage step sequence + error text slot
R7 Queue list + primary Process queue CTA
R8 Footer strip: “View in Library” link
Suggested variants

Stage step: each stage + Pending | Active | Done | Error
Pipeline banner: Idle | Running | Error
Responsive

Stepper: vertical stack on narrow; keep one column for queue.
Reusable vs page-specific

Reusable: Ops components, ingest tabs.
Page-specific: counts, ids, error strings.
E. Sermon-specific metadata display (Now on lists; Next when data rich)
Not a separate route — pattern frames on a dedicated page so designers apply consistently:

Frame name	Size	Purpose
Desktop / patterns / sermon-metadata — list-row
1440 × 800
Sermon list row with full meta
Desktop / patterns / sermon-metadata — search-source
1440 × 800
Source result row meta
Desktop / patterns / sermon-metadata — library-row
1440 × 800
Compact + pills
Components

Sermon / Title block (all three contexts as instances with different Density prop)
Priority

Now: pattern frames drive Home + Ask + Detail.
Later: Scripture chips frame.
F. Reusable design system — review surface (Now / Later)
Frame name	Size	Purpose
Desktop / ds-gallery / components
1440 × variable
All new components in a grid for QA
Desktop / ds-gallery / nav-states
1440 × 400
Nav Active per route
Responsive

Gallery is desktop-only Later if needed.
6. Continuation summary — build order inside Figma
01 — Foundations — add index / processing intents.
02 — Components — ship DS / Sermon/*, DS / Intel/*, DS / Ops/*, update Nav + App shell.
04b — Now — frames: sermon-detail (set), ask (set), patterns/metadata, ds-gallery.
04c — Next — library (set), pipeline (extended set).
04d — Later — scripture, result timestamps, mobile/tablet breakpoints for Library + Nav.
7. Traceability to product priorities
Priority	Frames to create / refresh
Now
sermon-detail/*, ask/*, patterns/sermon-metadata, ds-gallery, Nav + shell
Next
library/*, pipeline/* (extended)
Later
Scripture pattern, mobile Library cards, extra ops (pause/retry)