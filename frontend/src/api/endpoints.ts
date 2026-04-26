import { getJson, postJson } from './client';
import type {
  RepositoryResponse,
  StatsResponse,
  TitleInfo,
  VideoDetailResponse,
  VideoListItem,
  WikiQueryResponse,
} from './types';

export function getStats(): Promise<StatsResponse> {
  return getJson<StatsResponse>('/api/stats');
}

export function getVideoList(): Promise<VideoListItem[]> {
  return getJson<VideoListItem[]>('/api/videos');
}

export function getVideoDetail(videoId: string): Promise<VideoDetailResponse> {
  return getJson<VideoDetailResponse>(`/api/video/${encodeURIComponent(videoId)}`);
}

export function getVideoTitleInfo(videoId: string): Promise<TitleInfo> {
  return getJson<TitleInfo>(`/api/video/${encodeURIComponent(videoId)}/title`);
}

export function putVideoTitleOverride(videoId: string, title: string): Promise<TitleInfo> {
  return getJson<TitleInfo>(`/api/video/${encodeURIComponent(videoId)}/title`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ title }),
  });
}

export function deleteVideoTitleOverride(videoId: string): Promise<TitleInfo> {
  return getJson<TitleInfo>(`/api/video/${encodeURIComponent(videoId)}/title`, {
    method: 'DELETE',
  });
}

export function postExtractSermonTheme(
  videoId: string
): Promise<TitleInfo & { ok: boolean; theme: string | null }> {
  return getJson(
    `/api/video/${encodeURIComponent(videoId)}/title/extract-theme`,
    { method: 'POST' }
  ) as Promise<TitleInfo & { ok: boolean; theme: string | null }>;
}

export function getRepository(): Promise<RepositoryResponse> {
  return getJson<RepositoryResponse>('/api/repository');
}

export function postWikiQuery(
  question: string,
  topK = 10
): Promise<WikiQueryResponse> {
  return postJson<WikiQueryResponse>('/api/query', { question, top_k: topK });
}
