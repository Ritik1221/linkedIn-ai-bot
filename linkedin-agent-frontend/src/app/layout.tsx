import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { Providers } from "@/components/providers";
import WebVitalsReporter from "./WebVitalsReporter";
import AuthProvider from '@/providers/AuthProvider';

const inter = Inter({ 
  subsets: ["latin"],
  display: 'swap',
  preload: true,
});

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
    <html lang="en" className={inter.className}>
      <body>
        <AuthProvider>
          <Providers>
            {children}
            <WebVitalsReporter />
          </Providers>
        </AuthProvider>
      </body>
    </html>
  );
} 