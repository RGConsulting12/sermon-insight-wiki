interface PillProps {
  children: string;
  type?: 'transcript' | 'audio' | 'embeddings' | 'default';
}

export function Pill({ children, type = 'default' }: PillProps) {
  const config = {
    transcript: {
      bg: '#dbeafe',
      text: '#1e40af',
    },
    audio: {
      bg: '#fce7f3',
      text: '#9f1239',
    },
    embeddings: {
      bg: '#d1fae5',
      text: '#065f46',
    },
    default: {
      bg: '#f3f4f6',
      text: '#374151',
    },
  };

  const { bg, text } = config[type];

  return (
    <span 
      className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
      style={{ backgroundColor: bg, color: text }}
    >
      {children}
    </span>
  );
}
