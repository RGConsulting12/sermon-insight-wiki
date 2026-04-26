import { ReactNode } from 'react';
import { Info } from 'lucide-react';

interface InlineHelpProps {
  children: ReactNode;
  intent?: 'info' | 'success' | 'warning';
}

export function InlineHelp({ children, intent = 'info' }: InlineHelpProps) {
  const config = {
    info: {
      bg: 'var(--info-surface)',
      text: 'var(--info)',
    },
    success: {
      bg: 'var(--success-surface)',
      text: 'var(--success)',
    },
    warning: {
      bg: 'var(--warning-surface)',
      text: 'var(--warning)',
    },
  };

  const { bg, text } = config[intent];

  return (
    <div 
      className="p-4 rounded-lg flex items-start gap-3"
      style={{ backgroundColor: bg }}
    >
      <Info className="w-5 h-5 flex-shrink-0 mt-0.5" style={{ color: text }} />
      <div className="text-sm" style={{ color: text }}>
        {children}
      </div>
    </div>
  );
}
