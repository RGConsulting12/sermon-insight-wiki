/**
 * DTOs aligned with Flask JSON responses (Phase 1).
 */

export interface CostSummary {
  [key: string]: unknown;
}

/** GET /api/videos (DataLoader.get_all_videos) */
export interface VideoListItem {
  video_id: string;
  title: string;
  title_source?: 'user' | 'llm' | 'youtube';
  youtube_title?: string;
  llm_theme?: string | null;
  user_title?: string | null;
  summary: string;
  insights_count: number;
  nuggets_count: number;
  published_at: string;
  transcript_length: number;
  metadata: {
    title?: string;
    description?: string;
    published_at?: string;
    channel_title?: string;
    tags?: string[];
  };
}

export interface TitleInfo {
  display_title: string;
  source: 'user' | 'llm' | 'youtube';
  youtube_title: string;
  user_title: string | null;
  llm_theme: string | null;
  user_updated_at: string | null;
  llm_extracted_at: string | null;
}

export interface InsightsPayload {
  summary: string;
  insights: string[];
  golden_nuggets: string[];
  video_id?: string;
}

export interface VideoDetailResponse {
  video_id: string;
  insights: InsightsPayload;
  metadata: {
    title?: string;
    description?: string;
    published_at?: string;
    channel_title?: string;
    tags?: string[];
  };
  transcript: string | null;
  title_info: TitleInfo;
}

/** GET /api/stats */
export interface StatsResponse {
  total_videos: number;
  total_insights: number;
  total_nuggets: number;
  total_transcript_length: number;
  avg_insights_per_video: number;
  avg_nuggets_per_video: number;
  cost_data: CostSummary;
  embeddings_indexed_count: number;
}

/** One row in GET /api/repository → insight_files */
export interface RepositoryInsightFile {
  video_id: string;
  /** From YouTube metadata (per-file or all_metadata.json). */
  title: string;
  published_at?: string;
  channel_title?: string;
  filename: string;
  path: string;
  size: number;
  created: string;
  modified: string;
  insights_count: number;
  nuggets_count: number;
  has_transcript: boolean;
  transcript_size: number;
  has_chunks: boolean;
  chunk_count: number;
  has_chunk_transcripts?: boolean;
  has_audio: boolean;
  audio_size: number;
  has_embeddings: boolean;
}

/** GET /api/repository */
export interface RepositoryResponse {
  insight_files: RepositoryInsightFile[];
  insights_dir: string;
  total_size: number;
  total_transcripts_size: number;
  total_audio_size: number;
}

/** POST /api/query (sermon-insight-wiki hybrid RAG + scripture) */
export interface WikiRetrievalHit {
  video_id: string;
  chunk_index: number;
  evidence_id: string;
  text: string;
  similarity: number;
  rrf_score?: number;
  expansion?: string;
}

export interface WikiQueryResponse {
  answer_markdown: string;
  absence_markdown: string;
  counterfactual_markdown: string;
  blocking_analysis: string;
  retrieval: WikiRetrievalHit[];
  absence_report: Record<string, unknown>;
  scripture?: {
    refs: unknown[];
    context_included: boolean;
  };
}
