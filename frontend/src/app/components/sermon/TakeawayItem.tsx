interface TakeawayItemProps {
  number: number;
  children: string;
}

export function TakeawayItem({ number, children }: TakeawayItemProps) {
  return (
    <div className="flex gap-4">
      <div className="flex-shrink-0 w-8 h-8 bg-[var(--brand-primary)] text-white rounded-full flex items-center justify-center font-semibold">
        {number}
      </div>
      <p className="text-[var(--text-primary)] leading-relaxed pt-1">
        {children}
      </p>
    </div>
  );
}
