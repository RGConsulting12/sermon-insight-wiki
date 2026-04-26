import { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router';
import { PageContainer } from '../components/layout/PageContainer';
import { Section } from '../components/layout/Section';
import { Breadcrumb } from '../components/layout/Breadcrumb';
import { MetadataChips } from '../components/sermon/MetadataChips';
import { SectionCard } from '../components/sermon/SectionCard';
import { TakeawayItem } from '../components/sermon/TakeawayItem';
import { QuoteCallout } from '../components/sermon/QuoteCallout';
import { TranscriptPanel } from '../components/sermon/TranscriptPanel';
import { WatchLink } from '../components/sermon/WatchLink';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { ArrowLeft, Loader2 } from 'lucide-react';
import {
  getVideoDetail,
  putVideoTitleOverride,
  deleteVideoTitleOverride,
  postExtractSermonTheme,
} from '../../api/endpoints';
import { ApiError } from '../../api/client';
import type { TitleInfo, VideoDetailResponse } from '../../api/types';

function formatDate(iso: string | undefined) {
  if (!iso) return undefined;
  const d = new Date(iso);
  if (Number.isNaN(d.getTime())) return iso.slice(0, 10);
  return d.toLocaleDateString(undefined, {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  });
}

const sourceLabel: Record<TitleInfo['source'], string> = {
  user: 'Your custom title',
  llm: 'AI-extracted theme',
  youtube: 'YouTube title',
};

export function SermonDetail() {
  const { id: videoId = '' } = useParams<{ id: string }>();
  const [data, setData] = useState<VideoDetailResponse | null>(null);
  const [err, setErr] = useState<string | null>(null);
  const [titleDraft, setTitleDraft] = useState('');
  const [saving, setSaving] = useState(false);
  const [extracting, setExtracting] = useState(false);

  const load = () => {
    if (!videoId) return;
    getVideoDetail(videoId)
      .then((d) => {
        setData(d);
        setTitleDraft(d.title_info.display_title);
        setErr(null);
      })
      .catch((e) => {
        setData(null);
        setErr(
          e instanceof ApiError
            ? e.message
            : 'Failed to load sermon. Is the API running?'
        );
      });
  };

  useEffect(() => {
    load();
  }, [videoId]);

  const ti = data?.title_info;
  const applyTitleInfo = (t: TitleInfo) => {
    if (!data) return;
    setData({
      ...data,
      title_info: t,
      metadata: { ...data.metadata, title: t.display_title },
    });
    setTitleDraft(t.display_title);
  };

  const onSaveTitle = async () => {
    if (!videoId) return;
    setSaving(true);
    try {
      const t = await putVideoTitleOverride(videoId, titleDraft);
      applyTitleInfo(t);
    } catch (e) {
      setErr(e instanceof ApiError ? e.message : 'Save failed');
    } finally {
      setSaving(false);
    }
  };

  const onClearOverride = async () => {
    if (!videoId) return;
    setSaving(true);
    try {
      const t = await deleteVideoTitleOverride(videoId);
      applyTitleInfo(t);
    } catch (e) {
      setErr(e instanceof ApiError ? e.message : 'Reset failed');
    } finally {
      setSaving(false);
    }
  };

  const onExtract = async () => {
    if (!videoId) return;
    setExtracting(true);
    setErr(null);
    try {
      const res = await postExtractSermonTheme(videoId);
      applyTitleInfo({
        display_title: res.display_title,
        source: res.source,
        youtube_title: res.youtube_title,
        user_title: res.user_title,
        llm_theme: res.llm_theme,
        user_updated_at: res.user_updated_at,
        llm_extracted_at: res.llm_extracted_at,
      });
    } catch (e) {
      setErr(e instanceof ApiError ? e.message : 'Extraction failed');
    } finally {
      setExtracting(false);
    }
  };

  if (!videoId) {
    return <p className="p-6 text-sm text-[var(--text-secondary)]">Missing video id.</p>;
  }

  if (err && !data) {
    return (
      <PageContainer>
        <p className="text-sm text-red-700 bg-red-50 border border-red-200 rounded-md px-3 py-2">{err}</p>
        <Link to="/" className="text-sm text-[var(--brand-primary)] mt-4 inline-block">Back to home</Link>
      </PageContainer>
    );
  }

  if (!data || !ti) {
    return (
      <PageContainer>
        <div className="flex items-center gap-2 text-[var(--text-secondary)] p-6">
          <Loader2 className="w-5 h-5 animate-spin" />
          Loading…
        </div>
      </PageContainer>
    );
  }

  const youtubeUrl = `https://www.youtube.com/watch?v=${videoId}`;
  const dateLabel = formatDate(data.metadata.published_at);
  const speaker = data.metadata.channel_title?.trim();

  return (
    <PageContainer>
      <Breadcrumb
        items={[
          { label: 'Home', path: '/' },
          { label: 'Library', path: '/repository' },
          { label: data.title_info.display_title },
        ]}
      />

      <div className="mb-6">
        <Link to="/">
          <Button variant="ghost" className="gap-2">
            <ArrowLeft className="w-4 h-4" />
            Back to Home
          </Button>
        </Link>
      </div>

      <Section spacing="hi">
        <SectionCard>
          <div className="space-y-4">
            <h1 className="text-[var(--text-primary)]">{data.title_info.display_title}</h1>
            <p className="text-xs text-[var(--text-tertiary)]">{sourceLabel[data.title_info.source]}</p>

            <div className="border border-[var(--border-default)] rounded-md p-4 space-y-3 bg-[var(--background)]/50">
              <p className="text-sm font-medium text-[var(--text-primary)]">Edit display title</p>
              <p className="text-xs text-[var(--text-secondary)]">
                Shown in lists and on this page. YouTube: <span className="font-mono text-[var(--text-tertiary)]">{data.title_info.youtube_title}</span>
                {data.title_info.llm_theme && (
                  <span className="block mt-1">Last AI theme: {data.title_info.llm_theme}</span>
                )}
              </p>
              <div className="flex flex-col sm:flex-row gap-2 sm:items-center">
                <Input
                  value={titleDraft}
                  onChange={(e) => setTitleDraft(e.target.value)}
                  className="max-w-xl"
                  placeholder="Sermon title"
                />
                <Button type="button" onClick={onSaveTitle} disabled={saving || titleDraft === data.title_info.display_title}>
                  {saving ? 'Saving…' : 'Save title'}
                </Button>
                <Button type="button" variant="outline" onClick={onClearOverride} disabled={saving || !data.title_info.user_title}>
                  Clear your override
                </Button>
                <Button
                  type="button"
                  variant="secondary"
                  onClick={onExtract}
                  disabled={extracting}
                >
                  {extracting ? 'Extracting…' : 'Re-extract theme (AI)'}
                </Button>
              </div>
            </div>

            {err && <p className="text-sm text-amber-800">{err}</p>}

            <MetadataChips
              date={dateLabel}
              speaker={speaker}
              series={undefined}
              campus={undefined}
            />

            <WatchLink url={youtubeUrl} />

            {data.metadata.description && (
              <p className="text-[var(--text-secondary)] leading-relaxed whitespace-pre-line">
                {String(data.metadata.description).slice(0, 2000)}
                {String(data.metadata.description).length > 2000 ? '…' : ''}
              </p>
            )}
          </div>
        </SectionCard>
      </Section>

      <Section spacing="hi">
        <SectionCard title="Summary">
          <p className="text-[var(--text-primary)] leading-relaxed">
            {data.insights.summary || '—'}
          </p>
        </SectionCard>
      </Section>

      <Section spacing="hi">
        <SectionCard title="Key takeaways">
          <div className="space-y-4">
            {(data.insights.insights || []).map((t, index) => (
              <TakeawayItem key={index} number={index + 1}>
                {t}
              </TakeawayItem>
            ))}
            {(!data.insights.insights || data.insights.insights.length === 0) && (
              <p className="text-sm text-[var(--text-tertiary)]">—</p>
            )}
          </div>
        </SectionCard>
      </Section>

      <Section title="Quotable lines" spacing="hi">
        <div className="space-y-3">
          {(data.insights.golden_nuggets || []).map((q, index) => (
            <QuoteCallout key={index} style="gold">
              {q}
            </QuoteCallout>
          ))}
          {(!data.insights.golden_nuggets || data.insights.golden_nuggets.length === 0) && (
            <p className="text-sm text-[var(--text-tertiary)]">—</p>
          )}
        </div>
      </Section>

      <Section title="Full transcript">
        <TranscriptPanel transcript={data.transcript || ''} />
      </Section>
    </PageContainer>
  );
}
