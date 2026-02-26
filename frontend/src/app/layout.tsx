'use client';

import "./globals.css";
import Sidebar from "./components/Sidebar";
import { useState, useEffect } from "react";
import { Menu, X, Sparkles } from "lucide-react";
import Link from "next/link";

export default function RootLayout({ children }: { children: React.ReactNode }) {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);

  // Close sidebar on route change (optional but good for mobile)
  useEffect(() => {
    setIsSidebarOpen(false);
  }, []);

  return (
    <html lang="en" data-scroll-behavior="smooth">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet" />
        <title>NextHome — Intelligence Console</title>
        <meta name="description" content="AI-powered property intelligence platform for real estate professionals." />
      </head>
      <body>
        {/* Mobile Header */}
        <header className="mobile-header">
          <button className="hamburger" onClick={() => setIsSidebarOpen(true)}>
            <Menu size={24} />
          </button>

          <Link href="/" style={{ textDecoration: 'none', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <div style={{
              width: 32, height: 32, borderRadius: 8,
              background: 'linear-gradient(135deg, var(--color-accent), var(--color-cyan))',
              display: 'flex', alignItems: 'center', justifyContent: 'center'
            }}>
              <Sparkles size={18} color="#fff" />
            </div>
            <span style={{ fontSize: 16, fontWeight: 700, color: 'var(--color-text-primary)' }}>NextHome</span>
          </Link>

          <div style={{ width: 40 }} /> {/* Spacer */}
        </header>

        {/* Sidebar Overlay */}
        <div
          className={`mobile-overlay ${isSidebarOpen ? 'visible' : ''}`}
          onClick={() => setIsSidebarOpen(false)}
        />

        <Sidebar isOpen={isSidebarOpen} onClose={() => setIsSidebarOpen(false)} />

        <main className="main-content">
          {children}
        </main>
      </body>
    </html>
  );
}
