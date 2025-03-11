import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "LinkedIn AI Agent",
  description: "AI-powered assistant for job hunting, profile optimization, and networking on LinkedIn",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        {children}
      </body>
    </html>
  );
} 