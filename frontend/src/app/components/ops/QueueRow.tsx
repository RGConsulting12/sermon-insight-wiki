import { Youtube, ExternalLink, AlertCircle } from 'lucide-react';

interface QueueRowProps {
  id: string;
  url: string;
  title?: string;
  hasError?: boolean;
  errorMessage?: string;
}

export function QueueRow({ id, url, title, hasError, errorMessage }: QueueRowProps) {
  return (
    <div className={`p-4 border-b last:border-b-0 ${hasError ? 'bg-[var(--danger-surface)]' : ''}`}>
      <div className="flex items-start gap-3">
        <Youtube className={`w-5 h-5 mt-0.5 ${hasError ? 'text-[var(--danger)]' : 'text-red-600'}`} />
        <div className="flex-1 min-w-0">
          <p className="font-medium text-[var(--text-primary)] mb-1">
            {title || `Sermon ${id}`}
          </p>
          <a 
            href={url}
            target="_blank"
            rel="noopener noreferrer"
            className="text-sm text-[var(--brand-primary)] hover:underline flex items-center gap-1 break-all"
          >
            {url}
            <ExternalLink className="w-3 h-3 flex-shrink-0" />
          </a>
          {hasError && errorMessage && (
            <div className="flex items-start gap-2 mt-2 text-sm text-[var(--danger)]">
              <AlertCircle className="w-4 h-4 flex-shrink-0 mt-0.5" />
              <span>{errorMessage}</span>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
