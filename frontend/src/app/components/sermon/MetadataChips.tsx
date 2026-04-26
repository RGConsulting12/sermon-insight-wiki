import { Calendar, User, Folder, MapPin } from 'lucide-react';

interface MetadataChipsProps {
  date?: string;
  series?: string;
  speaker?: string;
  campus?: string;
}

export function MetadataChips({ date, series, speaker, campus }: MetadataChipsProps) {
  const chips = [];

  if (date) {
    chips.push({ icon: Calendar, label: date, key: 'date' });
  }
  if (speaker) {
    chips.push({ icon: User, label: speaker, key: 'speaker' });
  }
  if (series) {
    chips.push({ icon: Folder, label: series, key: 'series' });
  }
  if (campus) {
    chips.push({ icon: MapPin, label: campus, key: 'campus' });
  }

  if (chips.length === 0) return null;

  return (
    <div className="flex flex-wrap gap-2">
      {chips.map(({ icon: Icon, label, key }) => (
        <div
          key={key}
          className="inline-flex items-center gap-1.5 px-3 py-1.5 bg-gray-100 rounded-md text-sm text-[var(--text-secondary)]"
        >
          <Icon className="w-3.5 h-3.5" />
          <span>{label}</span>
        </div>
      ))}
    </div>
  );
}
