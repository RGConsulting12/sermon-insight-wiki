Figma frame plan — Sermon insight web app (Flask + Jinja + HTMX)
Assumptions baked into this plan: desktop-first frames; main content column max 1280px centered inside a 1440px-wide canvas (matches typical max-w-7xl feel); vertical scroll for long pages. Sermon detail maps to production route /video/<video_id>.

Naming conventions
Frames
[Viewport] / [Route path] / [Screen state]

Examples:

Desktop / home / default
Desktop / search / results-semantic
Desktop / repository / default
Desktop / pipeline / running
Desktop / sermon-detail / default
Optional suffix for experiments: - v2, - alt-nav.

Components (shared)
DS / [Category] / [Name]

Categories: Chrome, Nav, Layout, Content, Form, Feedback, Data, Media, Actions.

Examples: DS / Chrome / App shell, DS / Data / Stat tile, DS / Form / Search field.

Component variants (Figma properties)
Use consistent property names across the library:

State: Default | Hover | Focus | Disabled | Loading
Intent: Neutral | Brand | Success | Warning | Danger
Density: Comfortable | Compact (for tables/rows)
Breakpoint (optional, for responsive notes): Desktop | Tablet | Mobile (even if you only draw desktop first, define rules here)
Tokens / styles to define first
Define these before placing many screens so frames stay consistent.

Color (semantic-first)
Background / canvas: page wash, content surface, elevated surface
Border / divider: default, subtle
Text: primary, secondary, tertiary, inverse (if dark nav)
Intent fills: success, warning, danger, info (surface + on-surface text)
Brand: primary, primary-hover, focus ring
Data viz (optional): chart lines if you use charts later
Typography (type scale)
Display / page title (H1)
Section title (H2)
Subsection (H3)
Body
Body small / metadata
Mono (IDs, paths, technical strings)
Map to text styles in Figma: Type / Display, Type / H2, …

Spacing scale
8pt system recommended: 4, 8, 12, 16, 24, 32, 40, 48, 64 as variables Space / *.

Radius
SM / MD / LG (cards, inputs, pills)
Full (avatars if any)
Shadows
Card default, Card hover (subtle), Modal (if ever)
Layout tokens
Content max width: 1280
Page padding X: 24–32 (desktop)
Section gap Y: 24–32
Effects
Focus ring (outline style for a11y parity with implementation notes)
Suggested page hierarchy (Figma left sidebar)
Order top → bottom:

