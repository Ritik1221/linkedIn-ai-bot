'use client';

import React from 'react';
import Link from 'next/link';
import { 
  BriefcaseIcon, 
  UserGroupIcon, 
  ChatBubbleLeftRightIcon, 
  ChartBarIcon,
  ArrowTrendingUpIcon,
  ClockIcon,
  DocumentCheckIcon,
  BookOpenIcon 
} from '@heroicons/react/outline';
import MainLayout from '@/components/layout/MainLayout';

// Dashboard stats and metrics
const stats = [
  { id: 1, name: 'Active Applications', value: '12', icon: DocumentCheckIcon, change: '+3', changeType: 'increase' },
  { id: 2, name: 'Job Matches', value: '24', icon: BriefcaseIcon, change: '+5', changeType: 'increase' },
  { id: 3, name: 'Networking Opportunities', value: '8', icon: UserGroupIcon, change: '+2', changeType: 'increase' },
  { id: 4, name: 'Skills Match Rate', value: '67%', icon: ChartBarIcon, change: '+4%', changeType: 'increase' },
];

// Recent job recommendations
const recentJobs = [
  {
    id: 1,
    title: 'Senior Software Engineer',
    company: 'Tech Innovations Inc.',
    location: 'San Francisco, CA (Remote)',
    matchPercentage: 92,
    postedAt: '2 days ago',
    skills: ['JavaScript', 'React', 'Node.js', 'AWS'],
  },
  {
    id: 2,
    title: 'Product Manager',
    company: 'Future Products Co.',
    location: 'New York, NY (Hybrid)',
    matchPercentage: 87,
    postedAt: '1 day ago',
    skills: ['Product Strategy', 'Agile', 'User Research', 'Roadmapping'],
  },
  {
    id: 3,
    title: 'UX/UI Designer',
    company: 'Creative Solutions Ltd.',
    location: 'Boston, MA (On-site)',
    matchPercentage: 84,
    postedAt: '3 days ago',
    skills: ['Figma', 'User Testing', 'Wireframing', 'Design Systems'],
  },
];

// Upcoming actions
const upcomingActions = [
  {
    id: 1,
    title: 'Follow up on Google application',
    dueDate: 'Today',
    type: 'application',
    priority: 'high',
  },
  {
    id: 2,
    title: 'Prepare for Microsoft technical interview',
    dueDate: 'Tomorrow',
    type: 'interview',
    priority: 'high',
  },
  {
    id: 3,
    title: 'Update LinkedIn profile with new skills',
    dueDate: 'In 2 days',
    type: 'profile',
    priority: 'medium',
  },
];

// Recent network activity
const networkActivity = [
  {
    id: 1,
    name: 'Sarah Johnson',
    role: 'Engineering Manager at Amazon',
    action: 'Accepted your connection request',
    time: '2 hours ago',
    image: '/placeholders/profile1.jpg',
  },
  {
    id: 2, 
    name: 'Alex Thompson',
    role: 'Senior Developer at Microsoft',
    action: 'Viewed your profile',
    time: '5 hours ago',
    image: '/placeholders/profile2.jpg',
  },
  {
    id: 3,
    name: 'Linda Chen',
    role: 'Tech Recruiter at Netflix',
    action: 'Messaged you about a new opportunity',
    time: '1 day ago',
    image: '/placeholders/profile3.jpg',
  },
];

/**
 * Dashboard page component
 * Displays overview of job search activity, recommendations, and actions
 */
