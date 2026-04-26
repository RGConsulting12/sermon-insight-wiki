import { ReactNode } from 'react';

interface TitleBlockProps {
  title: string;
  hasSeries?: boolean;
  seriesName?: string;
  hasSpeaker?: boolean;
  speakerName?: string;
  hasDate?: boolean;
  date?: string;
  density?: 'comfortable' | 'compact';
}

export function TitleBlock({ 
  title, 
  hasSeries,
  seriesName,
  hasSpeaker, 
  speakerName,
  hasDate,
  date,
  density = 'comfortable'
}: TitleBlockProps) {
  const titleSize = density === 'comfortable' ? 'text-lg' : 'text-base';
  const metaSize = density === 'comfortable' ? 'text-sm' : 'text-xs';
  
  const metaItems = [];
  if (hasSpeaker && speakerName) metaItems.push(speakerName);
  if (hasSeries && seriesName) metaItems.push(seriesName);
  if (hasDate && date) metaItems.push(date);

  return (
    <div>
      <h3 className={`${titleSize} font-medium text-[var(--text-primary)] mb-1`}>
        {title}
      </h3>
      {metaItems.length > 0 && (
        <p className={`${metaSize} text-[var(--text-secondary)]`}>
          {metaItems.join(' • ')}
        </p>
      )}
    </div>
  );
}