00 — Cover
File title, owner, last updated, link to product spec
01 — Foundations
Color styles / variables, type ramp, spacing, radius, shadows, grid
02 — Components
All DS / … components and variants
03 — Patterns
Composed blocks used on multiple routes (e.g. “Sermon list module”, “RAG answer + sources”)
04 — Screens / Desktop
All route frames (default + key states)
05 — Screens / Responsive (optional)
Tablet/mobile only for: Chrome, Nav, Sermon list, Repository table
06 — Archive / Explorations
Old directions
Shared component inventory
Chrome & layout
Component name	Role	Suggested variants
DS / Chrome / App shell
Top nav + optional footer + content slot
With footer / No footer
DS / Nav / Primary
Main IA links
`Item=Default
DS / Layout / Page container
Centers max width, horizontal padding
Max=1280
DS / Layout / Page header
Title + description
With actions / No actions
DS / Layout / Section
Titled block wrapper
`Spacing=Lo
Forms & actions
Component name	Role	Variants
DS / Form / Text input
Single-line fields
State, optional With icon
DS / Form / Textarea
Pipeline bulk paste
Rows=5 default
DS / Form / Search bar
Field + primary button (GET search)
Loading optional
DS / Actions / Button
Primary / secondary / ghost / danger
State, Intent
DS / Actions / Link button
Text action in tables
State
Content & data
Component name	Role	Variants
DS / Data / Stat tile
Dashboard metrics
`Icon=On
DS / Data / Sermon list row
Home + similar lists
Density, optional Chevron
DS / Data / Status banner
Pipeline/API states
Intent
DS / Data / Inline help
Blue/purple explainer panels
`Intent=Info
DS / Data / Pill
Artifact badges
`Type=Transcript
DS / Data / Table
Repository
Header sticky note as variant or doc
DS / Data / Table row
One sermon artifact row
`Embeddings=Yes
DS / Content / Card
Generic surface
`Elevation=Flat
DS / Content / Quote callout
Golden quotes, matched excerpts
`Style=Yellow
DS / Content / Numbered list item
Takeaways
Number slot
DS / Content / RAG answer
Search AI block
`Length=Short
DS / Content / Search result item
Search source row
`Mode=Semantic
DS / Content / Transcript panel
Collapsed/expanded
`State=Collapsed
DS / Media / External link — Watch sermon
YouTube CTA
State
Feedback
Component name	Role	Variants
DS / Feedback / Empty state
Zero lists, no results
`Scene=Home
DS / Feedback / Loading text
“Generating…”, status fetch
—
DS / Feedback / Progress bar
Pipeline batch
Value as number property
DS / Feedback / HTMX indicator
Small inline spinner row
(annotation component)
Pipeline-specific (still reusable if parameterized)
Component name	Role	Variants
DS / Pipeline / Stage step
Icon + label + state
`Stage=Queued
DS / Pipeline / Queued sermon row
ID + external link
—
DS / Pipeline / Tab underlined
Individual vs playlist
Active boolean
Per-route frame plan
Global default for all route frames
Frame name root: Desktop / …
Frame size: 1440 × 900 minimum height; extend frame downward to fit full scroll for Repository, Pipeline (running), Sermon detail, Search results.
Major layout regions (all routes):
R1 — Top chrome (nav) · R2 — Page body (max 1280 centered) · R3 — Optional footer (short strip; match product decision)
Responsive behavior (all):

Desktop (1440): side margins = (1440 - 1280) / 2.
Tablet (Assumption, not drawn initially): reduce horizontal padding; nav may collapse to hamburger (DS / Nav / Primary → Mobile variant).
Mobile (Assumption): single column; stat tiles 2×2 or 1×4 stack; repository table → stacked cards per sermon (DS / Data / Table row repurposed as card variant).
Reusable vs page-specific:

Reusable: R1 shell, page container, page header, cards, buttons, banners, table primitives, sermon row, pills.
Page-specific: exact copy blocks, illustrative long transcript, realistic dummy sermon titles (instance overrides only—do not fork components per page).
1) / — Home / Dashboard
Field	Specification
Frame name
Desktop / home / default (+ optional Desktop / home / empty)
Desktop frame size
1440 × 2200 (scroll); hero stats + list can be tall
Major layout regions
R1 App nav · R2a Page header · R2b Stat grid · R2c Dashboard search strip · R2d Processed sermons list
Region	Components to place	Suggested variants
R1
DS / Chrome / App shell + DS / Nav / Primary
Active item = Home
R2a
DS / Layout / Page header
Optional secondary link to /pipeline in header actions variant
R2b
4× DS / Data / Stat tile
Different Icon / labels as instances
R2c
DS / Form / Search bar
Action label = Search, Placeholder for ministry question style
R2d
Stack of DS / Data / Sermon list row (6–10 instances)
Density=Comfortable; empty frame uses DS / Feedback / Empty state
Responsive notes: Stat grid 4 columns → 2 → 1; sermon rows keep full width; search bar stacks field above button on narrow widths.

Reusable vs specific: Rows and tiles are instances; only copy and numbers are page-specific.

2) /search — Ask across sermons
Field	Specification
Frame names
Desktop / search / no-query · Desktop / search / results-semantic · Desktop / search / no-results · optional Desktop / search / results-keyword
Desktop frame size
1440 × 2600 for results (answer + many sources)
Major layout regions
R1 Nav · R2a Page header + embeddings status (right cluster) · R2b Search form + semantic explainer · R2c Answer (conditional) · R2d Sources list (conditional) · R2e Empty / no-results (mutually exclusive with R2c–d in separate frames)
Region	Components	Variants
R1
Shell + nav
Active = Search
R2a
Page header + small Status text or Pill for embeddings
`Embeddings=Ready
R2b
Search bar + Inline help
Help Intent=Info
R2c
RAG answer inside Card
Length examples
R2d
Repeat Search result item
Mode=Semantic (excerpt + relevance) or Mode=Keyword (chips)
R2e
Empty state
Two frames: no query vs no results
Responsive notes: Results stack; relevance and chips wrap; consider max readable line length for answer text (not full 1280 if readability suffers—optional inner column 720–800 for prose only; document as content sub-grid).

