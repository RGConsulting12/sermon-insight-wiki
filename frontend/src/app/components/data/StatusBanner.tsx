import { ReactNode } from 'react';
import { AlertCircle, CheckCircle, Info, AlertTriangle } from 'lucide-react';

interface StatusBannerProps {
  intent?: 'success' | 'warning' | 'danger' | 'info';
  children: ReactNode;
}

export function StatusBanner({ intent = 'info', children }: StatusBannerProps) {
  const config = {
    success: {
      bg: 'var(--success-surface)',
      border: 'var(--success)',
      text: 'var(--success)',
      icon: CheckCircle,
    },
    warning: {
      bg: 'var(--warning-surface)',
      border: 'var(--warning)',
      text: 'var(--warning)',
      icon: AlertTriangle,
    },
    danger: {
      bg: 'var(--danger-surface)',
      border: 'var(--danger)',
      text: 'var(--danger)',
      icon: AlertCircle,
    },
    info: {
      bg: 'var(--info-surface)',
      border: 'var(--info)',
      text: 'var(--info)',
      icon: Info,
    },
  };

  const { bg, border, text, icon: Icon } = config[intent];

  return (
    <div 
      className="p-4 rounded-lg border flex items-start gap-3"
      style={{ 
        backgroundColor: bg,
        borderColor: border,
      }}
    >
      <Icon className="w-5 h-5 flex-shrink-0 mt-0.5" style={{ color: text }} />
      <div className="flex-1" style={{ color: text }}>
        {children}
      </div>
    </div>
  );
}
