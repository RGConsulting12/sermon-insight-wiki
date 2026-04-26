import { ExternalLink } from 'lucide-react';

interface WatchLinkProps {
  url: string;
  label?: string;
  state?: 'default' | 'hover';
}

export function WatchLink({ url, label = 'Watch on YouTube', state = 'default' }: WatchLinkProps) {
  return (
    <a
      href={url}
      target="_blank"
      rel="noopener noreferrer"
      className="inline-flex items-center gap-2 text-[var(--source)] hover:underline font-medium transition-colors"
    >
      {label}
      <ExternalLink className="w-4 h-4" />
    </a>
  );
}
