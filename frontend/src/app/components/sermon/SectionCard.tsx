import { ReactNode } from 'react';
import { Card } from '../ui/card';

interface SectionCardProps {
  title?: string;
  children: ReactNode;
  elevation?: 'flat' | 'elevated';
}

export function SectionCard({ title, children, elevation = 'flat' }: SectionCardProps) {
  return (
    <Card className={elevation === 'elevated' ? 'shadow-md' : ''}>
      <div className="p-6">
        {title && (
          <h2 className="text-[var(--text-primary)] mb-4">{title}</h2>
        )}
        {children}
      </div>
    </Card>
  );
}
