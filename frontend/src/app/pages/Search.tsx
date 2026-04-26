import { useEffect, useState } from 'react';
import { PageContainer } from '../components/layout/PageContainer';
import { PageHeader } from '../components/layout/PageHeader';
import { Section } from '../components/layout/Section';
import { InlineHelp } from '../components/data/InlineHelp';
import { IndexStatus } from '../components/intel/IndexStatus';
import { RAGAnswerCard } from '../components/intel/RAGAnswerCard';
import { SourceResultRow } from '../components/intel/SourceResultRow';
import { SearchEmpty } from '../components/intel/SearchEmpty';
import { SearchNoResults } from '../components/intel/SearchNoResults';
import { IndexNudge } from '../components/intel/IndexNudge';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { Card } from '../components/ui/card';
import { Search as SearchIcon } from 'lucide-react';
import { postWikiQuery, getStats } from '../../api/endpoints';
import { ApiError } from '../../api/client';
import type { WikiQueryResponse, WikiRetrievalHit, StatsResponse } from '../../api/types';

function formatScore(n: number) {
  if (Number.isNaN(n)) return '—';
  return n.toFixed(3);
}

export function Search() {
  const [query, setQuery] = useState('');
  const [stats, setStats] = useState<StatsResponse | null>(null);
  const [result, setResult] = useState<WikiQueryResponse | null>(null);
  const [isSearching, setIsSearching] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    getStats()
      .then(setStats)
      .catch(() => setStats(null));
  }, []);

  const total = stats?.total_videos ?? 0;
  const indexed = stats?.embeddings_indexed_count ?? 0;
  const pending = Math.max(0, total - indexed);
  const indexStatus: 'ready' | 'partial' | 'none' =
    total === 0 ? 'none' : pending === 0 ? 'ready' : 'partial';

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;
    setIsSearching(true);
    setError(null);
    setResult(null);
    try {
      const res = await postWikiQuery(query.trim(), 12);
      setResult(res);
    } catch (err) {
      setResult(null);
      setError(
        err instanceof ApiError
          ? err.message
          : 'Search failed. Is the Flask API running on the Vite proxy port?'
      );
    } finally {
      setIsSearching(false);
    }
  };

  const rows: WikiRetrievalHit[] = result?.retrieval ?? [];

  return (
    <PageContainer>
      <div className="flex items-start justify-between mb-8">
        <PageHeader
          title="Ask Across Sermons"
          description="Hybrid RAG + wiki + parallel scripture (sermon-insight-wiki backend)"
        />
        <IndexStatus status={indexStatus} count={indexed} />
      </div>

      {pending > 0 && total > 0 && (
        <Section>
          <IndexNudge missingCount={pending} />
        </Section>
      )}

      <Section spacing="hi">
        <form onSubmit={handleSearch} className="space-y-4">
          <div className="flex gap-2">
            <div className="flex-1 relative">
              <SearchIcon className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-[var(--text-tertiary)]" />
              <Input
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="What does the corpus say about grace, forgiveness, or a passage?"
                className="pl-10"
              />
            </div>
            <Button type="submit" disabled={isSearching}>
              {isSearching ? 'Searching…' : 'Search'}
            </Button>
          </div>

          {error && (
            <p className="text-sm text-amber-900 bg-amber-50 border border-amber-200 rounded-md px-3 py-2">
              {error}
            </p>
          )}

          <InlineHelp intent="info">
            <strong>How it works:</strong> Your question is hybrid-retrieved over transcript embeddings, merged
            with wiki context when relevant, and enriched with detected scripture references in multiple
            translations. The model returns an answer, absence notes, and counterfactual blocking analysis.
          </InlineHelp>
        </form>
      </Section>

      {result && rows.length > 0 && (
        <>
          <Section spacing="hi">
            <RAGAnswerCard answer={result.answer_markdown} sourceCount={rows.length} />
          </Section>

          {(result.absence_markdown || result.counterfactual_markdown) && (
            <Section title="Absence & counterfactuals" spacing="hi">
              <Card className="p-4 space-y-4 text-sm text-[var(--text-secondary)] whitespace-pre-wrap">
                {result.absence_markdown ? (
                  <div>
                    <h4 className="font-medium text-[var(--text-primary)] mb-1">Absence reasoning</h4>
                    {result.absence_markdown}
                  </div>
                ) : null}
                {result.counterfactual_markdown ? (
                  <div>
                    <h4 className="font-medium text-[var(--text-primary)] mb-1">Counterfactual / blocking</h4>
                    {result.counterfactual_markdown}
                  </div>
                ) : null}
                {result.blocking_analysis ? (
                  <div>
                    <h4 className="font-medium text-[var(--text-primary)] mb-1">Blocking summary</h4>
                    {result.blocking_analysis}
                  </div>
                ) : null}
              </Card>
            </Section>
          )}

          {result.scripture?.context_included && (
            <Section title="Scripture context" spacing="hi">
              <p className="text-sm text-[var(--text-secondary)]">
                Parallel Bible text was attached for {result.scripture.refs?.length ?? 0} detected reference(s).
              </p>
            </Section>
          )}

          <Section title={`Sources (${rows.length})`}>
            <div className="space-y-3">
              {rows.map((hit, i) => (
                <SourceResultRow
                  key={`${hit.evidence_id}-${i}`}
                  sermonTitle={hit.video_id}
                  excerpt={hit.text.length > 360 ? `${hit.text.slice(0, 360)}…` : hit.text}
                  videoId={hit.video_id}
                  mode="semantic"
                  relevance={hit.rrf_score ?? hit.similarity}
                  timestamp={`chunk ${hit.chunk_index}`}
                  date={`sim ${formatScore(hit.similarity)}`}
                />
              ))}
            </div>
          </Section>
        </>
      )}

      {result && rows.length === 0 && (
        <Section>
          <SearchNoResults />
        </Section>
      )}

      {!result && !isSearching && !error && (
        <Section>
          <SearchEmpty />
        </Section>
      )}
    </PageContainer>
  );
}
