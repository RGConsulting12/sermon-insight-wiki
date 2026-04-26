import { Card } from '../ui/card';
import { SearchX } from 'lucide-react';

export function SearchNoResults() {
  return (
    <Card className="p-12 text-center">
      <SearchX className="w-12 h-12 mx-auto mb-3 text-[var(--text-tertiary)]" />
      <p className="text-[var(--text-secondary)]">No results found</p>
      <p className="text-sm text-[var(--text-tertiary)] mt-1">
        Try rephrasing your question or using different keywords
      </p>
    </Card>
  );
}
