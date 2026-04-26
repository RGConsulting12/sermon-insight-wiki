import { useState } from 'react';
import { Card } from '../ui/card';
import { Button } from '../ui/button';
import { ChevronDown, ChevronUp } from 'lucide-react';

interface TranscriptPanelProps {
  transcript: string;
  defaultExpanded?: boolean;
}

export function TranscriptPanel({ transcript, defaultExpanded = false }: TranscriptPanelProps) {
  const [isExpanded, setIsExpanded] = useState(defaultExpanded);

  return (
    <Card className="p-6">
      <div className="relative">
        <div 
          className={`
            overflow-hidden transition-all
            ${isExpanded ? 'max-h-none' : 'max-h-64'}
          `}
        >
          <div className="font-mono text-sm text-[var(--text-secondary)] whitespace-pre-wrap leading-relaxed">
            {transcript}
          </div>
        </div>
        
        {!isExpanded && (
          <div className="absolute bottom-0 left-0 right-0 h-24 bg-gradient-to-t from-white to-transparent pointer-events-none" />
        )}
      </div>
      
      <div className="mt-4 pt-4 border-t border-[var(--border-default)]">
        <Button 
          variant="ghost" 
          onClick={() => setIsExpanded(!isExpanded)}
          className="w-full gap-2"
        >
          {isExpanded ? (
            <>
              <ChevronUp className="w-4 h-4" />
              Collapse Transcript
            </>
          ) : (
            <>
              <ChevronDown className="w-4 h-4" />
              Expand Full Transcript
            </>
          )}
        </Button>
      </div>
    </Card>
  );
}
