'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import {
  BriefcaseIcon,
  DocumentTextIcon,
  ClockIcon,
  CheckCircleIcon,
  XCircleIcon,
  EnvelopeIcon,
  PhoneIcon,
  VideoCameraIcon,
  UserGroupIcon,
  ChartBarIcon,
  PlusIcon,
  ChatBubbleLeftRightIcon,
  CalendarIcon,
  MapPinIcon,
  DocumentDuplicateIcon
} from '@heroicons/react/outline';
import MainLayout from '@/components/layout/MainLayout';

// Application status types
const statusTypes = {
  APPLIED: 'applied',
  SCREENING: 'screening',
  INTERVIEW: 'interview',
  OFFER: 'offer',
  REJECTED: 'rejected',
  WITHDRAWN: 'withdrawn',
};

// Mock applications data
const applications = [
  {
    id: 1,
    company: 'Google',
    role: 'Senior Software Engineer',
    location: 'Mountain View, CA (Remote)',
    status: statusTypes.INTERVIEW,
    dateApplied: '2023-06-01',
    lastUpdated: '2023-06-10',
    salary: '$150,000 - $180,000',
    contact: {
      name: 'Sarah Johnson',
      role: 'Technical Recruiter',
      email: 'sarah.johnson@google.com',
      phone: '(555) 123-4567',
    },
    nextSteps: [
      {
        id: 1,
        type: 'interview',
        title: 'Technical Interview',
        date: '2023-06-15T14:00:00',
        description: 'System design and coding interview with the engineering team.',
        completed: false,
      },
    ],
    notes: 'Had a great initial call with the recruiter. Team seems to be looking for someone with React and Node.js experience.',
    steps: [
      {
        id: 1,
        date: '2023-06-01',
        title: 'Application Submitted',
        description: 'Applied through company website.',
        status: 'completed',
      },
      {
        id: 2,
        date: '2023-06-05',
        title: 'Initial Screening Call',
        description: '30-minute call with recruiter Sarah Johnson.',
        status: 'completed',
      },
      {
        id: 3,
        date: '2023-06-10',
        title: 'Technical Screening',
        description: 'Completed online coding assessment.',
        status: 'completed',
      },
      {
        id: 4,
        date: '2023-06-15',
        title: 'Technical Interview',
        description: 'System design and coding interview with the engineering team.',
        status: 'scheduled',
      },
      {
        id: 5,
        date: null,
        title: 'Final Interviews',
        description: 'Full day of interviews with team members and leadership.',
        status: 'upcoming',
      },
    ],
  },
  {
    id: 2,
    company: 'Microsoft',
    role: 'Product Manager',
    location: 'Redmond, WA (Hybrid)',
    status: statusTypes.SCREENING,
    dateApplied: '2023-06-05',
    lastUpdated: '2023-06-08',
    salary: '$140,000 - $170,000',
    contact: {
      name: 'Michael Chen',
      role: 'HR Specialist',
      email: 'michael.chen@microsoft.com',
      phone: '(555) 234-5678',
    },
    nextSteps: [
      {
        id: 1,
        type: 'assessment',
        title: 'Product Case Study',
        date: '2023-06-18T10:00:00',
        description: 'Complete the product case study assignment.',
        completed: false,
      },
    ],
    notes: 'They\'re looking for someone with experience in agile methodologies and product roadmapping.',
    steps: [
      {
        id: 1,
        date: '2023-06-05',
        title: 'Application Submitted',
        description: 'Applied through LinkedIn.',
        status: 'completed',
      },
      {
        id: 2,
        date: '2023-06-08',
        title: 'Initial Screening Call',
        description: '45-minute call with HR specialist Michael Chen.',
        status: 'completed',
      },
      {
        id: 3,
        date: '2023-06-18',
        title: 'Product Case Study',
        description: 'Complete the product case study assignment.',
        status: 'scheduled',
      },
    ],
  },
  {
    id: 3,
    company: 'Amazon',
    role: 'Full Stack Developer',
    location: 'Seattle, WA (On-site)',
    status: statusTypes.APPLIED,
    dateApplied: '2023-06-10',
    lastUpdated: '2023-06-10',
    salary: '$130,000 - $160,000',
    contact: null,
    nextSteps: [],
    notes: 'Position requires experience with AWS services and serverless architecture.',
    steps: [
      {
        id: 1,
        date: '2023-06-10',
        title: 'Application Submitted',
        description: 'Applied through company website.',
        status: 'completed',
      },
    ],
  },
  {
    id: 4,
    company: 'Netflix',
    role: 'Senior UI Engineer',
    location: 'Los Gatos, CA (Remote)',
    status: statusTypes.REJECTED,
    dateApplied: '2023-05-15',
    lastUpdated: '2023-05-30',
    salary: '$160,000 - $200,000',
    contact: {
      name: 'Jessica Lee',
      role: 'Technical Recruiter',
      email: 'jessica.lee@netflix.com',
      phone: '(555) 345-6789',
    },
    nextSteps: [],
    notes: 'Received feedback that they were looking for someone with more streaming platform experience. Good to try again in a year.',
    steps: [
      {
        id: 1,
        date: '2023-05-15',
        title: 'Application Submitted',
        description: 'Applied through referral.',
        status: 'completed',
      },
      {
        id: 2,
        date: '2023-05-20',
        title: 'Initial Screening Call',
        description: '30-minute call with recruiter Jessica Lee.',
        status: 'completed',
      },
      {
        id: 3,
        date: '2023-05-25',
        title: 'Technical Screening',
        description: 'Completed online coding assessment.',
        status: 'completed',
      },
      {
        id: 4,
        date: '2023-05-30',
        title: 'Rejection',
        description: 'Received rejection email.',
        status: 'completed',
      },
    ],
  },
  {
    id: 5,
    company: 'Apple',
    role: 'iOS Developer',
    location: 'Cupertino, CA (On-site)',
    status: statusTypes.OFFER,
    dateApplied: '2023-05-10',
    lastUpdated: '2023-06-05',
    salary: '$140,000 - $180,000',
    contact: {
      name: 'David Kim',
      role: 'Engineering Manager',
      email: 'david.kim@apple.com',
      phone: '(555) 456-7890',
    },
    nextSteps: [
      {
        id: 1,
        type: 'offer',
        title: 'Review Offer Letter',
        date: '2023-06-15T00:00:00',
        description: 'Review and respond to the offer by June 15.',
        completed: false,
      },
    ],
    notes: 'Offer is competitive but would require relocation to Cupertino. Need to consider living costs.',
    steps: [
      {
        id: 1,
        date: '2023-05-10',
        title: 'Application Submitted',
        description: 'Applied through company website.',
        status: 'completed',
      },
      {
        id: 2,
        date: '2023-05-15',
        title: 'Initial Screening Call',
        description: '45-minute call with recruiter.',
        status: 'completed',
      },
      {
        id: 3,
        date: '2023-05-20',
        title: 'Technical Screening',
        description: 'Completed online coding assessment.',
        status: 'completed',
      },
      {
        id: 4,
        date: '2023-05-25',
        title: 'First Round Interview',
        description: 'Technical interview with two engineers.',
        status: 'completed',
      },
      {
        id: 5,
        date: '2023-05-30',
        title: 'Final Round Interviews',
        description: 'Series of interviews with team members and leadership.',
        status: 'completed',
      },
      {
        id: 6,
        date: '2023-06-05',
        title: 'Offer Received',
        description: 'Received formal offer letter.',
        status: 'completed',
      },
    ],
  },
];

