"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { validateEnv } from "../lib/env";

export default function Home() {
  const [missingEnvVars, setMissingEnvVars] = useState<string[]>([]);
  
  useEffect(() => {
    // Check for missing environment variables
    setMissingEnvVars(validateEnv());
  }, []);

  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24">
      <div className="z-10 max-w-5xl w-full items-center justify-center font-mono text-sm">
        <h1 className="text-4xl font-bold mb-8 text-center">
          LinkedIn AI Agent
        </h1>
        
        <p className="text-xl mb-8 text-center">
          Your AI-powered assistant for job hunting, profile optimization, and networking on LinkedIn
        </p>
        
        {missingEnvVars.length > 0 ? (
          <div className="bg-yellow-100 border-l-4 border-yellow-500 text-yellow-700 p-4 mb-8" role="alert">
            <p className="font-bold">Environment Setup Required</p>
            <p>The following environment variables are missing:</p>
            <ul className="list-disc pl-5">
              {missingEnvVars.map((envVar) => (
                <li key={envVar}>{envVar}</li>
              ))}
            </ul>
            <p className="mt-2">
              Please check the README.md file for setup instructions.
            </p>
          </div>
        ) : null}
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-8">
          <Link 
            href="/auth/login"
            className="group rounded-lg border border-gray-300 px-5 py-4 transition-colors hover:border-gray-300 hover:bg-gray-100 hover:dark:border-neutral-700 hover:dark:bg-neutral-800/30"
          >
            <h2 className="mb-3 text-2xl font-semibold">
              Login{" "}
              <span className="inline-block transition-transform group-hover:translate-x-1 motion-reduce:transform-none">
                →
              </span>
            </h2>
            <p className="m-0 max-w-[30ch] text-sm opacity-50">
              Sign in with your LinkedIn account to get started.
            </p>
          </Link>

          <Link
            href="/dashboard"
            className="group rounded-lg border border-gray-300 px-5 py-4 transition-colors hover:border-gray-300 hover:bg-gray-100 hover:dark:border-neutral-700 hover:dark:bg-neutral-800/30"
          >
            <h2 className="mb-3 text-2xl font-semibold">
              Dashboard{" "}
              <span className="inline-block transition-transform group-hover:translate-x-1 motion-reduce:transform-none">
                →
              </span>
            </h2>
            <p className="m-0 max-w-[30ch] text-sm opacity-50">
              Access your personalized job hunting dashboard.
            </p>
          </Link>
        </div>
      </div>
    </main>
  );
} 