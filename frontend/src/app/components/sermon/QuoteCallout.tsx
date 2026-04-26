import { Card } from '../ui/card';

interface QuoteCalloutProps {
  children: string;
  style?: 'gold' | 'neutral';
}

export function QuoteCallout({ children, style = 'gold' }: QuoteCalloutProps) {
  const borderColor = style === 'gold' ? 'var(--warning)' : 'var(--border-default)';
  const bgColor = style === 'gold' ? 'var(--warning-surface)' : 'var(--surface)';

  return (
    <Card 
      className="p-6 border-l-4"
      style={{ 
        borderLeftColor: borderColor,
        backgroundColor: bgColor 
      }}
    >
      <p className="italic text-[var(--text-primary)] leading-relaxed text-lg">
        "{children}"
      </p>
    </Card>
  );
}
