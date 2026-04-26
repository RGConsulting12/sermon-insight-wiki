import { LucideIcon } from 'lucide-react';
import { Card } from '../ui/card';

interface StatTileProps {
  label: string;
  value: string | number;
  icon?: LucideIcon;
  iconColor?: string;
}

export function StatTile({ label, value, icon: Icon, iconColor = 'var(--brand-primary)' }: StatTileProps) {
  return (
    <Card className="p-6">
      <div className="flex items-start justify-between">
        <div>
          <p className="text-sm text-[var(--text-secondary)] mb-1">{label}</p>
          <p className="text-3xl font-semibold text-[var(--text-primary)]">{value}</p>
        </div>
        {Icon && (
          <div 
            className="p-2 rounded-lg"
            style={{ backgroundColor: `${iconColor}15` }}
          >
            <Icon className="w-5 h-5" style={{ color: iconColor }} />
          </div>
        )}
      </div>
    </Card>
  );
}
