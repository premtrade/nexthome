import type { Metadata } from "next";
import "./globals.css";
import Sidebar from "./components/Sidebar";

export const metadata: Metadata = {
  title: "NextHome — Intelligence Console",
  description: "AI-powered property intelligence platform for real estate professionals. Automated SEO generation, buyer persona classification, and market analysis.",
  keywords: "real estate, AI, property management, SEO, buyer persona, market analysis",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" data-scroll-behavior="smooth">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet" />
      </head>
      <body>
        <Sidebar />
        <main className="main-content" style={{ marginLeft: 260, minHeight: '100vh', padding: '24px 32px' }}>
          {children}
        </main>
      </body>
    </html>
  );
}
