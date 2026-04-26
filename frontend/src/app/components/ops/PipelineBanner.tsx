import { CheckCircle, AlertTriangle, Loader } from 'lucide-react';

interface PipelineBannerProps {
  status: 'idle' | 'running' | 'error';
  message?: string;
  currentItem?: string;
  totalItems?: number;
  currentIndex?: number;
}

export function PipelineBanner({ status, message, currentItem, totalItems, currentIndex }: PipelineBannerProps) {
  const config = {
    idle: {
      icon: CheckCircle,
      defaultMessage: 'Pipeline is idle and ready to process',
      color: 'var(--success)',
      bg: 'var(--success-surface)',
      border: 'var(--success)',
    },
    running: {
      icon: Loader,
      defaultMessage: 'Pipeline is currently running',
      color: 'var(--processing)',
      bg: 'var(--processing-surface)',
      border: 'var(--processing)',
    },
    error: {
      icon: AlertTriangle,
      defaultMessage: 'Pipeline encountered an error',
      color: 'var(--danger)',
      bg: 'var(--danger-surface)',
      border: 'var(--danger)',
    },
  };

  const { icon: Icon, defaultMessage, color, bg, border } = config[status];

  return (
    <div 
      className="p-4 rounded-lg border flex items-start gap-3"
      style={{ 
        backgroundColor: bg,
        borderColor: border,
      }}
    >
      <Icon className={`w-5 h-5 flex-shrink-0 mt-0.5 ${status === 'running' ? 'animate-spin' : ''}`} style={{ color }} />
      <div className="flex-1">
        <div className="flex items-center justify-between">
          <span className="font-medium" style={{ color }}>
            {message || defaultMessage}
          </span>
          {status === 'running' && currentIndex !== undefined && totalItems !== undefined && (
            <span className="text-sm" style={{ color }}>
              Processing {currentIndex} of {totalItems}
            </span>
          )}
        </div>
        {currentItem && (
          <p className="text-sm mt-1" style={{ color }}>
            Current: {currentItem}
          </p>
        )}
      </div>
    </div>
  );
}
