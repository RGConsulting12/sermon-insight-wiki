import { Outlet } from 'react-router';
import { PrimaryNav } from './PrimaryNav';

export function AppShell() {
  return (
    <div className="min-h-screen bg-[var(--canvas)]">
      <PrimaryNav />
      <main>
        <Outlet />
      </main>
    </div>
  );
}