// Application statistics
const stats = [
  { id: 1, name: 'Total Applications', value: '12', icon: DocumentTextIcon },
  { id: 2, name: 'Active Applications', value: '8', icon: BriefcaseIcon },
  { id: 3, name: 'Interviews Scheduled', value: '3', icon: CalendarIcon },
  { id: 4, name: 'Offers', value: '1', icon: CheckCircleIcon },
];

/**
 * Applications page component
 * Tracks and manages job applications
 */
export default function ApplicationsPage() {
  const [selectedApplication, setSelectedApplication] = useState<number | null>(null);
  const [activeFilter, setActiveFilter] = useState('all');

  // Filter applications by status
  const filteredApplications = activeFilter === 'all'
    ? applications
    : applications.filter(app => app.status === activeFilter);

  // Get application details by ID
  const getApplicationDetails = (id: number) => {
    return applications.find(app => app.id === id) || null;
  };

  // Handle application card click
  const handleApplicationClick = (id: number) => {
    setSelectedApplication(id);
  };

  // Get color styles based on status
  const getStatusStyles = (status: string) => {
    switch (status) {
      case statusTypes.APPLIED:
        return { bg: 'bg-blue-100', text: 'text-blue-700', icon: DocumentTextIcon };
      case statusTypes.SCREENING:
        return { bg: 'bg-purple-100', text: 'text-purple-700', icon: PhoneIcon };
      case statusTypes.INTERVIEW:
        return { bg: 'bg-amber-100', text: 'text-amber-700', icon: UserGroupIcon };
      case statusTypes.OFFER:
        return { bg: 'bg-emerald-100', text: 'text-emerald-700', icon: CheckCircleIcon };
      case statusTypes.REJECTED:
        return { bg: 'bg-red-100', text: 'text-red-700', icon: XCircleIcon };
      case statusTypes.WITHDRAWN:
        return { bg: 'bg-gray-100', text: 'text-gray-700', icon: XCircleIcon };
      default:
        return { bg: 'bg-gray-100', text: 'text-gray-700', icon: DocumentTextIcon };
    }
  };

  // Format date string to readable format
  const formatDate = (dateString: string) => {
    if (!dateString) return '';
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
  };

  // Format datetime string for events
  const formatDateTime = (dateTimeString: string) => {
    if (!dateTimeString) return '';
    const date = new Date(dateTimeString);
    return date.toLocaleDateString('en-US', { 
      month: 'short', 
      day: 'numeric', 
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  return (
    <MainLayout>
      <div className="space-y-8">
        {/* Page header */}
        <div>
          <h1 className="text-2xl font-bold tracking-tight">Applications</h1>
          <p className="mt-2 text-muted-foreground">
            Track and manage your job applications. Keep notes, follow up on interviews, and never miss a deadline.
          </p>
        </div>

        {/* Application Stats */}
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
                  <dd className="mt-1 text-3xl font-semibold tracking-tight text-foreground">{stat.value}</dd>
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Filter tabs */}
        <div className="border-b border-gray-200">
          <nav className="-mb-px flex space-x-8" aria-label="Tabs">
            <button
              onClick={() => setActiveFilter('all')}
              className={`${
                activeFilter === 'all'
                  ? 'border-primary text-primary'
                  : 'border-transparent text-muted-foreground hover:border-gray-300 hover:text-foreground'
              } whitespace-nowrap border-b-2 py-4 px-1 text-sm font-medium`}
            >
              All Applications
            </button>
            <button
              onClick={() => setActiveFilter(statusTypes.APPLIED)}
              className={`${
                activeFilter === statusTypes.APPLIED
                  ? 'border-primary text-primary'
                  : 'border-transparent text-muted-foreground hover:border-gray-300 hover:text-foreground'
              } whitespace-nowrap border-b-2 py-4 px-1 text-sm font-medium`}
            >
              Applied
            </button>
            <button
              onClick={() => setActiveFilter(statusTypes.SCREENING)}
              className={`${
                activeFilter === statusTypes.SCREENING
                  ? 'border-primary text-primary'
                  : 'border-transparent text-muted-foreground hover:border-gray-300 hover:text-foreground'
              } whitespace-nowrap border-b-2 py-4 px-1 text-sm font-medium`}
            >
              Screening
            </button>
            <button
              onClick={() => setActiveFilter(statusTypes.INTERVIEW)}
              className={`${
                activeFilter === statusTypes.INTERVIEW
                  ? 'border-primary text-primary'
                  : 'border-transparent text-muted-foreground hover:border-gray-300 hover:text-foreground'
              } whitespace-nowrap border-b-2 py-4 px-1 text-sm font-medium`}
            >
              Interviews
            </button>
            <button
              onClick={() => setActiveFilter(statusTypes.OFFER)}
              className={`${
                activeFilter === statusTypes.OFFER
                  ? 'border-primary text-primary'
                  : 'border-transparent text-muted-foreground hover:border-gray-300 hover:text-foreground'
              } whitespace-nowrap border-b-2 py-4 px-1 text-sm font-medium`}
            >
              Offers
            </button>
          </nav>
        </div>

        {/* Main content grid */}
        <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
          {/* Applications list */}
          <div className="lg:col-span-1">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-medium">Applications ({filteredApplications.length})</h2>
              <button
                type="button"
                className="inline-flex items-center rounded-md bg-primary px-3 py-2 text-sm font-medium text-white shadow-sm hover:bg-primary/90"
              >
                <PlusIcon className="-ml-0.5 mr-1.5 h-4 w-4" aria-hidden="true" />
                Add Application
              </button>
            </div>
            
            <div className="space-y-3">
              {filteredApplications.map((application) => {
                const statusStyle = getStatusStyles(application.status);
                return (
                  <div
                    key={application.id}
                    className={`cursor-pointer rounded-lg border p-4 shadow-sm transition-colors hover:border-primary/50 ${
                      selectedApplication === application.id ? 'border-primary bg-primary/5' : 'border-gray-200 bg-white'
                    }`}
                    onClick={() => handleApplicationClick(application.id)}
                  >
                    <div className="flex items-center justify-between">
                      <div className="min-w-0 flex-1">
                        <h3 className="text-sm font-medium">{application.role}</h3>
                        <p className="mt-1 truncate text-sm text-muted-foreground">{application.company}</p>
                      </div>
                      <div className={`ml-4 flex-shrink-0 rounded-full ${statusStyle.bg} p-1`}>
                        <statusStyle.icon className={`h-4 w-4 ${statusStyle.text}`} aria-hidden="true" />
                      </div>
                    </div>
                    <div className="mt-4 flex items-center justify-between">
                      <div className="flex items-center text-xs text-muted-foreground">
                        <MapPinIcon className="mr-1 h-3 w-3" />
                        {application.location}
                      </div>
                      <div className="text-xs text-muted-foreground">
                        Applied {formatDate(application.dateApplied)}
                      </div>
                    </div>
                    <div className="mt-2">
                      <span
                        className={`inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium ${statusStyle.bg} ${statusStyle.text}`}
                      >
                        {application.status.charAt(0).toUpperCase() + application.status.slice(1)}
                      </span>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Application details */}
          <div className="lg:col-span-2">
            {selectedApplication ? (
              (() => {
                const application = getApplicationDetails(selectedApplication);
                if (!application) return null;
                
                const statusStyle = getStatusStyles(application.status);
                
                return (
                  <div className="rounded-lg bg-white shadow">
                    {/* Header */}
                    <div className="border-b border-gray-200 px-4 py-5 sm:px-6">
                      <div className="flex items-center justify-between">
                        <div>
                          <h3 className="text-lg font-medium text-foreground">{application.role}</h3>
                          <p className="mt-1 text-sm text-muted-foreground">{application.company} · {application.location}</p>
                        </div>
                        <div className="flex items-center">
                          <span
                            className={`inline-flex items-center rounded-full px-3 py-0.5 text-sm font-medium ${statusStyle.bg} ${statusStyle.text}`}
                          >
                            <statusStyle.icon className="mr-1 h-4 w-4" aria-hidden="true" />
                            {application.status.charAt(0).toUpperCase() + application.status.slice(1)}
                          </span>
                        </div>
                      </div>
                      <div className="mt-4 grid grid-cols-2 gap-4 text-sm sm:grid-cols-3">
                        <div>
                          <div className="text-sm font-medium text-muted-foreground">Applied</div>
                          <div className="mt-1">{formatDate(application.dateApplied)}</div>
                        </div>
                        <div>
                          <div className="text-sm font-medium text-muted-foreground">Last Updated</div>
                          <div className="mt-1">{formatDate(application.lastUpdated)}</div>
                        </div>
                        <div>
                          <div className="text-sm font-medium text-muted-foreground">Salary Range</div>
                          <div className="mt-1">{application.salary}</div>
                        </div>
                      </div>
                    </div>
                    
                    {/* Tabs */}
                    <div className="border-b border-gray-200">
                      <nav className="-mb-px flex space-x-8 px-4" aria-label="Tabs">
                        <button className="border-primary text-primary whitespace-nowrap border-b-2 py-4 px-1 text-sm font-medium">
                          Details
                        </button>
                      </nav>
                    </div>
                    
                    {/* Content */}
                    <div className="px-4 py-5 sm:p-6">
                      {/* Application Timeline */}
                      <div className="mb-8">
                        <h4 className="text-base font-medium">Application Timeline</h4>
                        <div className="mt-4 flow-root">
                          <ul className="-mb-8">
                            {application.steps.map((step, stepIdx) => (
                              <li key={step.id}>
                                <div className="relative pb-8">
                                  {stepIdx !== application.steps.length - 1 ? (
                                    <span
                                      className="absolute top-4 left-4 -ml-px h-full w-0.5 bg-gray-200"
                                      aria-hidden="true"
                                    />
                                  ) : null}
                                  <div className="relative flex space-x-3">
                                    <div>
                                      <span
                                        className={`h-8 w-8 rounded-full flex items-center justify-center ring-8 ring-white ${
                                          step.status === 'completed'
                                            ? 'bg-emerald-500'
                                            : step.status === 'scheduled'
                                            ? 'bg-blue-500'
                                            : 'bg-gray-400'
                                        }`}
                                      >
                                        {step.status === 'completed' ? (
                                          <CheckCircleIcon className="h-5 w-5 text-white" aria-hidden="true" />
                                        ) : step.status === 'scheduled' ? (
                                          <CalendarIcon className="h-5 w-5 text-white" aria-hidden="true" />
                                        ) : (
                                          <ClockIcon className="h-5 w-5 text-white" aria-hidden="true" />
                                        )}
                                      </span>
                                    </div>
                                    <div className="min-w-0 flex-1 pt-1.5">
                                      <div>
                                        <p className="text-sm font-medium text-foreground">{step.title}</p>
                                        {step.date && (
                                          <p className="text-xs text-muted-foreground">
                                            {formatDate(step.date)}
                                          </p>
                                        )}
                                      </div>
                                      <div className="mt-2 text-sm text-muted-foreground">
                                        <p>{step.description}</p>
                                      </div>
                                    </div>
                                  </div>
                                </div>
                              </li>
                            ))}
                          </ul>
                        </div>
                      </div>
                      
                      {/* Next Steps */}
                      {application.nextSteps.length > 0 && (
                        <div className="mb-8">
                          <h4 className="text-base font-medium">Next Steps</h4>
                          <div className="mt-4 space-y-4">
                            {application.nextSteps.map((step) => (
                              <div
                                key={step.id}
                                className="rounded-lg border border-gray-200 bg-white p-4 shadow-sm"
                              >
                                <div className="flex items-start">
                                  <div className="flex-shrink-0">
                                    {step.type === 'interview' ? (
                                      <div className="rounded-full bg-blue-100 p-2">
                                        <VideoCameraIcon className="h-5 w-5 text-blue-600" aria-hidden="true" />
                                      </div>
                                    ) : step.type === 'assessment' ? (
                                      <div className="rounded-full bg-purple-100 p-2">
                                        <DocumentDuplicateIcon className="h-5 w-5 text-purple-600" aria-hidden="true" />
                                      </div>
                                    ) : (
                                      <div className="rounded-full bg-emerald-100 p-2">
                                        <DocumentTextIcon className="h-5 w-5 text-emerald-600" aria-hidden="true" />
                                      </div>
                                    )}
                                  </div>
                                  <div className="ml-4 min-w-0 flex-1">
                                    <div className="flex items-center justify-between">
                                      <h5 className="text-sm font-medium">{step.title}</h5>
                                      <span className="text-xs text-muted-foreground">
                                        {formatDateTime(step.date)}
                                      </span>
                                    </div>
                                    <p className="mt-1 text-sm text-muted-foreground">{step.description}</p>
                                  </div>
                                </div>
                              </div>
                            ))}
                          </div>
                        </div>
                      )}
                      
                      {/* Contact Information */}
                      {application.contact && (
                        <div className="mb-8">
                          <h4 className="text-base font-medium">Contact Information</h4>
                          <div className="mt-4 rounded-lg border border-gray-200 bg-white p-4 shadow-sm">
                            <div className="flex items-center">
                              <div className="flex-shrink-0">
                                <div className="h-10 w-10 rounded-full bg-gray-200"></div>
                              </div>
                              <div className="ml-4 min-w-0 flex-1">
                                <p className="text-sm font-medium">{application.contact.name}</p>
                                <p className="text-xs text-muted-foreground">{application.contact.role}</p>
                              </div>
                              <div className="flex space-x-2">
                                <button
                                  type="button"
                                  className="inline-flex items-center rounded-full bg-primary/10 p-2 text-primary hover:bg-primary/20"
                                >
                                  <EnvelopeIcon className="h-4 w-4" aria-hidden="true" />
                                  <span className="sr-only">Email</span>
                                </button>
                                <button
                                  type="button"
                                  className="inline-flex items-center rounded-full bg-primary/10 p-2 text-primary hover:bg-primary/20"
                                >
                                  <PhoneIcon className="h-4 w-4" aria-hidden="true" />
                                  <span className="sr-only">Call</span>
                                </button>
                              </div>
                            </div>
                            <div className="mt-4 border-t border-gray-200 pt-4">
                              <div className="grid grid-cols-1 gap-y-4 gap-x-8 text-sm sm:grid-cols-2">
                                <div>
                                  <div className="text-muted-foreground">Email</div>
                                  <div className="mt-1">{application.contact.email}</div>
                                </div>
                                <div>
                                  <div className="text-muted-foreground">Phone</div>
                                  <div className="mt-1">{application.contact.phone}</div>
                                </div>
                              </div>
                            </div>
                          </div>
                        </div>
                      )}
                      
                      {/* Notes */}
                      <div>
                        <h4 className="text-base font-medium">Notes</h4>
                        <div className="mt-4 rounded-lg border border-gray-200 bg-white p-4 shadow-sm">
                          <p className="text-sm text-foreground">{application.notes}</p>
                        </div>
                      </div>
                    </div>
                    
                    {/* Actions */}
                    <div className="border-t border-gray-200 px-4 py-5 sm:px-6">
                      <div className="flex justify-end space-x-3">
                        <button
                          type="button"
                          className="inline-flex items-center rounded-md border border-input bg-background px-4 py-2 text-sm font-medium text-foreground shadow-sm hover:bg-muted"
                        >
                          <ChatBubbleLeftRightIcon className="mr-2 h-4 w-4" aria-hidden="true" />
                          Add Note
                        </button>
                        <button
                          type="button"
                          className="inline-flex items-center rounded-md border border-input bg-background px-4 py-2 text-sm font-medium text-foreground shadow-sm hover:bg-muted"
                        >
                          <CalendarIcon className="mr-2 h-4 w-4" aria-hidden="true" />
                          Add Event
                        </button>
                        <button
                          type="button"
                          className="inline-flex items-center rounded-md bg-primary px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-primary/90"
                        >
                          <ChartBarIcon className="mr-2 h-4 w-4" aria-hidden="true" />
                          Update Status
                        </button>
                      </div>
                    </div>
                  </div>
                );
              })()
            ) : (
              <div className="flex h-full min-h-[400px] flex-col items-center justify-center rounded-lg border-2 border-dashed border-gray-300 p-12 text-center">
                <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-gray-100">
                  <BriefcaseIcon className="h-6 w-6 text-gray-400" aria-hidden="true" />
                </div>
                <h3 className="mt-2 text-sm font-medium text-gray-900">No application selected</h3>
                <p className="mt-1 text-sm text-gray-500">Select an application from the list to view details.</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </MainLayout>
  );
} 