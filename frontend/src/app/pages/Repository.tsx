import { useEffect, useState } from 'react';
import { Link } from 'react-router';
import { PageContainer } from '../components/layout/PageContainer';
import { PageHeader } from '../components/layout/PageHeader';
import { Section } from '../components/layout/Section';
import { StatTile } from '../components/data/StatTile';
import { Pill } from '../components/data/Pill';
import { TitleBlock } from '../components/sermon/TitleBlock';
import { Card } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '../components/ui/table';
import { FileText, FileAudio, Database as DatabaseIcon, Folder, ChevronDown, ChevronUp } from 'lucide-react';
import { getRepository, getStats } from '../../api/endpoints';
import { ApiError } from '../../api/client';
import type { RepositoryInsightFile, StatsResponse } from '../../api/types';

function formatDate(iso: string) {
  if (!iso) return '—';
  const d = new Date(iso);
  if (Number.isNaN(d.getTime())) return iso.slice(0, 10);
  return d.toISOString().slice(0, 10);
}

export function Repository() {
  const [showAdvanced, setShowAdvanced] = useState(false);
  const [rows, setRows] = useState<RepositoryInsightFile[]>([]);
  const [stats, setStats] = useState<StatsResponse | null>(null);
  const [insightsPath, setInsightsPath] = useState('');
  const [loadError, setLoadError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    (async () => {
      try {
        const [repo, s] = await Promise.all([getRepository(), getStats()]);
        if (cancelled) return;
        setRows(repo.insight_files);
        setInsightsPath(repo.insights_dir);
        setStats(s);
        setLoadError(null);
      } catch (e) {
        if (cancelled) return;
        setLoadError(
          e instanceof ApiError
            ? e.message
            : 'Could not load repository. Run Flask on port 8025 (or set VITE_API_PROXY) with Vite dev server.'
        );
        setRows([]);
        setStats(null);
      }
    })();
    return () => {
      cancelled = true;
    };
  }, []);

  const total = stats?.total_videos ?? rows.length;
  const withAudio = rows.filter((r) => r.has_audio).length;
  const withTranscript = rows.filter((r) => r.has_transcript).length;
  const indexed = stats?.embeddings_indexed_count ?? rows.filter((r) => r.has_embeddings).length;

  return (
    <PageContainer>
      <PageHeader
        title="Sermon Library"
        description="Transcripts in data/raw_transcripts, wiki pages, and embedding index status"
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
            icon={FileText}
            iconColor="var(--brand-primary)"
          />
          <StatTile
            label="Audio Files"
            value={loadError ? '—' : withAudio}
            icon={FileAudio}
            iconColor="var(--success)"
          />
          <StatTile
            label="Transcripts"
            value={loadError ? '—' : withTranscript}
            icon={FileText}
            iconColor="var(--info)"
          />
          <StatTile
            label="Index Ready"
            value={loadError ? '—' : indexed}
            icon={DatabaseIcon}
            iconColor="var(--index-ready)"
          />
        </div>
      </Section>

      <Section spacing="hi">
        <Card>
          <button
            onClick={() => setShowAdvanced(!showAdvanced)}
            className="w-full p-4 flex items-center justify-between text-left hover:bg-gray-50 transition-colors"
          >
            <div className="flex items-center gap-3">
              <Folder className="w-5 h-5 text-[var(--text-tertiary)]" />
              <span className="text-sm font-medium text-[var(--text-primary)]">Repository Path</span>
            </div>
            {showAdvanced ? (
              <ChevronUp className="w-4 h-4 text-[var(--text-tertiary)]" />
            ) : (
              <ChevronDown className="w-4 h-4 text-[var(--text-tertiary)]" />
            )}
          </button>

          {showAdvanced && (
            <div className="p-4 border-t border-[var(--border-default)]">
              <code className="text-xs text-[var(--text-secondary)] bg-gray-50 px-2 py-1 rounded font-mono block break-all">
                {insightsPath || '—'}
              </code>
            </div>
          )}
        </Card>
      </Section>

      <Section title="Sermon Artifacts">
        <Card>
          <div className="overflow-x-auto">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Sermon</TableHead>
                  <TableHead>Insights</TableHead>
                  <TableHead className="text-center">Artifacts</TableHead>
                  <TableHead className="text-right">Actions</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {!loadError && rows.length === 0 && (
                  <TableRow>
                    <TableCell colSpan={4} className="text-sm text-[var(--text-secondary)] text-center py-8">
                      No insight files found.
                    </TableCell>
                  </TableRow>
                )}
                {rows.map((row) => {
                  const speaker = row.channel_title?.trim();
                  return (
                    <TableRow key={row.video_id}>
                      <TableCell>
                        <TitleBlock
                          title={row.title}
                          hasSpeaker={!!speaker}
                          speakerName={speaker}
                          hasDate={!!row.published_at}
                          date={row.published_at ? formatDate(row.published_at) : undefined}
                          density="compact"
                        />
                        <p className="text-xs text-[var(--text-tertiary)] font-mono mt-1">{row.video_id}</p>
                      </TableCell>
                      <TableCell className="text-sm text-[var(--text-secondary)]">
                        {row.insights_count > 0 && <div>{row.insights_count} takeaways</div>}
                        {row.nuggets_count > 0 && <div>{row.nuggets_count} quotes</div>}
                        {row.insights_count === 0 && row.nuggets_count === 0 && (
                          <span className="text-[var(--text-tertiary)]">—</span>
                        )}
                      </TableCell>
                      <TableCell>
                        <div className="flex flex-wrap gap-1.5 justify-center">
                          {row.has_transcript && <Pill type="transcript">Transcript</Pill>}
                          {row.has_audio && <Pill type="audio">Audio</Pill>}
                          {row.has_embeddings === true && <Pill type="embeddings">Indexed</Pill>}
                          {row.has_transcript && !row.has_embeddings && (
                            <span className="text-xs text-[var(--processing)]">Not indexed</span>
                          )}
                        </div>
                      </TableCell>
                      <TableCell className="text-right">
                        <div className="flex items-center justify-end gap-2">
                          <Button variant="ghost" size="sm" asChild>
                            <Link to={`/video/${row.video_id}`}>Open</Link>
                          </Button>
                        </div>
                      </TableCell>
                    </TableRow>
                  );
                })}
              </TableBody>
            </Table>
          </div>
        </Card>
      </Section>
    </PageContainer>
  );
}
