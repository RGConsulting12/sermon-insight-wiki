import { CheckCircle, AlertTriangle, XCircle, HelpCircle } from 'lucide-react';

interface IndexStatusProps {
  status: 'ready' | 'partial' | 'none' | 'unknown';
  count?: number;
}

export function IndexStatus({ status, count }: IndexStatusProps) {
  const config = {
    ready: {
      icon: CheckCircle,
      label: count ? `${count} Sermons Indexed` : 'Index Ready',
      color: 'var(--index-ready)',
      bg: 'var(--index-ready-surface)',
    },
    partial: {
      icon: AlertTriangle,
      label: count ? `${count} Sermons Pending` : 'Partial Index',
      color: 'var(--index-missing)',
      bg: 'var(--index-missing-surface)',
    },
    none: {
      icon: XCircle,
      label: 'No Index',
      color: 'var(--danger)',
      bg: 'var(--danger-surface)',
    },
    unknown: {
      icon: HelpCircle,
      label: 'Index Status Unknown',
      color: 'var(--text-tertiary)',
      bg: 'var(--canvas)',
    },
  };

  const { icon: Icon, label, color, bg } = config[status];

  return (
    <div 
      className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full"
      style={{ backgroundColor: bg, color }}
    >
      <Icon className="w-4 h-4" />
      <span className="text-sm font-medium">{label}</span>
    </div>
  );
}
