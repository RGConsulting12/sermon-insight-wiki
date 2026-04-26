import { useEffect, useState } from 'react';
import { PageContainer } from '../components/layout/PageContainer';
import { PageHeader } from '../components/layout/PageHeader';
import { Section } from '../components/layout/Section';
import { StatTile } from '../components/data/StatTile';
import { TitleBlock } from '../components/sermon/TitleBlock';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { Card } from '../components/ui/card';
import { Link } from 'react-router';
import { Video, FileText, Database, Zap, Search, ChevronRight } from 'lucide-react';
import { getStats, getVideoList } from '../../api/endpoints';
import { ApiError } from '../../api/client';
import type { StatsResponse, VideoListItem } from '../../api/types';

function formatPublished(published: string) {
  if (!published) return '';
  const d = new Date(published);
  if (Number.isNaN(d.getTime())) return published.slice(0, 10);
  return d.toLocaleDateString(undefined, { year: 'numeric', month: 'long', day: 'numeric' });
}

export function Home() {
  const [stats, setStats] = useState<StatsResponse | null>(null);
  const [videos, setVideos] = useState<VideoListItem[]>([]);
  const [loadError, setLoadError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    (async () => {
      try {
        const [s, v] = await Promise.all([getStats(), getVideoList()]);
        if (!cancelled) {
          setStats(s);
          setVideos(v);
          setLoadError(null);
        }
      } catch (e) {
        if (cancelled) return;
        const msg =
          e instanceof ApiError
            ? e.message
            : 'Could not load dashboard. Run Flask (`python -m sermon_insight_wiki.app`, default port 8025) and Vite (`cd frontend && npm run dev`) so /api is proxied.';
        setLoadError(msg);
        setStats(null);
        setVideos([]);
      }
    })();
    return () => {
      cancelled = true;
    };
  }, []);

  const total = stats?.total_videos ?? 0;
  const indexed = stats?.embeddings_indexed_count ?? 0;
  const pendingIndex = Math.max(0, total - indexed);

  return (
    <PageContainer>
      <PageHeader
        title="Dashboard"
        description="Your sermon library at a glance"
        actions={
          <Link to="/pipeline">
            <Button>Add Sermon</Button>
          </Link>
        }
      />

      {loadError && (
        <p className="text-sm text-amber-800 bg-amber-50 border border-amber-200 rounded-md px-3 py-2 mb-4">
          {loadError}
        </p>
      )}

      <Section spacing="hi">
        <div className="grid grid-cols-4 gap-4">
          <StatTile
            label="Total Sermons"
            value={loadError ? '—' : total}
            icon={Video}
            iconColor="var(--brand-primary)"
          />
          <StatTile
            label="Transcripts"
            value={loadError ? '—' : total}
            icon={FileText}
            iconColor="var(--success)"
          />
          <StatTile
            label="Index Ready"
            value={loadError ? '—' : indexed}
            icon={Database}
            iconColor="var(--index-ready)"
          />
          <StatTile
            label="Pending index"
            value={loadError ? '—' : pendingIndex}
            icon={Zap}
            iconColor="var(--processing)"
          />
        </div>
      </Section>

      <Section title="Search Across Sermons" spacing="hi">
        <Card className="p-6">
          <form className="flex gap-2">
            <div className="flex-1 relative">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-[var(--text-tertiary)]" />
              <Input
                placeholder="Ask a ministry question or search for a biblical topic..."
                className="pl-10"
              />
            </div>
            <Link to="/search">
              <Button type="button">Search</Button>
            </Link>
          </form>
        </Card>
      </Section>

      <Section title="Recent Sermons">
        <div className="space-y-3">
          {!loadError && videos.length === 0 && (
            <p className="text-sm text-[var(--text-secondary)]">No processed sermons yet.</p>
          )}
          {videos.slice(0, 8).map((v) => {
            const when = v.published_at || v.metadata?.published_at || '';
            const dateLabel = when ? formatPublished(when) : '—';
            const speaker = v.metadata?.channel_title?.trim() || '—';
            return (
              <Link key={v.video_id} to={`/video/${v.video_id}`} className="block">
                <Card className="p-4 hover:shadow-md hover:border-[var(--brand-primary)] transition-all group">
                  <div className="flex items-center justify-between">
                    <div className="flex-1 min-w-0">
                      <TitleBlock
                        title={v.title}
                        hasSpeaker
                        speakerName={speaker}
                        hasDate
                        date={dateLabel}
                        density="comfortable"
                      />
                    </div>
                    <ChevronRight className="w-5 h-5 text-[var(--text-tertiary)] group-hover:text-[var(--brand-primary)] transition-colors flex-shrink-0 ml-4" />
                  </div>
                </Card>
              </Link>
            );
          })}
        </div>
      </Section>
    </PageContainer>
  );
}
