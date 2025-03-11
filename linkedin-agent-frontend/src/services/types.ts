// Auth types
export interface User {
  id: string;
  email: string;
  firstName: string;
  lastName: string;
  role: 'user' | 'admin';
  isEmailVerified: boolean;
  createdAt: string;
  updatedAt: string;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface LoginResponse {
  user: User;
  token: string;
}

export interface RegisterRequest {
  email: string;
  password: string;
  firstName: string;
  lastName: string;
}

export interface RegisterResponse {
  user: User;
  token: string;
}

export interface ForgotPasswordRequest {
  email: string;
}

export interface ResetPasswordRequest {
  token: string;
  password: string;
}

export interface ChangePasswordRequest {
  currentPassword: string;
  newPassword: string;
}

export interface VerifyEmailRequest {
  token: string;
}

export interface UpdateProfileRequest {
  firstName?: string;
  lastName?: string;
  email?: string;
}

// Profile types
export interface Profile {
  id: string;
  userId: string;
  headline: string;
  summary: string;
  industry: string;
  location: string;
  currentPosition: string;
  education: Education[];
  experience: Experience[];
  skills: Skill[];
  languages: Language[];
  certifications: Certification[];
  projects: Project[];
}

export interface Education {
  id: string;
  school: string;
  degree: string;
  fieldOfStudy: string;
  startDate: string;
  endDate: string | null;
  description: string;
}

export interface Experience {
  id: string;
  company: string;
  title: string;
  location: string;
  startDate: string;
  endDate: string | null;
  description: string;
  isCurrentPosition: boolean;
}

export interface Skill {
  id: string;
  name: string;
  endorsements: number;
  level: 'beginner' | 'intermediate' | 'advanced' | 'expert';
}

export interface Language {
  id: string;
  name: string;
  proficiency: 'elementary' | 'limited_working' | 'professional_working' | 'full_professional' | 'native';
}

export interface Certification {
  id: string;
  name: string;
  organization: string;
  issueDate: string;
  expirationDate: string | null;
  credentialId: string;
  credentialUrl: string;
}

export interface Project {
  id: string;
  name: string;
  description: string;
  startDate: string;
  endDate: string | null;
  url: string;
}

export interface ProfileUpdateRequest {
  headline?: string;
  summary?: string;
  industry?: string;
  location?: string;
  currentPosition?: string;
}

export interface ProfileAnalysis {
  strengths: string[];
  weaknesses: string[];
  opportunities: string[];
  recommendations: ProfileRecommendation[];
  skillGaps: SkillGap[];
  industryComparison: IndustryComparison;
}

export interface ProfileRecommendation {
  type: 'summary' | 'experience' | 'education' | 'skills' | 'projects';
  recommendation: string;
  priority: 'low' | 'medium' | 'high';
}

export interface SkillGap {
  skill: string;
  relevance: number;
  jobPostings: number;
  resources: {
    title: string;
    url: string;
    type: 'course' | 'article' | 'video' | 'book';
  }[];
}

export interface IndustryComparison {
  industry: string;
  averageExperience: number;
  topSkills: {
    skill: string;
    percentage: number;
  }[];
  educationLevel: {
    level: string;
    percentage: number;
  }[];
}

// Job types
export interface Job {
  id: string;
  title: string;
  company: string;
  location: string;
  description: string;
  requirements: string;
  salary: string | null;
  employmentType: string;
  experienceLevel: string;
  postedDate: string;
  applicationDeadline: string | null;
  url: string;
  matchScore: number;
  skills: string[];
  isSaved: boolean;
  isApplied: boolean;
  source: string;
}

export interface JobSearchParams {
  query?: string;
  location?: string;
  employmentType?: string;
  experienceLevel?: string;
  postedWithin?: string;
  salary?: string;
  remote?: boolean;
  page?: number;
  limit?: number;
  sortBy?: string;
  sortOrder?: 'asc' | 'desc';
}

export interface JobSearchResponse {
  jobs: Job[];
  total: number;
  page: number;
  limit: number;
  totalPages: number;
}

export interface JobMatchAnalysis {
  overallScore: number;
  skillsMatch: {
    score: number;
    matching: string[];
    missing: string[];
  };
  experienceMatch: {
    score: number;
    relevantExperience: string[];
  };
  educationMatch: {
    score: number;
    relevantEducation: string[];
  };
  locationMatch: {
    score: number;
    distance: number;
    isRemote: boolean;
  };
  recommendations: {
    skills: string[];
    resume: string;
    coverLetter: string;
  };
}

// Application types
export interface Application {
  id: string;
  userId: string;
  jobId: string;
  job: Job;
  status: ApplicationStatus;
  appliedDate: string;
  resumeUrl: string | null;
  coverLetterUrl: string | null;
  notes: string;
  followUpDate: string | null;
  interviewDate: string | null;
  interviewNotes: string | null;
  offerAmount: number | null;
  offerDetails: string | null;
  rejectionReason: string | null;
  createdAt: string;
  updatedAt: string;
  statusHistory: StatusHistoryItem[];
}

export type ApplicationStatus =
  | 'applied'
  | 'screening'
  | 'interview'
  | 'technical'
  | 'offer'
  | 'accepted'
  | 'rejected'
  | 'withdrawn';

export interface StatusHistoryItem {
  id: string;
  status: ApplicationStatus;
  date: string;
  notes: string | null;
}

export interface ApplicationCreateRequest {
  jobId: string;
  status: ApplicationStatus;
  appliedDate: string;
  resumeUrl?: string;
  coverLetterUrl?: string;
  notes?: string;
}

export interface ApplicationUpdateRequest {
  status?: ApplicationStatus;
  appliedDate?: string;
  resumeUrl?: string;
  coverLetterUrl?: string;
  notes?: string;
  followUpDate?: string | null;
  interviewDate?: string | null;
  interviewNotes?: string | null;
  offerAmount?: number | null;
  offerDetails?: string | null;
  rejectionReason?: string | null;
}

export interface ApplicationSearchParams {
  status?: ApplicationStatus;
  startDate?: string;
  endDate?: string;
  company?: string;
  page?: number;
  limit?: number;
  sortBy?: string;
  sortOrder?: 'asc' | 'desc';
}

export interface ApplicationSearchResponse {
  applications: Application[];
  total: number;
  page: number;
  limit: number;
  totalPages: number;
}

export interface ApplicationStats {
  totalApplications: number;
  byStatus: Record<ApplicationStatus, number>;
  byMonth: {
    month: string;
    count: number;
  }[];
  responseRate: number;
  interviewRate: number;
  offerRate: number;
  averageTimeToResponse: number;
}

// Networking types
export interface Connection {
  id: string;
  userId: string;
  name: string;
  title: string;
  company: string;
  email: string;
  phone: string;
  linkedInUrl: string;
  notes: string;
  tags: string[];
  lastContactDate: string | null;
  nextContactDate: string | null;
  relationshipStrength: number;
  createdAt: string;
  updatedAt: string;
  interactions: Interaction[];
}

export interface Interaction {
  id: string;
  connectionId: string;
  type: InteractionType;
  date: string;
  notes: string;
  outcome: string;
  followUpDate: string | null;
  createdAt: string;
  updatedAt: string;
}

export type InteractionType =
  | 'email'
  | 'call'
  | 'meeting'
  | 'coffee'
  | 'lunch'
  | 'event'
  | 'linkedin'
  | 'other';

export interface ConnectionCreateRequest {
  name: string;
  title?: string;
  company?: string;
  email?: string;
  phone?: string;
  linkedInUrl?: string;
  notes?: string;
  tags?: string[];
}

export interface ConnectionUpdateRequest {
  name?: string;
  title?: string;
  company?: string;
  email?: string;
  phone?: string;
  linkedInUrl?: string;
  notes?: string;
  tags?: string[];
  lastContactDate?: string | null;
  nextContactDate?: string | null;
  relationshipStrength?: number;
}

export interface InteractionCreateRequest {
  connectionId: string;
  type: InteractionType;
  date: string;
  notes?: string;
  outcome?: string;
  followUpDate?: string | null;
}

export interface InteractionUpdateRequest {
  type?: InteractionType;
  date?: string;
  notes?: string;
  outcome?: string;
  followUpDate?: string | null;
}

export interface ConnectionSearchParams {
  query?: string;
  tags?: string[];
  company?: string;
  lastContactAfter?: string;
  lastContactBefore?: string;
  page?: number;
  limit?: number;
  sortBy?: 'name' | 'lastContactDate' | 'relationshipStrength' | 'createdAt';
  sortOrder?: 'asc' | 'desc';
}

export interface ConnectionSearchResponse {
  connections: Connection[];
  total: number;
  page: number;
  limit: number;
  totalPages: number;
}

export interface NetworkingStats {
  totalConnections: number;
  newConnectionsThisMonth: number;
  interactionsByType: Record<InteractionType, number>;
  interactionsByMonth: {
    month: string;
    count: number;
  }[];
  topCompanies: {
    company: string;
    count: number;
  }[];
  connectionsByTag: {
    tag: string;
    count: number;
  }[];
}

export interface MessageTemplate {
  id: string;
  name: string;
  subject: string;
  body: string;
  type: 'introduction' | 'follow-up' | 'thank-you' | 'request' | 'other';
  createdAt: string;
  updatedAt: string;
}

export interface MessageTemplateCreateRequest {
  name: string;
  subject: string;
  body: string;
  type: 'introduction' | 'follow-up' | 'thank-you' | 'request' | 'other';
}

export interface MessageTemplateUpdateRequest {
  name?: string;
  subject?: string;
  body?: string;
  type?: 'introduction' | 'follow-up' | 'thank-you' | 'request' | 'other';
}

// Analytics types
export interface DashboardStats {
  jobMetrics: {
    totalApplications: number;
    activeApplications: number;
    interviewsScheduled: number;
    offersReceived: number;
    applicationsByStatus: Record<string, number>;
    applicationsByMonth: {
      month: string;
      count: number;
    }[];
    responseRate: number;
    interviewRate: number;
    offerRate: number;
  };
  networkingMetrics: {
    totalConnections: number;
    newConnectionsThisMonth: number;
    pendingFollowUps: number;
    interactionsByType: Record<string, number>;
    interactionsByMonth: {
      month: string;
      count: number;
    }[];
  };
  profileMetrics: {
    profileStrength: number;
    profileViewsThisMonth: number;
    skillsEndorsed: number;
    profileCompletionPercentage: number;
    profileCompletionBySection: Record<string, number>;
  };
  marketInsights: {
    topInDemandSkills: {
      skill: string;
      demand: number;
    }[];
    averageSalaryByRole: {
      role: string;
      salary: number;
    }[];
    jobGrowthByIndustry: {
      industry: string;
      growth: number;
    }[];
    topHiringCompanies: {
      company: string;
      openings: number;
    }[];
  };
}

export interface ActivityLog {
  id: string;
  userId: string;
  type: 'application' | 'networking' | 'profile' | 'system';
  action: string;
  details: Record<string, any>;
  timestamp: string;
}

export interface ActivityLogSearchParams {
  type?: 'application' | 'networking' | 'profile' | 'system';
  startDate?: string;
  endDate?: string;
  page?: number;
  limit?: number;
}

export interface ActivityLogSearchResponse {
  logs: ActivityLog[];
  total: number;
  page: number;
  limit: number;
  totalPages: number;
}

export interface GoalType {
  id: string;
  name: string;
  description: string;
  category: 'application' | 'networking' | 'profile' | 'learning';
  metricKey: string;
  defaultTarget: number;
  defaultPeriod: 'daily' | 'weekly' | 'monthly' | 'quarterly';
}

export interface Goal {
  id: string;
  userId: string;
  goalTypeId: string;
  goalType: GoalType;
  target: number;
  current: number;
  period: 'daily' | 'weekly' | 'monthly' | 'quarterly';
  startDate: string;
  endDate: string;
  status: 'active' | 'completed' | 'failed';
  createdAt: string;
  updatedAt: string;
}

export interface GoalCreateRequest {
  goalTypeId: string;
  target: number;
  period: 'daily' | 'weekly' | 'monthly' | 'quarterly';
  startDate: string;
  endDate?: string;
}

export interface GoalUpdateRequest {
  target?: number;
  period?: 'daily' | 'weekly' | 'monthly' | 'quarterly';
  startDate?: string;
  endDate?: string;
  status?: 'active' | 'completed' | 'failed';
}

export interface MarketReport {
  id: string;
  title: string;
  description: string;
  industry: string;
  region: string;
  date: string;
  insights: {
    title: string;
    description: string;
    data?: Record<string, any>;
  }[];
  recommendations: {
    title: string;
    description: string;
  }[];
  createdAt: string;
} 