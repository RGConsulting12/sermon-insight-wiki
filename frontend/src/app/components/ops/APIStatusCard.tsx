import { Card } from '../ui/card';
import { CheckCircle, XCircle } from 'lucide-react';

interface APIStatusCardProps {
  status: 'ok' | 'error';
  serviceName: string;
  message?: string;
}

export function APIStatusCard({ status, serviceName, message }: APIStatusCardProps) {
  const isOk = status === 'ok';
  const Icon = isOk ? CheckCircle : XCircle;
  const color = isOk ? 'var(--success)' : 'var(--danger)';
  const bg = isOk ? 'var(--success-surface)' : 'var(--danger-surface)';

  return (
    <Card 
      className="p-4"
      style={{ backgroundColor: bg }}
    >
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <Icon className="w-5 h-5" style={{ color }} />
          <div>
            <p className="font-medium" style={{ color }}>
              {serviceName}
            </p>
            {message && (
              <p className="text-sm mt-0.5" style={{ color }}>
                {message}
              </p>
            )}
          </div>
        </div>
        <span className="text-sm font-medium" style={{ color }}>
          {isOk ? '✓ Connected' : '✗ Error'}
        </span>
      </div>
    </Card>
  );
}
