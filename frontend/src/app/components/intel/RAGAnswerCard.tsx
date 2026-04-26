import { Card } from '../ui/card';
import { Sparkles } from 'lucide-react';

interface RAGAnswerCardProps {
  answer: string;
  sourceCount: number;
}

export function RAGAnswerCard({ answer, sourceCount }: RAGAnswerCardProps) {
  return (
    <Card className="p-6">
      <div className="flex items-start gap-3 mb-4">
        <div className="p-2 bg-[var(--brand-primary)]/10 rounded-lg">
          <Sparkles className="w-5 h-5 text-[var(--brand-primary)]" />
        </div>
        <div>
          <h3 className="font-medium text-[var(--text-primary)]">AI-Generated Answer</h3>
          <p className="text-sm text-[var(--text-secondary)]">Based on your sermon library</p>
        </div>
      </div>
      
      <div className="prose max-w-none">
        <p className="text-[var(--text-primary)] leading-relaxed whitespace-pre-wrap">
          {answer}
        </p>
      </div>
      
      <div className="mt-4 pt-4 border-t border-[var(--border-default)]">
        <p className="text-xs text-[var(--text-tertiary)]">
          Generated from {sourceCount} relevant sermon excerpts
        </p>
      </div>
    </Card>
  );
}
