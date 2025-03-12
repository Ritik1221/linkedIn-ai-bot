'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { 
  UserGroupIcon,
  ChatBubbleLeftRightIcon,
  UserPlusIcon,
  MagnifyingGlassIcon,
  EnvelopeIcon,
  UserIcon,
  CakeIcon,
  ArrowPathIcon,
  PaperAirplaneIcon,
  ChevronRightIcon,
  MapPinIcon
} from '@heroicons/react/outline';
import MainLayout from '@/components/layout/MainLayout';

// Mock connections data
const connections = [
  {
    id: 1,
    name: 'Sarah Johnson',
    role: 'Engineering Manager at Amazon',
    mutualConnections: 12,
    location: 'Seattle, WA',
    profileImage: '/placeholders/profile1.jpg',
    isNew: true,
    connected: '2 days ago',
  },
  {
    id: 2,
    name: 'Michael Chen',
    role: 'Senior Software Engineer at Google',
    mutualConnections: 8,
    location: 'San Francisco, CA',
    profileImage: '/placeholders/profile2.jpg',
    isNew: false,
    connected: '1 week ago',
  },
  {
    id: 3,
    name: 'Emily Rodriguez',
    role: 'Product Manager at Netflix',
    mutualConnections: 5,
    location: 'Los Angeles, CA',
    profileImage: '/placeholders/profile3.jpg',
    isNew: false,
    connected: '2 weeks ago',
  },
  {
    id: 4,
    name: 'David Kim',
    role: 'UX Designer at Adobe',
    mutualConnections: 15,
    location: 'New York, NY',
    profileImage: '/placeholders/profile4.jpg',
    isNew: true,
    connected: '1 day ago',
  },
  {
    id: 5,
    name: 'Jessica Patel',
    role: 'Technical Recruiter at Microsoft',
    mutualConnections: 3,
    location: 'Seattle, WA',
    profileImage: '/placeholders/profile5.jpg',
    isNew: false,
    connected: '3 weeks ago',
  },
];

// Mock suggested connections
const suggestedConnections = [
  {
    id: 101,
    name: 'Robert Wilson',
    role: 'CTO at TechStart Inc.',
    mutualConnections: 18,
    location: 'Boston, MA',
    profileImage: '/placeholders/profile6.jpg',
    reason: 'Based on your profile',
  },
  {
    id: 102,
    name: 'Olivia Taylor',
    role: 'Full Stack Developer at Stripe',
    mutualConnections: 7,
    location: 'Remote',
    profileImage: '/placeholders/profile7.jpg',
    reason: 'Similar skills',
  },
  {
    id: 103,
    name: 'James Anderson',
    role: 'Engineering Director at Meta',
    mutualConnections: 11,
    location: 'Menlo Park, CA',
    profileImage: '/placeholders/profile8.jpg',
    reason: 'You may know each other',
  },
];

// Mock messages
const messages = [
  {
    id: 201,
    sender: {
      name: 'Sarah Johnson',
      role: 'Engineering Manager at Amazon',
      profileImage: '/placeholders/profile1.jpg',
    },
    preview: "Hi Alex, I noticed you have experience with React and Node.js. We're looking for...",
    date: '2 hours ago',
    unread: true,
  },
  {
    id: 202,
    sender: {
      name: 'Jessica Patel',
      role: 'Technical Recruiter at Microsoft',
      profileImage: '/placeholders/profile5.jpg',
    },
    preview: "Thanks for connecting! I'd love to talk about some opportunities we have at Microsoft...",
    date: '1 day ago',
    unread: false,
  },
  {
    id: 203,
    sender: {
      name: 'Michael Chen',
      role: 'Senior Software Engineer at Google',
      profileImage: '/placeholders/profile2.jpg',
    },
    preview: "Hey Alex, I'm putting together a meetup for developers in the area. Would you be interested...",
    date: '3 days ago',
    unread: false,
  },
];

