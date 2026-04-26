import { Link } from 'react-router';
import { AlertTriangle } from 'lucide-react';

interface IndexNudgeProps {
  missingCount: number;
}

export function IndexNudge({ missingCount }: IndexNudgeProps) {
  return (
    <div 
      className="p-4 rounded-lg border flex items-start gap-3"
      style={{ 
        backgroundColor: 'var(--index-missing-surface)',
        borderColor: 'var(--index-missing)',
      }}
    >
      <AlertTriangle className="w-5 h-5 flex-shrink-0 mt-0.5" style={{ color: 'var(--index-missing)' }} />
      <div className="flex-1" style={{ color: 'var(--index-missing)' }}>
        <p className="font-medium mb-1">
          {missingCount} sermon{missingCount !== 1 ? 's' : ''} not yet indexed
        </p>
        <p className="text-sm">
          Visit the{' '}
          <Link to="/repository" className="underline font-medium">
            Library
          </Link>
          {' '}to generate embeddings for better search results.
        </p>
      </div>
    </div>
  );
}
