import type { Metadata } from "next";
import "./globals.css";
import Link from "next/link";

export const metadata: Metadata = {
  title: "LLM Research OS",
  description: "Local-first AI research platform",
};

const navLinks = [
  { href: "/", label: "Dashboard" },
  { href: "/query", label: "Search" },
  { href: "/agent", label: "Agent" },
  { href: "/evaluation", label: "Evaluation" },
  { href: "/experiments", label: "Experiments" },
];

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-gray-950 text-gray-100 font-sans">
        <nav className="border-b border-gray-800 bg-gray-900 px-6 py-4 flex items-center gap-8">
          <span className="text-lg font-bold tracking-tight text-indigo-400">LLM-OS</span>
          {navLinks.map((link) => (
            <Link
              key={link.href}
              href={link.href}
              className="text-sm text-gray-400 hover:text-white transition-colors"
            >
              {link.label}
            </Link>
          ))}
        </nav>
        <main className="p-6 max-w-5xl mx-auto">{children}</main>
      </body>
    </html>
  );
}
