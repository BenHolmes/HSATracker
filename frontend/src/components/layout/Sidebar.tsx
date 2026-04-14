import {
  ArrowRightLeft,
  Landmark,
  LayoutDashboard,
  PiggyBank,
  Receipt,
  ShieldCheck,
} from 'lucide-react'
import { NavLink } from 'react-router-dom'

const navItems = [
  { to: '/',                label: 'Dashboard',       icon: LayoutDashboard, end: true },
  { to: '/expenses',        label: 'Expenses',         icon: Receipt,         end: false },
  { to: '/reimbursements',  label: 'Reimbursements',   icon: ArrowRightLeft,  end: false },
  { to: '/contributions',   label: 'Contributions',    icon: PiggyBank,       end: false },
  { to: '/balance',         label: 'Balance',          icon: Landmark,        end: false },
]

export default function Sidebar() {
  return (
    <aside className="flex flex-col w-60 shrink-0 bg-slate-900 h-screen">
      {/* Logo / app name */}
      <div className="flex items-center gap-2.5 px-5 py-5 border-b border-slate-700">
        <ShieldCheck className="w-6 h-6 text-emerald-400 shrink-0" />
        <span className="text-white font-semibold text-base tracking-tight">HSATracker</span>
      </div>

      {/* Navigation */}
      <nav className="flex-1 px-3 py-4 space-y-0.5 overflow-y-auto">
        {navItems.map(({ to, label, icon: Icon, end }) => (
          <NavLink
            key={to}
            to={to}
            end={end}
            className={({ isActive }) =>
              [
                'flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium transition-colors',
                isActive
                  ? 'bg-emerald-600 text-white'
                  : 'text-slate-400 hover:bg-slate-800 hover:text-white',
              ].join(' ')
            }
          >
            <Icon className="w-4 h-4 shrink-0" />
            {label}
          </NavLink>
        ))}
      </nav>

      {/* Footer */}
      <div className="px-5 py-4 border-t border-slate-700">
        <p className="text-xs text-slate-500">Self-hosted · All data local</p>
      </div>
    </aside>
  )
}
