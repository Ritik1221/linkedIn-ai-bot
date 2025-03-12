'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { useAuth } from '@/contexts/AuthContext';
import { 
  BriefcaseIcon, 
  ChatBubbleLeftRightIcon, 
  ChartBarIcon, 
  HomeIcon, 
  UserIcon, 
  BellIcon, 
  EnvelopeIcon, 
  Bars3Icon, 
  XMarkIcon,
  MagnifyingGlassIcon
} from '@heroicons/react/outline';

type NavItem = {
  name: string;
  href: string;
  icon: React.ForwardRefExoticComponent<React.SVGProps<SVGSVGElement>>;
  current: boolean;
};

export default function MainLayout({ children }: { children: React.ReactNode }) {
  const { isAuthenticated, user, logout } = useAuth();
  const pathname = usePathname();
  const [sidebarOpen, setSidebarOpen] = useState(false);

  // Define navigation items
  const navigation: NavItem[] = [
    { name: 'Dashboard', href: '/dashboard', icon: HomeIcon, current: pathname === '/dashboard' },
    { name: 'Jobs', href: '/jobs', icon: BriefcaseIcon, current: pathname.startsWith('/jobs') },
    { name: 'Applications', href: '/applications', icon: EnvelopeIcon, current: pathname.startsWith('/applications') },
    { name: 'Networking', href: '/networking', icon: ChatBubbleLeftRightIcon, current: pathname.startsWith('/networking') },
    { name: 'Analytics', href: '/analytics', icon: ChartBarIcon, current: pathname.startsWith('/analytics') },
    { name: 'Profile', href: '/profile', icon: UserIcon, current: pathname.startsWith('/profile') },
  ];

  // If not authenticated, redirect to login
  if (!isAuthenticated) {
    return (
      <div className="flex min-h-screen flex-col items-center justify-center">
        <div className="text-center">
          <h1 className="text-2xl font-bold">Please sign in to access this page</h1>
          <Link href="/auth/login" className="mt-4 inline-block rounded-md bg-primary px-4 py-2 text-sm font-medium text-white">
            Sign in
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background">
      {/* Mobile sidebar */}
      <div className="lg:hidden">
        {sidebarOpen && (
          <div className="fixed inset-0 z-50 bg-slate-900/80 backdrop-blur-sm" onClick={() => setSidebarOpen(false)} />
        )}

        <div className={`fixed inset-y-0 left-0 z-50 w-72 overflow-y-auto bg-white px-6 pb-4 transition-transform duration-300 ease-in-out ${sidebarOpen ? 'translate-x-0' : '-translate-x-full'}`}>
          <div className="flex h-16 items-center justify-between">
            <Link href="/dashboard" className="flex items-center">
              <span className="text-xl font-bold text-primary">LinkedIn AI Agent</span>
            </Link>
            <button
              type="button"
              className="-m-2.5 p-2.5 text-gray-700"
              onClick={() => setSidebarOpen(false)}
            >
              <span className="sr-only">Close sidebar</span>
              <XMarkIcon className="h-6 w-6" aria-hidden="true" />
            </button>
          </div>
          <nav className="mt-8">
            <ul className="space-y-2">
              {navigation.map((item) => (
                <li key={item.name}>
                  <Link
                    href={item.href}
                    className={`group flex items-center rounded-md px-3 py-2 text-sm font-medium ${
                      item.current ? 'bg-primary/10 text-primary' : 'text-muted-foreground hover:bg-muted hover:text-foreground'
                    }`}
                  >
                    <item.icon
                      className={`mr-3 h-5 w-5 flex-shrink-0 ${
                        item.current ? 'text-primary' : 'text-muted-foreground group-hover:text-foreground'
                      }`}
                      aria-hidden="true"
                    />
                    {item.name}
                  </Link>
                </li>
              ))}
            </ul>
          </nav>
        </div>
      </div>

      {/* Static sidebar for desktop */}
      <div className="hidden lg:fixed lg:inset-y-0 lg:z-50 lg:flex lg:w-72 lg:flex-col">
        <div className="flex grow flex-col gap-y-5 overflow-y-auto border-r border-border bg-card px-6 pb-4">
          <div className="flex h-16 items-center">
            <Link href="/dashboard" className="flex items-center">
              <span className="text-xl font-bold text-primary">LinkedIn AI Agent</span>
            </Link>
          </div>
          <nav className="flex flex-1 flex-col">
            <ul className="flex flex-1 flex-col gap-y-7">
              <li>
                <ul className="space-y-1">
                  {navigation.map((item) => (
                    <li key={item.name}>
                      <Link
                        href={item.href}
                        className={`group flex items-center rounded-md px-3 py-2 text-sm font-medium ${
                          item.current ? 'bg-primary/10 text-primary' : 'text-muted-foreground hover:bg-muted hover:text-foreground'
                        }`}
                      >
                        <item.icon
                          className={`mr-3 h-5 w-5 flex-shrink-0 ${
                            item.current ? 'text-primary' : 'text-muted-foreground group-hover:text-foreground'
                          }`}
                          aria-hidden="true"
                        />
                        {item.name}
                      </Link>
                    </li>
                  ))}
                </ul>
              </li>
              <li className="mt-auto">
                <button
                  onClick={() => logout()}
                  className="group flex w-full items-center rounded-md px-3 py-2 text-sm font-medium text-muted-foreground hover:bg-muted hover:text-foreground"
                >
                  <span>Sign out</span>
                </button>
              </li>
            </ul>
          </nav>
        </div>
      </div>

      {/* Main content */}
      <div className="lg:pl-72">
        <header className="sticky top-0 z-40 flex h-16 items-center border-b border-border bg-background px-4 shadow-sm sm:px-6 lg:px-8">
          <button
            type="button"
            className="-ml-2 mr-2 text-muted-foreground lg:hidden"
            onClick={() => setSidebarOpen(true)}
          >
            <span className="sr-only">Open sidebar</span>
            <Bars3Icon className="h-6 w-6" aria-hidden="true" />
          </button>
          
          {/* Search */}
          <div className="flex flex-1 gap-x-4 self-stretch lg:gap-x-6">
            <div className="relative flex flex-1 items-center">
              <MagnifyingGlassIcon className="pointer-events-none absolute inset-y-0 left-0 ml-3 h-5 w-5 text-muted-foreground" aria-hidden="true" />
              <input
                type="text"
                placeholder="Search jobs, connections, skills..."
                className="h-10 w-full rounded-md border border-input bg-background pl-10 pr-3 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
              />
            </div>
          </div>
          
          {/* Actions */}
          <div className="flex items-center gap-x-4">
            <button className="relative p-1 text-muted-foreground hover:text-foreground">
              <span className="sr-only">View notifications</span>
              <BellIcon className="h-6 w-6" aria-hidden="true" />
              <span className="absolute right-0 top-0 h-2 w-2 rounded-full bg-destructive"></span>
            </button>
            
            {/* Profile dropdown */}
            <div className="relative">
              <div className="flex items-center gap-x-3">
                <div className="h-8 w-8 rounded-full bg-primary/10 flex items-center justify-center text-primary font-medium">
                  {user?.firstName?.charAt(0) || user?.email?.charAt(0) || 'U'}
                </div>
                <span className="hidden lg:flex lg:items-center">
                  <span className="text-sm font-medium">
                    {user?.firstName ? `${user.firstName} ${user.lastName || ''}` : user?.email || 'User'}
                  </span>
                </span>
              </div>
            </div>
          </div>
        </header>

        <main className="py-6">
          <div className="px-4 sm:px-6 lg:px-8">
            {children}
          </div>
        </main>
      </div>
    </div>
  );
} 