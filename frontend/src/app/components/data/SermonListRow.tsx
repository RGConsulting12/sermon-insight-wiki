import { Link } from 'react-router';
import { ChevronRight } from 'lucide-react';

interface SermonListRowProps {
  id: string;
  title: string;
  date: string;
  duration?: string;
  density?: 'comfortable' | 'compact';
  showChevron?: boolean;
}

export function SermonListRow({ 
  id, 
  title, 
  date, 
  duration,
  density = 'comfortable',
  showChevron = true 
}: SermonListRowProps) {
  const padding = density === 'comfortable' ? 'p-4' : 'p-3';
  
  return (
    <Link
      to={`/video/${id}`}
      className={`
        ${padding} flex items-center justify-between
        bg-[var(--surface)] border border-[var(--border-default)] rounded-lg
        hover:border-[var(--brand-primary)] hover:shadow-sm
        transition-all group
      `}
    >
      <div className="flex-1 min-w-0">
        <h3 className="font-medium text-[var(--text-primary)] mb-1 group-hover:text-[var(--brand-primary)] transition-colors">
          {title}
        </h3>
        <div className="flex items-center gap-3 text-sm text-[var(--text-secondary)]">
          <span>{date}</span>
          {duration && (
            <>
              <span>•</span>
              <span>{duration}</span>
            </>
          )}
        </div>
      </div>
      {showChevron && (
        <ChevronRight className="w-5 h-5 text-[var(--text-tertiary)] group-hover:text-[var(--brand-primary)] transition-colors flex-shrink-0 ml-4" />
      )}
    </Link>
  );
}
