'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { 
  MagnifyingGlassIcon,
  BriefcaseIcon,
  MapPinIcon,
  ClockIcon,
  AdjustmentsHorizontalIcon,
  BookmarkIcon
} from '@heroicons/react/outline';
import MainLayout from '@/components/layout/MainLayout';

// Mock job data
const jobs = [
  {
    id: 1,
    title: 'Senior Software Engineer',
    company: 'Tech Innovations Inc.',
    location: 'San Francisco, CA (Remote)',
    salary: '$120,000 - $160,000',
    matchPercentage: 92,
    postedAt: '2 days ago',
    description: 'We are looking for a skilled senior software engineer to join our growing team. You will be responsible for developing and maintaining high-quality applications.',
    skills: ['JavaScript', 'React', 'Node.js', 'AWS', 'GraphQL', 'TypeScript'],
    isSaved: false,
  },
  {
    id: 2,
    title: 'Product Manager',
    company: 'Future Products Co.',
    location: 'New York, NY (Hybrid)',
    salary: '$110,000 - $140,000',
    matchPercentage: 87,
    postedAt: '1 day ago',
    description: 'Seeking an experienced product manager to lead our product development initiatives and work closely with engineering, design, and marketing teams.',
    skills: ['Product Strategy', 'Agile', 'User Research', 'Roadmapping', 'A/B Testing', 'Data Analysis'],
    isSaved: true,
  },
  {
    id: 3,
    title: 'UX/UI Designer',
    company: 'Creative Solutions Ltd.',
    location: 'Boston, MA (On-site)',
    salary: '$90,000 - $120,000',
    matchPercentage: 84,
    postedAt: '3 days ago',
    description: 'Join our design team to create beautiful, intuitive user experiences for our flagship products. You\'ll work on all aspects of the design process from research to implementation.',
    skills: ['Figma', 'User Testing', 'Wireframing', 'Design Systems', 'Prototyping', 'Visual Design'],
    isSaved: false,
  },
  {
    id: 4,
    title: 'DevOps Engineer',
    company: 'Cloud Systems Inc.',
    location: 'Remote',
    salary: '$115,000 - $145,000',
    matchPercentage: 78,
    postedAt: '5 days ago',
    description: 'Looking for a DevOps engineer to improve our CI/CD pipelines, infrastructure, and cloud architecture. Experience with Kubernetes and AWS is essential.',
    skills: ['AWS', 'Kubernetes', 'Docker', 'CI/CD', 'Terraform', 'Linux'],
    isSaved: false,
  },
  {
    id: 5,
    title: 'Full Stack Developer',
    company: 'Innovative Apps LLC',
    location: 'Chicago, IL (Hybrid)',
    salary: '$100,000 - $130,000',
    matchPercentage: 89,
    postedAt: '2 days ago',
    description: 'Join our engineering team to build robust web applications. You\'ll work on both frontend and backend development using modern technologies.',
    skills: ['JavaScript', 'React', 'Node.js', 'MongoDB', 'Express', 'GraphQL'],
    isSaved: true,
  },
];

// Filter options
const filters = {
  jobType: [
    { id: 'full-time', name: 'Full-time' },
    { id: 'part-time', name: 'Part-time' },
    { id: 'contract', name: 'Contract' },
    { id: 'internship', name: 'Internship' },
  ],
  location: [
    { id: 'remote', name: 'Remote' },
    { id: 'hybrid', name: 'Hybrid' },
    { id: 'on-site', name: 'On-site' },
  ],
  experience: [
    { id: 'entry', name: 'Entry Level' },
    { id: 'mid', name: 'Mid Level' },
    { id: 'senior', name: 'Senior Level' },
    { id: 'executive', name: 'Executive Level' },
  ],
  salary: [
    { id: '0-50', name: '$0 - $50,000' },
    { id: '50-100', name: '$50,000 - $100,000' },
    { id: '100-150', name: '$100,000 - $150,000' },
    { id: '150-plus', name: '$150,000+' },
  ],
};

// Define the filter state type
interface FilterState {
  jobType: string[];
  location: string[];
  experience: string[];
  salary: string[];
  [key: string]: string[]; // Index signature to allow string indexing
}

/**
 * Jobs listing page component
 * Shows available job listings with filtering and sorting options
 */
