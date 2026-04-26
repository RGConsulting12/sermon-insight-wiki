import { ReactNode } from 'react';

interface PageContainerProps {
  children: ReactNode;
  maxWidth?: number;
}

export function PageContainer({ children, maxWidth = 1280 }: PageContainerProps) {
  return (
    <div className="mx-auto px-6 py-8" style={{ maxWidth: `${maxWidth}px` }}>
      {children}
    </div>
  );
}
