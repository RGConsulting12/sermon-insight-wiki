import { Card } from '../ui/card';
import { Search } from 'lucide-react';

export function SearchEmpty() {
  return (
    <Card className="p-12 text-center">
      <Search className="w-12 h-12 mx-auto mb-3 text-[var(--text-tertiary)]" />
      <p className="text-[var(--text-secondary)]">Enter a question to search across all sermons</p>
      <p className="text-sm text-[var(--text-tertiary)] mt-1">
        Ask ministry questions or search for biblical topics
      </p>
    </Card>
  );
}
