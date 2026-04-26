import { Link, useLocation } from 'react-router';
import { Home, Search, Database, Upload, BookOpen } from 'lucide-react';

const navItems = [
  { path: '/', label: 'Home', icon: Home },
  { path: '/search', label: 'Ask', icon: Search },
  { path: '/repository', label: 'Library', icon: Database },
  { path: '/pipeline', label: 'Pipeline', icon: Upload },
];

export function PrimaryNav() {
  const location = useLocation();

  return (
    <nav className="bg-[var(--surface)] border-b border-[var(--border-default)]">
      <div className="max-w-[1280px] mx-auto px-6">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center gap-3">
            <div className="flex items-center gap-2">
              <div className="flex items-center justify-center w-8 h-8 bg-[var(--brand-primary)] rounded">
                <BookOpen className="w-5 h-5 text-white" />
              </div>
              <div className="flex flex-col">
                <span className="text-xs text-[var(--text-tertiary)]">Local corpus</span>
                <span className="font-semibold text-[var(--text-primary)]">Sermon Insight Wiki</span>
              </div>
            </div>
          </div>
          
          <div className="flex items-center gap-1">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = location.pathname === item.path;
              
              return (
                <Link
                  key={item.path}
                  to={item.path}
                  className={`
                    flex items-center gap-2 px-4 py-2 rounded-md transition-colors
                    ${isActive 
                      ? 'bg-[var(--brand-primary)] text-white' 
                      : 'text-[var(--text-secondary)] hover:bg-gray-100 hover:text-[var(--text-primary)]'
                    }
                  `}
                >
                  <Icon className="w-4 h-4" />
                  <span>{item.label}</span>
                </Link>
              );
            })}
          </div>
        </div>
      </div>
    </nav>
  );
}
