import { Link } from 'react-router';
import { ChevronRight } from 'lucide-react';

interface BreadcrumbItem {
  label: string;
  path?: string;
}

interface BreadcrumbProps {
  items: BreadcrumbItem[];
}

export function Breadcrumb({ items }: BreadcrumbProps) {
  return (
    <nav className="flex items-center gap-2 text-sm text-[var(--text-secondary)] mb-6">
      {items.map((item, index) => {
        const isLast = index === items.length - 1;
        
        return (
          <div key={index} className="flex items-center gap-2">
            {item.path && !isLast ? (
              <Link to={item.path} className="hover:text-[var(--brand-primary)] transition-colors">
                {item.label}
              </Link>
            ) : (
              <span className={isLast ? 'text-[var(--text-primary)] truncate' : ''}>
                {item.label}
              </span>
            )}
            {!isLast && <ChevronRight className="w-4 h-4 flex-shrink-0" />}
          </div>
        );
      })}
    </nav>
  );
}
