'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import {
    LayoutDashboard, Building2, Cpu, Search,
    TrendingUp, Bell, Settings, Sparkles, X
} from 'lucide-react';
import { useEffect } from 'react';

const navItems = [
    { href: '/', label: 'Dashboard', icon: LayoutDashboard },
    { href: '/properties', label: 'Properties', icon: Building2 },
    { href: '/pipeline', label: 'AI Pipeline', icon: Cpu },
    { href: '/search', label: 'Smart Search', icon: Search },
    { href: '/market', label: 'Market Intel', icon: TrendingUp },
    { href: '/alerts', label: 'Alerts', icon: Bell },
    { href: '/settings', label: 'Settings', icon: Settings },
];

interface SidebarProps {
    isOpen?: boolean;
    onClose?: () => void;
}

export default function Sidebar({ isOpen, onClose }: SidebarProps) {
    const pathname = usePathname();

    // Close sidebar when clicking a link on mobile
    const handleLinkClick = () => {
        if (onClose) onClose();
    };

    return (
        <aside className={`sidebar ${isOpen ? 'open' : ''}`}>
            {/* Logo Section */}
            <div style={{ padding: '24px 20px 32px', borderBottom: '1px solid var(--color-border)', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                <Link href="/" onClick={handleLinkClick} style={{ textDecoration: 'none', display: 'flex', alignItems: 'center', gap: '10px' }}>
                    <div style={{
                        width: 36, height: 36, borderRadius: 10,
                        background: 'linear-gradient(135deg, var(--color-accent), var(--color-cyan))',
                        display: 'flex', alignItems: 'center', justifyContent: 'center',
                        boxShadow: '0 4px 16px rgba(99, 102, 241, 0.3)'
                    }}>
                        <Sparkles size={20} color="#fff" />
                    </div>
                    <div className="logo-text">
                        <div style={{ fontSize: 18, fontWeight: 700, color: 'var(--color-text-primary)', lineHeight: 1.2 }}>
                            NextHome
                        </div>
                        <div style={{ fontSize: 10, fontWeight: 500, color: 'var(--color-text-muted)', letterSpacing: '0.08em', textTransform: 'uppercase' }}>
                            Intelligence
                        </div>
                    </div>
                </Link>

                {/* Mobile Close Button */}
                <button
                    onClick={onClose}
                    className="hamburger"
                    style={{ display: 'none' }} /* Managed via CSS for mobile purely */
                >
                    <X size={20} />
                </button>
            </div>

            {/* Navigation */}
            <nav style={{ padding: '16px 0', flex: 1 }}>
                <div style={{ padding: '0 20px', marginBottom: 8 }}>
                    <span className="nav-label" style={{ fontSize: 10, fontWeight: 600, color: 'var(--color-text-muted)', letterSpacing: '0.08em', textTransform: 'uppercase' }}>
                        Menu
                    </span>
                </div>
                {navItems.map((item) => {
                    const isActive = pathname === item.href || (item.href !== '/' && pathname.startsWith(item.href));
                    return (
                        <Link
                            key={item.href}
                            href={item.href}
                            className={`nav-item ${isActive ? 'active' : ''}`}
                            onClick={handleLinkClick}
                        >
                            <item.icon size={18} />
                            <span className="nav-label">{item.label}</span>
                        </Link>
                    );
                })}
            </nav>

            {/* Footer Status */}
            <div style={{
                padding: '16px 20px', borderTop: '1px solid var(--color-border)',
                display: 'flex', alignItems: 'center', gap: 8
            }}>
                <div style={{
                    width: 8, height: 8, borderRadius: '50%',
                    background: 'var(--color-emerald)',
                    boxShadow: '0 0 8px var(--color-emerald)'
                }} />
                <span className="nav-label" style={{ fontSize: 12, color: 'var(--color-text-muted)' }}>
                    Pipeline Active
                </span>
            </div>

            <style jsx>{`
                @media (max-width: 768px) {
                    .hamburger { display: block !important; }
                }
            `}</style>
        </aside>
    );
}