export default function DashboardPage() {
  return (
    <MainLayout>
      <div className="space-y-8">
        {/* Page header */}
        <div>
          <h1 className="text-2xl font-bold tracking-tight">Dashboard</h1>
          <p className="mt-2 text-muted-foreground">
            Your job search at a glance. Track applications, discover opportunities, and improve your career prospects.
          </p>
        </div>

        {/* Stats overview */}
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
          {stats.map((stat) => (
            <div
              key={stat.id}
              className="overflow-hidden rounded-lg bg-white px-4 py-5 shadow sm:p-6"
            >
              <div className="flex items-center">
                <div className="flex-shrink-0 rounded-md bg-primary/10 p-3">
                  <stat.icon className="h-6 w-6 text-primary" aria-hidden="true" />
                </div>
                <div className="ml-5 w-0 flex-1">
                  <dt className="truncate text-sm font-medium text-muted-foreground">{stat.name}</dt>
                  <dd className="flex items-baseline">
                    <div className="text-2xl font-semibold text-foreground">{stat.value}</div>
                    <div className={`ml-2 flex items-baseline text-sm font-semibold ${
                      stat.changeType === 'increase' ? 'text-emerald-600' : 'text-red-600'
                    }`}>
                      {stat.changeType === 'increase' ? (
                        <ArrowTrendingUpIcon className="h-4 w-4 flex-shrink-0 self-center" aria-hidden="true" />
                      ) : (
                        <ArrowTrendingUpIcon className="h-4 w-4 flex-shrink-0 self-center transform rotate-180" aria-hidden="true" />
                      )}
                      <span className="sr-only">{stat.changeType === 'increase' ? 'Increased' : 'Decreased'} by</span>
                      <span className="ml-1">{stat.change}</span>
                    </div>
                  </dd>
                </div>
              </div>
            </div>
          ))}
        </div>

        <div className="grid grid-cols-1 gap-8 lg:grid-cols-2">
          {/* Recommended jobs */}
          <div className="overflow-hidden rounded-lg bg-white shadow">
            <div className="p-6">
              <div className="flex items-center justify-between">
                <h2 className="text-lg font-semibold">Recommended Jobs</h2>
                <Link href="/jobs" className="text-sm font-medium text-primary hover:underline">
                  View all jobs
                </Link>
              </div>
              <div className="mt-6 flow-root">
                <ul className="divide-y divide-border">
                  {recentJobs.map((job) => (
                    <li key={job.id} className="py-4">
                      <div className="flex items-center justify-between">
                        <div className="min-w-0 flex-1">
                          <p className="truncate text-sm font-medium">{job.title}</p>
                          <div className="mt-1 flex items-center text-sm text-muted-foreground">
                            <span>{job.company}</span>
                            <span className="mx-1.5">•</span>
                            <span>{job.location}</span>
                          </div>
                          <div className="mt-2 flex flex-wrap gap-2">
                            {job.skills.slice(0, 3).map((skill, idx) => (
                              <span key={idx} className="inline-flex items-center rounded-full bg-muted px-2.5 py-0.5 text-xs font-medium">
                                {skill}
                              </span>
                            ))}
                            {job.skills.length > 3 && (
                              <span className="inline-flex items-center rounded-full bg-muted px-2.5 py-0.5 text-xs font-medium">
                                +{job.skills.length - 3} more
                              </span>
                            )}
                          </div>
                        </div>
                        <div className="ml-4 flex flex-col items-end">
                          <span className="inline-flex items-center rounded-full bg-emerald-50 px-2.5 py-0.5 text-xs font-medium text-emerald-700">
                            {job.matchPercentage}% match
                          </span>
                          <span className="mt-2 text-xs text-muted-foreground">{job.postedAt}</span>
                        </div>
                      </div>
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          </div>

          {/* Upcoming actions */}
          <div className="overflow-hidden rounded-lg bg-white shadow">
            <div className="p-6">
              <div className="flex items-center justify-between">
                <h2 className="text-lg font-semibold">Upcoming Actions</h2>
                <Link href="/applications" className="text-sm font-medium text-primary hover:underline">
                  View all
                </Link>
              </div>
              <div className="mt-6 flow-root">
                <ul className="divide-y divide-border">
                  {upcomingActions.map((action) => (
                    <li key={action.id} className="py-4">
                      <div className="flex items-center">
                        <div className={`flex-shrink-0 rounded-full p-2 ${
                          action.priority === 'high' ? 'bg-rose-100' : 'bg-amber-100'
                        }`}>
                          <ClockIcon className={`h-5 w-5 ${
                            action.priority === 'high' ? 'text-rose-600' : 'text-amber-600'
                          }`} />
                        </div>
                        <div className="ml-4 min-w-0 flex-1">
                          <p className="truncate text-sm font-medium">{action.title}</p>
                          <p className="text-sm text-muted-foreground">Due: {action.dueDate}</p>
                        </div>
                        <div>
                          <button type="button" className="inline-flex items-center rounded-md bg-primary px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-primary/90">
                            Take action
                          </button>
                        </div>
                      </div>
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 gap-8 lg:grid-cols-2">
          {/* Network activity */}
          <div className="overflow-hidden rounded-lg bg-white shadow">
            <div className="p-6">
              <div className="flex items-center justify-between">
                <h2 className="text-lg font-semibold">Network Activity</h2>
                <Link href="/networking" className="text-sm font-medium text-primary hover:underline">
                  View all
                </Link>
              </div>
              <div className="mt-6 flow-root">
                <ul className="divide-y divide-border">
                  {networkActivity.map((activity) => (
                    <li key={activity.id} className="py-4">
                      <div className="flex items-center space-x-4">
                        <div className="flex-shrink-0">
                          <div className="h-10 w-10 rounded-full bg-gray-200"></div>
                        </div>
                        <div className="min-w-0 flex-1">
                          <p className="truncate text-sm font-medium">{activity.name}</p>
                          <p className="text-sm text-muted-foreground">{activity.role}</p>
                          <p className="mt-1 text-sm text-muted-foreground">
                            {activity.action} · {activity.time}
                          </p>
                        </div>
                        <div>
                          <button
                            type="button"
                            className="inline-flex items-center rounded-md bg-primary px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-primary/90"
                          >
                            Respond
                          </button>
                        </div>
                      </div>
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          </div>

          {/* Skills to develop */}
          <div className="overflow-hidden rounded-lg bg-white shadow">
            <div className="p-6">
              <div className="flex items-center justify-between">
                <h2 className="text-lg font-semibold">Skills to Develop</h2>
                <Link href="/profile/skills" className="text-sm font-medium text-primary hover:underline">
                  View all
                </Link>
              </div>
              <div className="mt-6 flow-root">
                <ul className="divide-y divide-border">
                  <li className="py-4">
                    <div className="flex items-center">
                      <div className="flex-shrink-0 rounded-full bg-blue-100 p-2">
                        <BookOpenIcon className="h-5 w-5 text-blue-600" />
                      </div>
                      <div className="ml-4 min-w-0 flex-1">
                        <p className="truncate text-sm font-medium">React Native</p>
                        <p className="text-sm text-muted-foreground">Requested in 15% of matched jobs</p>
                        <div className="mt-2 w-full bg-gray-200 rounded-full h-2">
                          <div className="bg-blue-600 h-2 rounded-full w-1/4"></div>
                        </div>
                      </div>
                    </div>
                  </li>
                  <li className="py-4">
                    <div className="flex items-center">
                      <div className="flex-shrink-0 rounded-full bg-blue-100 p-2">
                        <BookOpenIcon className="h-5 w-5 text-blue-600" />
                      </div>
                      <div className="ml-4 min-w-0 flex-1">
                        <p className="truncate text-sm font-medium">GraphQL</p>
                        <p className="text-sm text-muted-foreground">Requested in 23% of matched jobs</p>
                        <div className="mt-2 w-full bg-gray-200 rounded-full h-2">
                          <div className="bg-blue-600 h-2 rounded-full w-2/5"></div>
                        </div>
                      </div>
                    </div>
                  </li>
                  <li className="py-4">
                    <div className="flex items-center">
                      <div className="flex-shrink-0 rounded-full bg-blue-100 p-2">
                        <BookOpenIcon className="h-5 w-5 text-blue-600" />
                      </div>
                      <div className="ml-4 min-w-0 flex-1">
                        <p className="truncate text-sm font-medium">AWS Lambda</p>
                        <p className="text-sm text-muted-foreground">Requested in 18% of matched jobs</p>
                        <div className="mt-2 w-full bg-gray-200 rounded-full h-2">
                          <div className="bg-blue-600 h-2 rounded-full w-1/3"></div>
                        </div>
                      </div>
                    </div>
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>
    </MainLayout>
  );
} 