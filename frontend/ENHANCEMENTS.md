# Sermon Insight - UI Enhancements

This document outlines the UI enhancements made to the Sermon Insight application based on the Figma design specification.

## Overview

The application has been enhanced with ministry-focused terminology, improved component organization, and better semantic design tokens to create a more professional sermon intelligence platform.

## Key Changes

### 1. Terminology Updates
- **"Search"** → **"Ask"** (more natural, ministry-focused language)
- **"Repository"** → **"Library"** (clearer for end users)
- Added ministry context throughout (e.g., "Grace Community Church")

### 2. New Design Tokens

Added semantic color tokens to `theme.css`:
- `--index-ready`: For indexed/searchable sermons
- `--index-missing`: For sermons awaiting indexing
- `--processing`: For active pipeline operations
- `--source`: For external sermon links (YouTube)

### 3. Component Architecture

#### DS/Sermon Components (Sermon Domain)
Located in `/src/app/components/sermon/`:
- **TitleBlock** - Displays sermon title with metadata (speaker, series, date)
- **MetadataChips** - Icon-based chips for date, speaker, series, campus
- **SectionCard** - Consistent card wrapper for sermon sections
- **TakeawayItem** - Numbered insight items
- **QuoteCallout** - Highlighted quotes with gold/neutral styling
- **TranscriptPanel** - Collapsible/expandable transcript viewer
- **WatchLink** - External sermon video link

#### DS/Intel Components (Search Intelligence)
Located in `/src/app/components/intel/`:
- **IndexStatus** - Shows indexing status (ready/partial/none/unknown)
- **RAGAnswerCard** - AI-generated answer display with source count
- **SourceResultRow** - Search result with semantic/keyword modes
- **SearchEmpty** - Empty state for no query
- **SearchNoResults** - Empty state for zero results
- **IndexNudge** - Warning banner for missing embeddings

#### DS/Ops Components (Pipeline Operations)
Located in `/src/app/components/ops/`:
- **PipelineBanner** - Status banner (idle/running/error)
- **StageStep** - Processing stage indicator (pending/active/done/error)
- **QueueRow** - Queued sermon display with error states
- **APIStatusCard** - External API connection status

### 4. Page Enhancements

#### Home Dashboard
- Uses `TitleBlock` for consistent sermon display
- Shows "Index Ready" count instead of generic embeddings
- Ministry-focused search placeholder

#### Ask (Search)
- Displays `IndexStatus` badge
- Enhanced `RAGAnswerCard` with AI indicator
- `SourceResultRow` components with relevance scores
- `IndexNudge` for partial index warnings
- Better empty states

#### Library (Repository)
- Enhanced table with `TitleBlock` components
- Shows insight counts (takeaways, quotes)
- Collapsible path disclosure
- Better artifact pills (Transcript, Audio, Indexed)
- Compact density mode

#### Pipeline
- `PipelineBanner` with progress information
- `APIStatusCard` for YouTube API status
- Detailed `StageStep` indicators
- Enhanced `QueueRow` components
- Better error states

#### Sermon Detail
- Breadcrumb navigation (Home → Library → Sermon)
- `MetadataChips` for rich metadata display
- `SectionCard` wrappers for consistency
- `TakeawayItem` components with numbering
- `QuoteCallout` components with gold highlighting
- `TranscriptPanel` with collapse/expand
- `WatchLink` for YouTube

### 5. Navigation Updates
- Updated labels: "Ask" and "Library"
- Added ministry name display in header
- Better active state indication

## Component Usage Examples

### TitleBlock
```tsx
<TitleBlock
  title="The Power of Faith"
  hasSpeaker
  speakerName="Pastor John Smith"
  hasSeries
  seriesName="Faith in Action"
  hasDate
  date="April 13, 2026"
  density="comfortable" // or "compact"
/>
```

### IndexStatus
```tsx
<IndexStatus status="ready" count={38} />
<IndexStatus status="partial" count={4} />
```

### StageStep
```tsx
<StageStep
  name="Extract Audio"
  state="active" // pending | active | done | error
  icon={FileAudio}
/>
```

## File Structure

```
/src/app/
├── components/
│   ├── chrome/          # App shell, navigation
│   ├── layout/          # Page containers, headers, sections
│   ├── sermon/          # Sermon-specific components
│   ├── intel/           # Search intelligence components
│   ├── ops/             # Pipeline operation components
│   ├── data/            # Generic data display (StatTile, Pill, etc.)
│   └── ui/              # Base UI primitives (shadcn)
├── pages/
│   ├── Home.tsx
│   ├── Search.tsx       # "Ask" functionality
│   ├── Repository.tsx   # "Library" functionality
│   ├── Pipeline.tsx
│   └── SermonDetail.tsx
└── routes.tsx
```

## Design System Alignment

All components follow the Figma specification with:
- Consistent spacing (8pt system)
- Semantic color usage
- Typography hierarchy
- State variants (default/hover/active/disabled)
- Intent variants (success/warning/danger/info)
- Density modes where applicable

## Future Enhancements (Later)

As noted in the specification, these features are planned:
- Scripture chips and references
- Timestamp links in search results
- Mobile/tablet responsive layouts
- Advanced operations (pause/retry)
- Density toggle controls
