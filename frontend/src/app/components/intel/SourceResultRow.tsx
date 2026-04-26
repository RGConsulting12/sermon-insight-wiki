import { Card } from '../ui/card';
import { ExternalLink } from 'lucide-react';
import { Link } from 'react-router';

interface SourceResultRowProps {
  sermonTitle: string;
  excerpt: string;
  videoId: string;
  mode?: 'semantic' | 'keyword';
  relevance?: number;
  timestamp?: string;
  date?: string;
  keywords?: string[];
}

export function SourceResultRow({ 
  sermonTitle, 
  excerpt, 
  videoId,
  mode = 'semantic',
  relevance,
  timestamp,
  date,
  keywords = []
}: SourceResultRowProps) {
  return (
    <Card className="p-4 hover:shadow-md transition-shadow">
      <div className="flex items-start justify-between mb-3">
        <div className="flex-1">
          <h3 className="font-medium text-[var(--text-primary)] mb-1">
            {sermonTitle}
          </h3>
          <div className="flex flex-wrap items-center gap-2 text-sm text-[var(--text-secondary)]">
            {timestamp && (
              <span className="px-2 py-0.5 bg-gray-100 rounded text-xs font-mono">
                {timestamp}
              </span>
            )}
            {date && <span>{date}</span>}
            <Link 
              to={`/video/${videoId}`}
              className="flex items-center gap-1 text-[var(--brand-primary)] hover:underline"
            >
              View sermon
              <ExternalLink className="w-3 h-3" />
            </Link>
          </div>
        </div>
        {mode === 'semantic' && relevance !== undefined && (
          <div className="ml-4 flex-shrink-0">
            <div className="px-2 py-1 bg-[var(--info-surface)] text-[var(--info)] rounded text-sm font-medium">
              {Math.round(relevance * 100)}% match
            </div>
          </div>
        )}
      </div>
      
      <p className="text-[var(--text-secondary)] leading-relaxed mb-2">
        {excerpt}
      </p>

      {mode === 'keyword' && keywords.length > 0 && (
        <div className="flex flex-wrap gap-1.5 mt-3">
          {keywords.map((keyword, index) => (
            <span 
              key={index}
              className="px-2 py-0.5 bg-[var(--brand-primary)]/10 text-[var(--brand-primary)] rounded text-xs font-medium"
            >
              {keyword}
            </span>
          ))}
        </div>
      )}
    </Card>
  );
}
