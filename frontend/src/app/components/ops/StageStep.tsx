import { LucideIcon, CheckCircle, Clock, Circle, XCircle } from 'lucide-react';

interface StageStepProps {
  name: string;
  state: 'pending' | 'active' | 'done' | 'error';
  icon: LucideIcon;
}

export function StageStep({ name, state, icon: StageIcon }: StageStepProps) {
  const stateConfig = {
    done: { 
      color: 'var(--success)', 
      bg: 'var(--success-surface)',
      Icon: CheckCircle,
      label: 'Completed'
    },
    active: { 
      color: 'var(--processing)', 
      bg: 'var(--processing-surface)',
      Icon: Clock,
      label: 'In Progress',
      animate: true
    },
    pending: { 
      color: 'var(--text-tertiary)', 
      bg: 'var(--canvas)',
      Icon: Circle,
      label: 'Pending'
    },
    error: { 
      color: 'var(--danger)', 
      bg: 'var(--danger-surface)',
      Icon: XCircle,
      label: 'Failed'
    },
  };

  const { color, bg, Icon: StatusIcon, label, animate } = stateConfig[state];

  return (
    <div className="flex items-center gap-3">
      <div 
        className="w-10 h-10 rounded-full flex items-center justify-center flex-shrink-0"
        style={{ backgroundColor: bg }}
      >
        {state === 'done' || state === 'error' ? (
          <StatusIcon className="w-5 h-5" style={{ color }} />
        ) : state === 'active' ? (
          <StatusIcon className={`w-5 h-5 ${animate ? 'animate-pulse' : ''}`} style={{ color }} />
        ) : (
          <StageIcon className="w-5 h-5" style={{ color }} />
        )}
      </div>
      <div className="flex-1">
        <p className="font-medium" style={{ color }}>
          {name}
        </p>
        <p className="text-sm text-[var(--text-tertiary)]">
          {label}
        </p>
      </div>
    </div>
  );
}
