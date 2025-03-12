'use client';

import React, { useState } from 'react';
import { 
  PencilIcon, 
  UserIcon, 
  AcademicCapIcon, 
  BriefcaseIcon, 
  CodeBracketIcon, 
  MapPinIcon,
  BuildingOfficeIcon,
  DocumentTextIcon,
  PaperClipIcon,
  PhotoIcon
} from '@heroicons/react/outline';
import MainLayout from '@/components/layout/MainLayout';

// Mock user data
const userData = {
  personal: {
    firstName: 'Alex',
    lastName: 'Johnson',
    title: 'Senior Software Engineer',
    email: 'alex.johnson@example.com',
    phone: '+1 (555) 123-4567',
    location: 'San Francisco, CA',
    about: 'Experienced software engineer with 8+ years building web and mobile applications. Passionate about user experience, performance optimization, and clean code. Looking for new opportunities in a fast-paced, innovative company.',
    linkedin: 'https://linkedin.com/in/alexjohnson',
    github: 'https://github.com/alexjohnson',
    website: 'https://alexjohnson.dev',
  },
  experience: [
    {
      id: 1,
      company: 'Tech Innovations Inc.',
      title: 'Senior Software Engineer',
      location: 'San Francisco, CA',
      type: 'Full-time',
      startDate: 'Jan 2020',
      endDate: 'Present',
      description: 'Led the development of a React-based dashboard for enterprise customers, improving user engagement by 35%. Mentored junior developers and implemented CI/CD pipelines that reduced deployment time by 50%.',
      skills: ['React', 'TypeScript', 'Node.js', 'AWS', 'Docker'],
    },
    {
      id: 2,
      company: 'WebSolutions Co.',
      title: 'Software Engineer',
      location: 'Boston, MA',
      type: 'Full-time',
      startDate: 'Mar 2017',
      endDate: 'Dec 2019',
      description: 'Developed and maintained multiple web applications using React, Redux, and Node.js. Implemented responsive designs and improved application performance by 40%.',
      skills: ['JavaScript', 'React', 'Redux', 'CSS', 'Node.js'],
    },
    {
      id: 3,
      company: 'StartupVision',
      title: 'Frontend Developer',
      location: 'Remote',
      type: 'Contract',
      startDate: 'Jun 2015',
      endDate: 'Feb 2017',
      description: 'Built interactive web applications for various clients. Worked with designers to implement responsive, cross-browser compatible websites.',
      skills: ['JavaScript', 'HTML', 'CSS', 'jQuery', 'Bootstrap'],
    },
  ],
  education: [
    {
      id: 1,
      institution: 'University of California, Berkeley',
      degree: 'Master of Computer Science',
      fieldOfStudy: 'Software Engineering',
      startDate: 'Aug 2013',
      endDate: 'May 2015',
      description: 'Focused on software engineering practices, algorithms, and machine learning. Graduated with honors.',
    },
    {
      id: 2,
      institution: 'Boston University',
      degree: 'Bachelor of Science',
      fieldOfStudy: 'Computer Science',
      startDate: 'Sep 2009',
      endDate: 'May 2013',
      description: 'Computer Science major with minor in Mathematics. Dean\'s List all semesters.',
    },
  ],
  skills: [
    { id: 1, name: 'JavaScript', level: 'Expert', endorsements: 28 },
    { id: 2, name: 'React', level: 'Expert', endorsements: 25 },
    { id: 3, name: 'TypeScript', level: 'Advanced', endorsements: 20 },
    { id: 4, name: 'Node.js', level: 'Advanced', endorsements: 18 },
    { id: 5, name: 'AWS', level: 'Intermediate', endorsements: 12 },
    { id: 6, name: 'GraphQL', level: 'Intermediate', endorsements: 10 },
    { id: 7, name: 'Docker', level: 'Intermediate', endorsements: 8 },
    { id: 8, name: 'Python', level: 'Beginner', endorsements: 5 },
  ],
  preferences: {
    jobTypes: ['Full-time', 'Contract'],
    locations: ['San Francisco, CA', 'Remote'],
    salary: '$120,000 - $160,000',
    industries: ['Technology', 'Finance', 'Healthcare'],
    companySize: ['Startup', 'Mid-size', 'Enterprise'],
    remotePreference: 'Remote or Hybrid',
  },
};