Reusable vs specific: Modes are variants/instances; mock Q&A text is page-specific.

3) /repository — Sermon library (artifacts)
Field	Specification
Frame name
Desktop / repository / default (+ Desktop / repository / empty)
Desktop frame size
1440 × 2800 (table + structure section)
Major layout regions
R1 Nav · R2a Page header · R2b Summary stat row · R2c Path disclosure (optional “advanced” treatment in notes) · R2d Table · R2e Repository structure preview
Region	Components	Variants
R1
Shell + nav
Active = Repository
R2b
4× Stat tile
Different metrics
R2c
Card + mono Type / Mono path
Optional DS / Actions / Link “Copy path” (future)
R2d
Table + header row + N× Table row
Row: Embeddings=Generating uses Loading text + disabled actions
R2d actions column
Link button, Button ghost for generate
HTMX noted in design description only
R2e
Card + tree lines
Static preview
Responsive notes: Horizontal scroll inside table for tablet; mobile = card stack per sermon with pills in a 2-column subgrid.

Reusable vs specific: Table + pills are library-driven; file names / IDs are instance text.

4) /pipeline — Ingest & process
Field	Specification
Frame names
Desktop / pipeline / idle-queue-empty · Desktop / pipeline / idle-queue-has-items · Desktop / pipeline / running · Desktop / pipeline / api-error
Desktop frame size
1440 × 3200 for running (detailed progress); 1440 × 2000 for idle
Major layout regions
R1 Nav · R2a Page header · R2b Pipeline status · R2c YouTube API status · R2d Add sources (tabs + forms + result slot) · R2e Detailed progress (running only) · R2f Queued sermons + start CTA · R2g Processed summary
Region	Components	Variants
R2b
Status banner + Progress bar
Intent=Warning when running, Success when idle
R2c
Status banner
`Intent=Success
R2d
Tab underlined + Textarea / Text input + Button groups + empty Card for results
Individual vs Playlist tabs
R2e
Stack of Stage step + per-sermon progress rows (compose as pattern)
Multiple Active steps
R2f
Queued sermon row list + primary Button “Process N…”
N>0 vs empty state
R2g
Inline help + text link to repository
—
Responsive notes: Queued list and progress stacks vertically; avoid horizontal split on small screens.

Reusable vs specific: Stage iconography is shared; numeric counts are instance properties.

5) /video/<id> — Sermon detail
Field	Specification
Frame name
Desktop / sermon-detail / default (+ optional Desktop / sermon-detail / no-transcript)
Desktop frame size
1440 × 4000+ (long transcript)
Major layout regions
R1 Nav · R2a Back link row · R2b Sermon header · R2c Summary · R2d Takeaways · R2e Quotable lines · R2f Transcript
Region	Components	Variants
R2a
DS / Actions / Link button
“Back to Home”
R2b
Card + title Type / Display + metadata row + External link — Watch sermon + description excerpt
Metadata chips optional
R2c–e
Card + Numbered list item / Quote callout
Quote Style=Yellow
R2f
Transcript panel
`Collapsed
Responsive notes: Metadata chips wrap; transcript inner scroll max-height on desktop; mobile full width with same scroll behavior.

Reusable vs specific: Structure is 100% components; sermon text is content only.

Cross-cutting: what to draw once vs per frame
Draw once in 02 — Components	Instantiate per screen
Buttons, inputs, pills, cards, nav, shell, banners
Titles, counts, row text, Q&A copy
Table primitives
Row count
Empty states (variant per scene)
—
Sermon row
—
Optional secondary frames (not in original five routes)
If you add Operations later:

Desktop / stats / default
Desktop / costs / default
Use the same R1–R2 structure and reuse Stat tiles, Tables, Cards.

Checklist before duplicating frames
Variables for color, space, radius exist.
Text styles for full ramp.
App shell + Nav pinned or placed first on every screen.
Auto-layout on: page container, section stacks, table rows, sermon rows.
Component props for Intent, State, Mode where listed—avoid exploding combinations; use separate frames for semantic vs keyword if variants get unwieldy.