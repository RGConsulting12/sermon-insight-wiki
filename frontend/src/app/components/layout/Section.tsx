import { ReactNode } from 'react';

interface SectionProps {
  title?: string;
  children: ReactNode;
  spacing?: 'lo' | 'hi';
  className?: string;
}

export function Section({ title, children, spacing = 'lo', className = '' }: SectionProps) {
  const spacingClass = spacing === 'lo' ? 'mb-6' : 'mb-8';
  
  return (
    <div className={`${spacingClass} ${className}`}>
      {title && <h2 className="text-[var(--text-primary)] mb-4">{title}</h2>}
      {children}
    </div>
  );
}
