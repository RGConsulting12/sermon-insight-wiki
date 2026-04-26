import { useState } from 'react';
import { PageContainer } from '../components/layout/PageContainer';
import { PageHeader } from '../components/layout/PageHeader';
import { Section } from '../components/layout/Section';
import { InlineHelp } from '../components/data/InlineHelp';
import { PipelineBanner } from '../components/ops/PipelineBanner';
import { StageStep } from '../components/ops/StageStep';
import { QueueRow } from '../components/ops/QueueRow';
import { APIStatusCard } from '../components/ops/APIStatusCard';
import { Card } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { Textarea } from '../components/ui/textarea';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../components/ui/tabs';
import { Progress } from '../components/ui/progress';
import { Link } from 'react-router';
import { 
  Download, 
  FileAudio, 
  FileText, 
  Database, 
  Youtube
} from 'lucide-react';

interface QueuedSermon {
  id: string;
  url: string;
  title: string;
}

interface ProcessingStage {
  name: string;
  state: 'pending' | 'active' | 'done' | 'error';
  icon: any;
}

const stages: ProcessingStage[] = [
  { name: 'Download Video', state: 'done', icon: Download },
  { name: 'Extract Audio', state: 'active', icon: FileAudio },
  { name: 'Generate Transcript', state: 'pending', icon: FileText },
  { name: 'Create Embeddings', state: 'pending', icon: Database },
];

export function Pipeline() {
  const [inputMode, setInputMode] = useState<'individual' | 'playlist'>('individual');
  const [individualUrl, setIndividualUrl] = useState('');
  const [playlistUrls, setPlaylistUrls] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [queuedSermons, setQueuedSermons] = useState<QueuedSermon[]>([
    { id: '1', url: 'https://youtube.com/watch?v=abc123', title: 'Sermon on Faith' },
    { id: '2', url: 'https://youtube.com/watch?v=def456', title: 'Sermon on Hope' },
  ]);

  const handleAddToQueue = () => {
    if (inputMode === 'individual' && individualUrl) {
      setQueuedSermons([...queuedSermons, {
        id: Date.now().toString(),
        url: individualUrl,
        title: `Sermon ${queuedSermons.length + 1}`,
      }]);
      setIndividualUrl('');
    }
  };

  const handleStartProcessing = () => {
    setIsProcessing(true);
  };

  return (
    <PageContainer>
      <PageHeader 
        title="Pipeline"
        description="Add and process sermon videos from YouTube"
      />

      <Section spacing="hi">
        <PipelineBanner 
          status={isProcessing ? 'running' : 'idle'}
          currentItem={isProcessing ? 'Sermon on Faith' : undefined}
          currentIndex={isProcessing ? 2 : undefined}
          totalItems={isProcessing ? 4 : undefined}
        />
      </Section>

      <Section spacing="hi">
        <APIStatusCard 
          status="ok"
          serviceName="YouTube Data API v3"
        />
      </Section>

      <Section title="Add Sermons">
        <Card className="p-6">
          <Tabs value={inputMode} onValueChange={(v) => setInputMode(v as any)}>
            <TabsList className="mb-4">
              <TabsTrigger value="individual">Individual Video</TabsTrigger>
              <TabsTrigger value="playlist">Bulk Import</TabsTrigger>
            </TabsList>

            <TabsContent value="individual" className="space-y-4">
              <div className="space-y-2">
                <label className="text-sm font-medium">YouTube Video URL</label>
                <div className="flex gap-2">
                  <Input 
                    value={individualUrl}
                    onChange={(e) => setIndividualUrl(e.target.value)}
                    placeholder="https://www.youtube.com/watch?v=..."
                  />
                  <Button onClick={handleAddToQueue} disabled={!individualUrl}>
                    Add to Queue
                  </Button>
                </div>
              </div>
            </TabsContent>

            <TabsContent value="playlist" className="space-y-4">
              <div className="space-y-2">
                <label className="text-sm font-medium">YouTube URLs (one per line)</label>
                <Textarea 
                  value={playlistUrls}
                  onChange={(e) => setPlaylistUrls(e.target.value)}
                  placeholder="https://www.youtube.com/watch?v=abc123&#10;https://www.youtube.com/watch?v=def456&#10;https://www.youtube.com/watch?v=ghi789"
                  rows={5}
                />
                <Button disabled={!playlistUrls}>Add All to Queue</Button>
              </div>
            </TabsContent>
          </Tabs>
        </Card>
      </Section>

      {isProcessing && (
        <Section title="Processing Details">
          <Card className="p-6 space-y-6">
            <div>
              <div className="flex items-center justify-between mb-2">
                <span className="text-sm font-medium">Current: Sermon on Faith</span>
                <span className="text-sm text-[var(--text-secondary)]">2 of 4</span>
              </div>
              <Progress value={50} />
            </div>

            <div className="space-y-3">
              {stages.map((stage, index) => (
                <StageStep
                  key={index}
                  name={stage.name}
                  state={stage.state}
                  icon={stage.icon}
                />
              ))}
            </div>
          </Card>
        </Section>
      )}

      <Section title={`Processing Queue (${queuedSermons.length})`}>
        {queuedSermons.length > 0 ? (
          <div className="space-y-3">
            <Card className="divide-y">
              {queuedSermons.map((sermon) => (
                <QueueRow
                  key={sermon.id}
                  id={sermon.id}
                  url={sermon.url}
                  title={sermon.title}
                />
              ))}
            </Card>

            <Button 
              onClick={handleStartProcessing}
              disabled={isProcessing}
              className="w-full"
              size="lg"
            >
              {isProcessing ? 'Processing...' : `Process ${queuedSermons.length} Sermon${queuedSermons.length !== 1 ? 's' : ''}`}
            </Button>
          </div>
        ) : (
          <Card className="p-12 text-center">
            <Youtube className="w-12 h-12 mx-auto mb-3 text-[var(--text-tertiary)]" />
            <p className="text-[var(--text-secondary)]">No sermons in queue</p>
            <p className="text-sm text-[var(--text-tertiary)] mt-1">Add YouTube URLs above to get started</p>
          </Card>
        )}
      </Section>

      <Section>
        <InlineHelp intent="info">
          Once processing is complete, transcripts and embeddings will be available in the{' '}
          <Link to="/repository" className="underline font-medium">Library</Link>.
          Indexed sermons can be searched using the{' '}
          <Link to="/search" className="underline font-medium">Ask</Link> feature.
        </InlineHelp>
      </Section>
    </PageContainer>
  );
}