/**
 * Profile page component
 * Displays and allows editing of user profile information
 */
export default function ProfilePage() {
  const [activeTab, setActiveTab] = useState('personal');
  const [editMode, setEditMode] = useState(false);

  const tabClasses = (tabName: string) =>
    `px-4 py-2 text-sm font-medium ${
      activeTab === tabName
        ? 'bg-primary text-white rounded-md'
        : 'text-muted-foreground hover:text-foreground hover:bg-muted rounded-md'
    }`;

  return (
    <MainLayout>
      <div className="space-y-8">
        {/* Profile header */}
        <div className="rounded-lg bg-white p-6 shadow">
          <div className="md:flex md:items-center md:justify-between">
            <div className="flex items-center gap-6">
              <div className="h-24 w-24 rounded-full bg-primary/10 flex items-center justify-center text-primary">
                <UserIcon className="h-12 w-12" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-foreground">
                  {userData.personal.firstName} {userData.personal.lastName}
                </h1>
                <p className="text-lg text-muted-foreground">{userData.personal.title}</p>
                <div className="mt-1 flex items-center text-sm text-muted-foreground">
                  <MapPinIcon className="mr-1 h-4 w-4" />
                  {userData.personal.location}
                </div>
              </div>
            </div>
            <div className="mt-4 flex md:mt-0">
              <button
                type="button"
                className="inline-flex items-center rounded-md bg-primary px-3 py-2 text-sm font-medium text-white shadow-sm hover:bg-primary/90"
                onClick={() => setEditMode(!editMode)}
              >
                <PencilIcon className="mr-1.5 h-4 w-4" />
                {editMode ? 'View Profile' : 'Edit Profile'}
              </button>
            </div>
          </div>
        </div>

        {/* Profile tabs and content */}
        <div className="grid grid-cols-1 gap-8 md:grid-cols-4">
          {/* Tabs */}
          <div className="space-y-6">
            <nav className="flex flex-col space-y-1">
              <button
                onClick={() => setActiveTab('personal')}
                className={tabClasses('personal')}
              >
                <div className="flex items-center">
                  <UserIcon className="mr-2 h-4 w-4" />
                  Personal Information
                </div>
              </button>
              <button
                onClick={() => setActiveTab('experience')}
                className={tabClasses('experience')}
              >
                <div className="flex items-center">
                  <BriefcaseIcon className="mr-2 h-4 w-4" />
                  Experience
                </div>
              </button>
              <button
                onClick={() => setActiveTab('education')}
                className={tabClasses('education')}
              >
                <div className="flex items-center">
                  <AcademicCapIcon className="mr-2 h-4 w-4" />
                  Education
                </div>
              </button>
              <button
                onClick={() => setActiveTab('skills')}
                className={tabClasses('skills')}
              >
                <div className="flex items-center">
                  <CodeBracketIcon className="mr-2 h-4 w-4" />
                  Skills
                </div>
              </button>
              <button
                onClick={() => setActiveTab('preferences')}
                className={tabClasses('preferences')}
              >
                <div className="flex items-center">
                  <DocumentTextIcon className="mr-2 h-4 w-4" />
                  Job Preferences
                </div>
              </button>
            </nav>

            {/* Profile completeness */}
            <div className="rounded-lg bg-white p-4 shadow">
              <h3 className="text-sm font-medium">Profile Completeness</h3>
              <div className="mt-2">
                <div className="h-2 w-full rounded-full bg-gray-200">
                  <div className="h-2 rounded-full bg-primary" style={{ width: '85%' }} />
                </div>
                <div className="mt-2 text-xs text-muted-foreground">85% complete</div>
              </div>
              <div className="mt-3 text-xs">
                <p className="font-medium">Suggested improvements:</p>
                <ul className="mt-1 list-inside list-disc space-y-1 text-muted-foreground">
                  <li>Add a profile photo</li>
                  <li>Upload your resume</li>
                </ul>
              </div>
            </div>
          </div>

          {/* Content */}
          <div className="md:col-span-3">
            {/* Personal Information */}
            {activeTab === 'personal' && (
              <div className="rounded-lg bg-white p-6 shadow">
                <h2 className="text-lg font-medium">Personal Information</h2>
                
                {editMode ? (
                  <div className="mt-4 space-y-4">
                    <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
                      <div>
                        <label htmlFor="firstName" className="block text-sm font-medium text-foreground">
                          First Name
                        </label>
                        <input
                          type="text"
                          id="firstName"
                          className="mt-1 block w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
                          defaultValue={userData.personal.firstName}
                        />
                      </div>
                      <div>
                        <label htmlFor="lastName" className="block text-sm font-medium text-foreground">
                          Last Name
                        </label>
                        <input
                          type="text"
                          id="lastName"
                          className="mt-1 block w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
                          defaultValue={userData.personal.lastName}
                        />
                      </div>
                      <div>
                        <label htmlFor="title" className="block text-sm font-medium text-foreground">
                          Professional Title
                        </label>
                        <input
                          type="text"
                          id="title"
                          className="mt-1 block w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
                          defaultValue={userData.personal.title}
                        />
                      </div>
                      <div>
                        <label htmlFor="location" className="block text-sm font-medium text-foreground">
                          Location
                        </label>
                        <input
                          type="text"
                          id="location"
                          className="mt-1 block w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
                          defaultValue={userData.personal.location}
                        />
                      </div>
                      <div>
                        <label htmlFor="email" className="block text-sm font-medium text-foreground">
                          Email
                        </label>
                        <input
                          type="email"
                          id="email"
                          className="mt-1 block w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
                          defaultValue={userData.personal.email}
                        />
                      </div>
                      <div>
                        <label htmlFor="phone" className="block text-sm font-medium text-foreground">
                          Phone
                        </label>
                        <input
                          type="text"
                          id="phone"
                          className="mt-1 block w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
                          defaultValue={userData.personal.phone}
                        />
                      </div>
                    </div>
                    <div>
                      <label htmlFor="about" className="block text-sm font-medium text-foreground">
                        About
                      </label>
                      <textarea
                        id="about"
                        rows={4}
                        className="mt-1 block w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
                        defaultValue={userData.personal.about}
                      />
                    </div>
                    <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
                      <div>
                        <label htmlFor="linkedin" className="block text-sm font-medium text-foreground">
                          LinkedIn
                        </label>
                        <input
                          type="url"
                          id="linkedin"
                          className="mt-1 block w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
                          defaultValue={userData.personal.linkedin}
                        />
                      </div>
                      <div>
                        <label htmlFor="github" className="block text-sm font-medium text-foreground">
                          GitHub
                        </label>
                        <input
                          type="url"
                          id="github"
                          className="mt-1 block w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
                          defaultValue={userData.personal.github}
                        />
                      </div>
                      <div>
                        <label htmlFor="website" className="block text-sm font-medium text-foreground">
                          Personal Website
                        </label>
                        <input
                          type="url"
                          id="website"
                          className="mt-1 block w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
                          defaultValue={userData.personal.website}
                        />
                      </div>
                    </div>
                    <div className="flex flex-col space-y-4 sm:flex-row sm:space-x-4 sm:space-y-0">
                      <div>
                        <button
                          type="button"
                          className="inline-flex items-center rounded-md bg-muted px-3 py-2 text-sm font-medium text-foreground shadow-sm hover:bg-muted/80"
                        >
                          <PhotoIcon className="mr-1.5 h-4 w-4" />
                          Upload Photo
                        </button>
                      </div>
                      <div>
                        <button
                          type="button"
                          className="inline-flex items-center rounded-md bg-muted px-3 py-2 text-sm font-medium text-foreground shadow-sm hover:bg-muted/80"
                        >
                          <PaperClipIcon className="mr-1.5 h-4 w-4" />
                          Upload Resume
                        </button>
                      </div>
                    </div>
                    <div className="flex justify-end">
                      <button
                        type="button"
                        className="inline-flex items-center rounded-md bg-primary px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-primary/90"
                      >
                        Save Changes
                      </button>
                    </div>
                  </div>
                ) : (
                  <div className="mt-4 space-y-6">
                    <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
                      <div>
                        <h3 className="text-sm font-medium text-muted-foreground">Email</h3>
                        <p className="mt-1 text-sm">{userData.personal.email}</p>
                      </div>
                      <div>
                        <h3 className="text-sm font-medium text-muted-foreground">Phone</h3>
                        <p className="mt-1 text-sm">{userData.personal.phone}</p>
                      </div>
                      <div>
                        <h3 className="text-sm font-medium text-muted-foreground">Location</h3>
                        <p className="mt-1 text-sm">{userData.personal.location}</p>
                      </div>
                    </div>
                    <div>
                      <h3 className="text-sm font-medium text-muted-foreground">About</h3>
                      <p className="mt-1 text-sm whitespace-pre-line">{userData.personal.about}</p>
                    </div>
                    <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
                      <div>
                        <h3 className="text-sm font-medium text-muted-foreground">LinkedIn</h3>
                        <a
                          href={userData.personal.linkedin}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="mt-1 block text-sm text-primary hover:underline"
                        >
                          {userData.personal.linkedin.replace('https://', '')}
                        </a>
                      </div>
                      <div>
                        <h3 className="text-sm font-medium text-muted-foreground">GitHub</h3>
                        <a
                          href={userData.personal.github}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="mt-1 block text-sm text-primary hover:underline"
                        >
                          {userData.personal.github.replace('https://', '')}
                        </a>
                      </div>
                      <div>
                        <h3 className="text-sm font-medium text-muted-foreground">Personal Website</h3>
                        <a
                          href={userData.personal.website}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="mt-1 block text-sm text-primary hover:underline"
                        >
                          {userData.personal.website.replace('https://', '')}
                        </a>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            )}

            {/* Experience */}
            {activeTab === 'experience' && (
              <div className="rounded-lg bg-white p-6 shadow">
                <div className="mb-6 flex items-center justify-between">
                  <h2 className="text-lg font-medium">Work Experience</h2>
                  {editMode && (
                    <button
                      type="button"
                      className="inline-flex items-center rounded-md bg-primary px-3 py-1.5 text-sm font-medium text-white shadow-sm hover:bg-primary/90"
                    >
                      Add Experience
                    </button>
                  )}
                </div>
                <div className="space-y-6">
                  {userData.experience.map((exp) => (
                    <div key={exp.id} className="relative border-l-2 border-primary/30 pl-5 pb-5">
                      <div className="absolute -left-[9px] top-0 h-4 w-4 rounded-full border-2 border-primary bg-white" />
                      <div className="flex justify-between">
                        <div>
                          <h3 className="text-base font-medium">{exp.title}</h3>
                          <div className="flex items-center text-sm">
                            <BuildingOfficeIcon className="mr-1 h-4 w-4 text-muted-foreground" />
                            <span>{exp.company}</span>
                            <span className="mx-1.5 text-muted-foreground">•</span>
                            <span>{exp.type}</span>
                          </div>
                          <div className="mt-1 text-sm text-muted-foreground">
                            <span>{exp.startDate} - {exp.endDate}</span>
                            <span className="mx-1.5">•</span>
                            <span>{exp.location}</span>
                          </div>
                        </div>
                        {editMode && (
                          <button className="text-muted-foreground hover:text-foreground">
                            <PencilIcon className="h-4 w-4" />
                          </button>
                        )}
                      </div>
                      <p className="mt-2 text-sm">{exp.description}</p>
                      <div className="mt-3 flex flex-wrap gap-2">
                        {exp.skills.map((skill, idx) => (
                          <span
                            key={idx}
                            className="inline-flex items-center rounded-full bg-muted px-2.5 py-0.5 text-xs font-medium"
                          >
                            {skill}
                          </span>
                        ))}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Education */}
            {activeTab === 'education' && (
              <div className="rounded-lg bg-white p-6 shadow">
                <div className="mb-6 flex items-center justify-between">
                  <h2 className="text-lg font-medium">Education</h2>
                  {editMode && (
                    <button
                      type="button"
                      className="inline-flex items-center rounded-md bg-primary px-3 py-1.5 text-sm font-medium text-white shadow-sm hover:bg-primary/90"
                    >
                      Add Education
                    </button>
                  )}
                </div>
                <div className="space-y-6">
                  {userData.education.map((edu) => (
                    <div key={edu.id} className="relative border-l-2 border-primary/30 pl-5 pb-5">
                      <div className="absolute -left-[9px] top-0 h-4 w-4 rounded-full border-2 border-primary bg-white" />
                      <div className="flex justify-between">
                        <div>
                          <h3 className="text-base font-medium">{edu.institution}</h3>
                          <div className="text-sm">
                            <span>{edu.degree}, {edu.fieldOfStudy}</span>
                          </div>
                          <div className="mt-1 text-sm text-muted-foreground">
                            <span>{edu.startDate} - {edu.endDate}</span>
                          </div>
                        </div>
                        {editMode && (
                          <button className="text-muted-foreground hover:text-foreground">
                            <PencilIcon className="h-4 w-4" />
                          </button>
                        )}
                      </div>
                      <p className="mt-2 text-sm">{edu.description}</p>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Skills */}
            {activeTab === 'skills' && (
              <div className="rounded-lg bg-white p-6 shadow">
                <div className="mb-6 flex items-center justify-between">
                  <h2 className="text-lg font-medium">Skills</h2>
                  {editMode && (
                    <button
                      type="button"
                      className="inline-flex items-center rounded-md bg-primary px-3 py-1.5 text-sm font-medium text-white shadow-sm hover:bg-primary/90"
                    >
                      Add Skill
                    </button>
                  )}
                </div>
                <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
                  {userData.skills.map((skill) => (
                    <div
                      key={skill.id}
                      className="flex items-center justify-between rounded-lg border border-input p-3"
                    >
                      <div>
                        <div className="flex items-center">
                          <h3 className="text-sm font-medium">{skill.name}</h3>
                          <span className="ml-2 inline-flex items-center rounded-full bg-muted px-2 py-0.5 text-xs font-medium">
                            {skill.level}
                          </span>
                        </div>
                        <p className="text-xs text-muted-foreground">{skill.endorsements} endorsements</p>
                      </div>
                      {editMode && (
                        <div className="flex items-center">
                          <button className="text-muted-foreground hover:text-foreground">
                            <PencilIcon className="h-4 w-4" />
                          </button>
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Job Preferences */}
            {activeTab === 'preferences' && (
              <div className="rounded-lg bg-white p-6 shadow">
                <div className="mb-6 flex items-center justify-between">
                  <h2 className="text-lg font-medium">Job Preferences</h2>
                </div>
                {editMode ? (
                  <div className="space-y-4">
                    <div>
                      <label className="block text-sm font-medium text-foreground">Job Types</label>
                      <div className="mt-2 flex flex-wrap gap-2">
                        {['Full-time', 'Part-time', 'Contract', 'Internship', 'Temporary'].map((type) => (
                          <label
                            key={type}
                            className={`inline-flex items-center rounded-full px-3 py-1 text-sm ${
                              userData.preferences.jobTypes.includes(type)
                                ? 'bg-primary text-white'
                                : 'bg-muted text-foreground'
                            }`}
                          >
                            <input
                              type="checkbox"
                              defaultChecked={userData.preferences.jobTypes.includes(type)}
                              className="sr-only"
                            />
                            {type}
                          </label>
                        ))}
                      </div>
                    </div>
                    <div>
                      <label htmlFor="salary" className="block text-sm font-medium text-foreground">
                        Expected Salary
                      </label>
                      <input
                        type="text"
                        id="salary"
                        className="mt-1 block w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
                        defaultValue={userData.preferences.salary}
                      />
                    </div>
                    <div>
                      <label htmlFor="remotePreference" className="block text-sm font-medium text-foreground">
                        Remote Work Preference
                      </label>
                      <select
                        id="remotePreference"
                        className="mt-1 block w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
                        defaultValue={userData.preferences.remotePreference}
                      >
                        <option>On-site only</option>
                        <option>Remote only</option>
                        <option>Hybrid preferred</option>
                        <option>Remote or Hybrid</option>
                        <option>Open to all options</option>
                      </select>
                    </div>
                    <div className="flex justify-end">
                      <button
                        type="button"
                        className="inline-flex items-center rounded-md bg-primary px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-primary/90"
                      >
                        Save Preferences
                      </button>
                    </div>
                  </div>
                ) : (
                  <div className="space-y-4">
                    <div>
                      <h3 className="text-sm font-medium text-muted-foreground">Job Types</h3>
                      <div className="mt-1 flex flex-wrap gap-2">
                        {userData.preferences.jobTypes.map((type) => (
                          <span
                            key={type}
                            className="inline-flex items-center rounded-full bg-muted px-2.5 py-0.5 text-xs font-medium"
                          >
                            {type}
                          </span>
                        ))}
                      </div>
                    </div>
                    <div>
                      <h3 className="text-sm font-medium text-muted-foreground">Locations</h3>
                      <div className="mt-1 flex flex-wrap gap-2">
                        {userData.preferences.locations.map((location) => (
                          <span
                            key={location}
                            className="inline-flex items-center rounded-full bg-muted px-2.5 py-0.5 text-xs font-medium"
                          >
                            <MapPinIcon className="mr-1 h-3 w-3" />
                            {location}
                          </span>
                        ))}
                      </div>
                    </div>
                    <div>
                      <h3 className="text-sm font-medium text-muted-foreground">Expected Salary</h3>
                      <p className="mt-1 text-sm">{userData.preferences.salary}</p>
                    </div>
                    <div>
                      <h3 className="text-sm font-medium text-muted-foreground">Industries</h3>
                      <div className="mt-1 flex flex-wrap gap-2">
                        {userData.preferences.industries.map((industry) => (
                          <span
                            key={industry}
                            className="inline-flex items-center rounded-full bg-muted px-2.5 py-0.5 text-xs font-medium"
                          >
                            {industry}
                          </span>
                        ))}
                      </div>
                    </div>
                    <div>
                      <h3 className="text-sm font-medium text-muted-foreground">Company Size</h3>
                      <div className="mt-1 flex flex-wrap gap-2">
                        {userData.preferences.companySize.map((size) => (
                          <span
                            key={size}
                            className="inline-flex items-center rounded-full bg-muted px-2.5 py-0.5 text-xs font-medium"
                          >
                            {size}
                          </span>
                        ))}
                      </div>
                    </div>
                    <div>
                      <h3 className="text-sm font-medium text-muted-foreground">Remote Work Preference</h3>
                      <p className="mt-1 text-sm">{userData.preferences.remotePreference}</p>
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      </div>
    </MainLayout>
  );
} 