// Mock upcoming events
const upcomingEvents = [
  {
    id: 301,
    title: 'Tech Networking Mixer',
    date: 'June 15, 2023',
    time: '6:00 PM - 8:00 PM',
    location: 'San Francisco, CA',
    attendees: 125,
    connections: 8,
  },
  {
    id: 302,
    title: 'Women in Tech Conference',
    date: 'June 22-23, 2023',
    time: 'All Day',
    location: 'Online',
    attendees: 500,
    connections: 15,
  },
];

// Networking stats data
const stats = [
  { name: 'Total Connections', value: '157', icon: UserGroupIcon, change: '+12 this month' },
  { name: 'Connection Requests', value: '5', icon: UserPlusIcon, change: '3 new today' },
  { name: 'Messages', value: '8', icon: EnvelopeIcon, change: '2 unread' },
  { name: 'Profile Views', value: '43', icon: UserIcon, change: '+18% from last week' },
];

/**
 * Networking page component
 * Displays connections, suggested connections, messages, and networking events
 */
export default function NetworkingPage() {
  const [activeSection, setActiveSection] = useState('connections');
  
  return (
    <MainLayout>
      <div className="space-y-8">
        {/* Page header */}
        <div>
          <h1 className="text-2xl font-bold tracking-tight">Networking</h1>
          <p className="mt-2 text-muted-foreground">
            Build and manage your professional network. Connect with industry professionals and grow your career opportunities.
          </p>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
          {stats.map((stat) => (
            <div
              key={stat.name}
              className="overflow-hidden rounded-lg bg-white px-4 py-5 shadow sm:p-6"
            >
              <div className="flex items-center">
                <div className="flex-shrink-0 rounded-md bg-primary/10 p-3">
                  <stat.icon className="h-6 w-6 text-primary" aria-hidden="true" />
                </div>
                <div className="ml-5 w-0 flex-1">
                  <dt className="truncate text-sm font-medium text-muted-foreground">{stat.name}</dt>
                  <dd className="mt-1">
                    <div className="text-lg font-semibold text-foreground">{stat.value}</div>
                    <div className="text-sm text-muted-foreground">{stat.change}</div>
                  </dd>
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Section Tabs */}
        <div className="border-b border-gray-200">
          <nav className="-mb-px flex space-x-8" aria-label="Tabs">
            <button
              onClick={() => setActiveSection('connections')}
              className={`${
                activeSection === 'connections'
                  ? 'border-primary text-primary'
                  : 'border-transparent text-muted-foreground hover:border-gray-300 hover:text-foreground'
              } whitespace-nowrap border-b-2 py-4 px-1 text-sm font-medium`}
            >
              My Connections
            </button>
            <button
              onClick={() => setActiveSection('suggested')}
              className={`${
                activeSection === 'suggested'
                  ? 'border-primary text-primary'
                  : 'border-transparent text-muted-foreground hover:border-gray-300 hover:text-foreground'
              } whitespace-nowrap border-b-2 py-4 px-1 text-sm font-medium`}
            >
              Suggested Connections
            </button>
            <button
              onClick={() => setActiveSection('messages')}
              className={`${
                activeSection === 'messages'
                  ? 'border-primary text-primary'
                  : 'border-transparent text-muted-foreground hover:border-gray-300 hover:text-foreground'
              } whitespace-nowrap border-b-2 py-4 px-1 text-sm font-medium`}
            >
              Messages
            </button>
            <button
              onClick={() => setActiveSection('events')}
              className={`${
                activeSection === 'events'
                  ? 'border-primary text-primary'
                  : 'border-transparent text-muted-foreground hover:border-gray-300 hover:text-foreground'
              } whitespace-nowrap border-b-2 py-4 px-1 text-sm font-medium`}
            >
              Events
            </button>
          </nav>
        </div>

        {/* Section content */}
        <div>
          {/* My Connections */}
          {activeSection === 'connections' && (
            <div>
              <div className="mb-6 flex items-center justify-between">
                <h2 className="text-xl font-semibold">My Connections</h2>
                <div className="relative rounded-md shadow-sm">
                  <div className="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
                    <MagnifyingGlassIcon className="h-5 w-5 text-muted-foreground" aria-hidden="true" />
                  </div>
                  <input
                    type="text"
                    className="block w-full rounded-md border border-input bg-background py-1.5 pl-10 pr-3 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
                    placeholder="Search connections"
                  />
                </div>
              </div>

              <div className="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3">
                {connections.map((connection) => (
                  <div
                    key={connection.id}
                    className="overflow-hidden rounded-lg border border-gray-200 bg-white shadow transition-all hover:border-primary/50"
                  >
                    <div className="p-5">
                      <div className="flex justify-between">
                        <div className="flex-shrink-0">
                          <div className="h-16 w-16 rounded-full bg-gray-200"></div>
                        </div>
                        <div className="ml-4 flex-1">
                          <h3 className="text-base font-medium">{connection.name}</h3>
                          <p className="text-sm text-muted-foreground">{connection.role}</p>
                          <div className="mt-1 flex items-center text-xs text-muted-foreground">
                            <MapPinIcon className="mr-1 h-3 w-3" />
                            {connection.location}
                          </div>
                          <div className="mt-2 text-xs text-muted-foreground">
                            {connection.mutualConnections} mutual connections
                          </div>
                        </div>
                      </div>
                      <div className="mt-4 flex items-center justify-between">
                        <span className="text-xs text-muted-foreground">
                          Connected {connection.connected}
                        </span>
                        <button className="rounded-md bg-primary px-2.5 py-1.5 text-xs font-medium text-white shadow-sm hover:bg-primary/90">
                          Message
                        </button>
                      </div>
                      {connection.isNew && (
                        <div className="mt-2 rounded-full bg-emerald-50 px-2 py-0.5 text-center text-xs font-medium text-emerald-700">
                          New connection
                        </div>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Suggested Connections */}
          {activeSection === 'suggested' && (
            <div>
              <div className="mb-6 flex items-center justify-between">
                <h2 className="text-xl font-semibold">Suggested Connections</h2>
                <button
                  type="button"
                  className="inline-flex items-center rounded-md border border-input bg-background px-3 py-2 text-sm font-medium text-foreground shadow-sm hover:bg-muted"
                >
                  <ArrowPathIcon className="mr-1.5 h-4 w-4" />
                  Refresh suggestions
                </button>
              </div>

              <div className="space-y-4">
                {suggestedConnections.map((connection) => (
                  <div
                    key={connection.id}
                    className="overflow-hidden rounded-lg border border-gray-200 bg-white shadow transition-all hover:border-primary/50"
                  >
                    <div className="p-5">
                      <div className="flex items-start">
                        <div className="flex-shrink-0">
                          <div className="h-16 w-16 rounded-full bg-gray-200"></div>
                        </div>
                        <div className="ml-4 flex-1">
                          <div className="flex items-center justify-between">
                            <div>
                              <h3 className="text-base font-medium">{connection.name}</h3>
                              <p className="text-sm text-muted-foreground">{connection.role}</p>
                              <div className="mt-1 flex items-center text-xs text-muted-foreground">
                                <MapPinIcon className="mr-1 h-3 w-3" />
                                {connection.location}
                              </div>
                              <div className="mt-1 text-xs">
                                <span className="font-medium">{connection.mutualConnections}</span>{' '}
                                <span className="text-muted-foreground">mutual connections</span>
                              </div>
                              <div className="mt-2 rounded-full bg-blue-50 px-2.5 py-0.5 text-xs font-medium text-blue-700 inline-block">
                                {connection.reason}
                              </div>
                            </div>
                            <div className="ml-4">
                              <button className="rounded-md bg-primary px-3 py-2 text-sm font-medium text-white shadow-sm hover:bg-primary/90">
                                <UserPlusIcon className="h-4 w-4" />
                                <span className="sr-only">Connect</span>
                              </button>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Messages */}
          {activeSection === 'messages' && (
            <div>
              <div className="mb-6 flex items-center justify-between">
                <h2 className="text-xl font-semibold">Messages</h2>
                <button
                  type="button"
                  className="inline-flex items-center rounded-md bg-primary px-3 py-2 text-sm font-medium text-white shadow-sm hover:bg-primary/90"
                >
                  <PaperAirplaneIcon className="mr-1.5 h-4 w-4" />
                  New Message
                </button>
              </div>

              <div className="overflow-hidden rounded-lg border border-gray-200 bg-white shadow">
                <ul className="divide-y divide-gray-200">
                  {messages.map((message) => (
                    <li key={message.id}>
                      <div className={`flex items-center p-4 hover:bg-gray-50 ${message.unread ? 'bg-blue-50' : ''}`}>
                        <div className="flex-shrink-0">
                          <div className="h-12 w-12 rounded-full bg-gray-200"></div>
                        </div>
                        <div className="ml-3 min-w-0 flex-1">
                          <div className="flex items-center justify-between">
                            <p className="truncate text-sm font-medium">{message.sender.name}</p>
                            <p className="text-xs text-muted-foreground">{message.date}</p>
                          </div>
                          <p className="truncate text-sm text-muted-foreground">{message.sender.role}</p>
                          <p className="mt-1 truncate text-sm">{message.preview}</p>
                        </div>
                        <div className="ml-4">
                          <ChevronRightIcon className="h-5 w-5 text-muted-foreground" />
                        </div>
                      </div>
                    </li>
                  ))}
                </ul>
                <div className="bg-gray-50 px-4 py-4 sm:px-6">
                  <div className="flex items-center justify-center">
                    <button
                      type="button"
                      className="inline-flex items-center rounded-md border border-input bg-background px-4 py-2 text-sm font-medium text-foreground shadow-sm hover:bg-muted"
                    >
                      View all messages
                    </button>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Events */}
          {activeSection === 'events' && (
            <div>
              <div className="mb-6 flex items-center justify-between">
                <h2 className="text-xl font-semibold">Networking Events</h2>
                <div>
                  <button
                    type="button"
                    className="inline-flex items-center rounded-md border border-input bg-background px-3 py-2 text-sm font-medium text-foreground shadow-sm hover:bg-muted"
                  >
                    Browse all events
                  </button>
                </div>
              </div>

              <div className="grid grid-cols-1 gap-6 md:grid-cols-2">
                {upcomingEvents.map((event) => (
                  <div
                    key={event.id}
                    className="overflow-hidden rounded-lg border border-gray-200 bg-white shadow transition-all hover:border-primary/50"
                  >
                    <div className="p-6">
                      <h3 className="text-lg font-medium">{event.title}</h3>
                      <div className="mt-2 flex items-center text-sm text-muted-foreground">
                        <CakeIcon className="mr-1.5 h-5 w-5 flex-shrink-0 text-muted-foreground" />
                        <span>{event.date}</span>
                        <span className="mx-1">•</span>
                        <span>{event.time}</span>
                      </div>
                      <div className="mt-1 flex items-center text-sm text-muted-foreground">
                        <MapPinIcon className="mr-1.5 h-5 w-5 flex-shrink-0 text-muted-foreground" />
                        <span>{event.location}</span>
                      </div>
                      <div className="mt-4 border-t border-gray-200 pt-4">
                        <div className="flex items-center justify-between">
                          <div className="text-sm">
                            <span className="font-medium">{event.attendees}</span>{' '}
                            <span className="text-muted-foreground">attendees</span>
                          </div>
                          <div className="text-sm">
                            <span className="font-medium">{event.connections}</span>{' '}
                            <span className="text-muted-foreground">connections attending</span>
                          </div>
                        </div>
                      </div>
                      <div className="mt-4">
                        <button
                          type="button"
                          className="inline-flex w-full items-center justify-center rounded-md bg-primary px-3 py-2 text-sm font-medium text-white shadow-sm hover:bg-primary/90"
                        >
                          Register for event
                        </button>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </MainLayout>
  );
} 