export default function JobsPage() {
  const [searchTerm, setSearchTerm] = useState('');
  const [showFilters, setShowFilters] = useState(false);
  const [selectedFilters, setSelectedFilters] = useState<FilterState>({
    jobType: [],
    location: [],
    experience: [],
    salary: [],
  });

  // Toggle the saved state of a job
  const toggleSaveJob = (jobId: number) => {
    // In a real app, this would call an API to save/unsave a job
    console.log(`Toggling save state for job ${jobId}`);
  };

  // Filter change handler
  const handleFilterChange = (category: string, id: string) => {
    setSelectedFilters((prev) => {
      const currentFilters = [...prev[category]];
      if (currentFilters.includes(id)) {
        return {
          ...prev,
          [category]: currentFilters.filter((filterId) => filterId !== id),
        };
      } else {
        return {
          ...prev,
          [category]: [...currentFilters, id],
        };
      }
    });
  };

  // Clear all filters
  const clearFilters = () => {
    setSelectedFilters({
      jobType: [],
      location: [],
      experience: [],
      salary: [],
    });
  };

  return (
    <MainLayout>
      <div className="space-y-6">
        {/* Page header */}
        <div>
          <h1 className="text-2xl font-bold tracking-tight">Jobs</h1>
          <p className="mt-2 text-muted-foreground">
            Discover job opportunities that match your skills and preferences.
          </p>
        </div>

        {/* Search and filter bar */}
        <div className="rounded-lg bg-white p-4 shadow sm:flex sm:items-center sm:justify-between">
          <div className="relative flex-grow">
            <div className="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
              <MagnifyingGlassIcon className="h-5 w-5 text-muted-foreground" aria-hidden="true" />
            </div>
            <input
              type="text"
              placeholder="Search for jobs, skills, or companies"
              className="block w-full rounded-md border border-input bg-background py-2 pl-10 pr-3 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>
          <div className="mt-3 flex sm:ml-4 sm:mt-0">
            <button
              type="button"
              className="inline-flex items-center rounded-md bg-primary px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-primary/90"
              onClick={() => setShowFilters(!showFilters)}
            >
              <AdjustmentsHorizontalIcon className="-ml-0.5 mr-1.5 h-5 w-5" aria-hidden="true" />
              Filters
            </button>
          </div>
        </div>

        {/* Filters section */}
        {showFilters && (
          <div className="rounded-lg bg-white p-4 shadow">
            <div className="flex items-center justify-between">
              <h2 className="text-lg font-medium">Filters</h2>
              <button
                type="button"
                className="text-sm text-primary hover:underline"
                onClick={clearFilters}
              >
                Clear all
              </button>
            </div>
            <div className="mt-4 grid grid-cols-1 gap-y-6 sm:grid-cols-2 lg:grid-cols-4">
              {/* Job Type Filter */}
              <div>
                <h3 className="text-sm font-medium text-gray-700">Job Type</h3>
                <div className="mt-2 space-y-2">
                  {filters.jobType.map((option) => (
                    <div key={option.id} className="flex items-center">
                      <input
                        id={`job-type-${option.id}`}
                        name="job-type"
                        type="checkbox"
                        checked={selectedFilters.jobType.includes(option.id)}
                        onChange={() => handleFilterChange('jobType', option.id)}
                        className="h-4 w-4 rounded border-gray-300 text-primary focus:ring-primary"
                      />
                      <label
                        htmlFor={`job-type-${option.id}`}
                        className="ml-2 text-sm text-gray-700"
                      >
                        {option.name}
                      </label>
                    </div>
                  ))}
                </div>
              </div>

              {/* Location Filter */}
              <div>
                <h3 className="text-sm font-medium text-gray-700">Location</h3>
                <div className="mt-2 space-y-2">
                  {filters.location.map((option) => (
                    <div key={option.id} className="flex items-center">
                      <input
                        id={`location-${option.id}`}
                        name="location"
                        type="checkbox"
                        checked={selectedFilters.location.includes(option.id)}
                        onChange={() => handleFilterChange('location', option.id)}
                        className="h-4 w-4 rounded border-gray-300 text-primary focus:ring-primary"
                      />
                      <label
                        htmlFor={`location-${option.id}`}
                        className="ml-2 text-sm text-gray-700"
                      >
                        {option.name}
                      </label>
                    </div>
                  ))}
                </div>
              </div>

              {/* Experience Level Filter */}
              <div>
                <h3 className="text-sm font-medium text-gray-700">Experience Level</h3>
                <div className="mt-2 space-y-2">
                  {filters.experience.map((option) => (
                    <div key={option.id} className="flex items-center">
                      <input
                        id={`experience-${option.id}`}
                        name="experience"
                        type="checkbox"
                        checked={selectedFilters.experience.includes(option.id)}
                        onChange={() => handleFilterChange('experience', option.id)}
                        className="h-4 w-4 rounded border-gray-300 text-primary focus:ring-primary"
                      />
                      <label
                        htmlFor={`experience-${option.id}`}
                        className="ml-2 text-sm text-gray-700"
                      >
                        {option.name}
                      </label>
                    </div>
                  ))}
                </div>
              </div>

              {/* Salary Range Filter */}
              <div>
                <h3 className="text-sm font-medium text-gray-700">Salary Range</h3>
                <div className="mt-2 space-y-2">
                  {filters.salary.map((option) => (
                    <div key={option.id} className="flex items-center">
                      <input
                        id={`salary-${option.id}`}
                        name="salary"
                        type="checkbox"
                        checked={selectedFilters.salary.includes(option.id)}
                        onChange={() => handleFilterChange('salary', option.id)}
                        className="h-4 w-4 rounded border-gray-300 text-primary focus:ring-primary"
                      />
                      <label
                        htmlFor={`salary-${option.id}`}
                        className="ml-2 text-sm text-gray-700"
                      >
                        {option.name}
                      </label>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Jobs list */}
        <div className="space-y-4">
          {jobs.map((job) => (
            <div
              key={job.id}
              className="overflow-hidden rounded-lg bg-white shadow transition-all hover:ring-2 hover:ring-primary/50"
            >
              <div className="p-6">
                <div className="flex items-start justify-between">
                  <div className="min-w-0 flex-1">
                    <Link 
                      href={`/jobs/${job.id}`}
                      className="text-lg font-semibold leading-tight text-foreground hover:text-primary hover:underline"
                    >
                      {job.title}
                    </Link>
                    <div className="mt-1 flex flex-wrap items-center text-sm text-muted-foreground">
                      <span>{job.company}</span>
                      <span className="mx-1.5">•</span>
                      <span className="inline-flex items-center">
                        <MapPinIcon className="mr-1 h-4 w-4" />
                        {job.location}
                      </span>
                      <span className="mx-1.5">•</span>
                      <span className="inline-flex items-center">
                        <ClockIcon className="mr-1 h-4 w-4" />
                        {job.postedAt}
                      </span>
                    </div>
                    <p className="mt-2 line-clamp-2 text-sm text-muted-foreground">
                      {job.description}
                    </p>
                    <div className="mt-3 flex flex-wrap gap-2">
                      {job.skills.map((skill, idx) => (
                        <span
                          key={idx}
                          className="inline-flex items-center rounded-full bg-muted px-2.5 py-0.5 text-xs font-medium"
                        >
                          {skill}
                        </span>
                      ))}
                    </div>
                  </div>
                  <div className="ml-4 flex flex-col items-end">
                    <button
                      onClick={() => toggleSaveJob(job.id)}
                      className={`rounded-full p-1.5 ${
                        job.isSaved ? 'text-primary' : 'text-muted-foreground hover:text-foreground'
                      }`}
                    >
                      <BookmarkIcon className="h-5 w-5" aria-hidden="true" />
                      <span className="sr-only">{job.isSaved ? 'Unsave job' : 'Save job'}</span>
                    </button>
                    <span className="mt-2 inline-flex items-center rounded-full bg-emerald-50 px-2.5 py-0.5 text-xs font-medium text-emerald-700">
                      {job.matchPercentage}% match
                    </span>
                  </div>
                </div>
                <div className="mt-4 flex items-center justify-between">
                  <div className="text-sm font-medium text-foreground">{job.salary}</div>
                  <div>
                    <Link
                      href={`/jobs/${job.id}`}
                      className="inline-flex items-center rounded-md bg-primary px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-primary/90"
                    >
                      View Details
                    </Link>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </MainLayout>
  );
} 