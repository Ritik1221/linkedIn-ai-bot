'use client';

import dynamic from 'next/dynamic';
import React from 'react';
import type { JobMatchData } from './JobMatchVisualizer';

// Import skeleton loader
import JobMatchSkeletonLoader from './JobMatchSkeletonLoader';

// Dynamically import the JobMatchVisualizer with SSR disabled
const DynamicJobMatchVisualizer = dynamic(
  () => import('./JobMatchVisualizer').then((mod) => mod.default),
  {
    loading: () => <JobMatchSkeletonLoader />,
    ssr: false, // Disable SSR for this component as it uses browser-specific APIs
  }
);

interface DynamicJobMatchVisualizerProps {
  matchData: JobMatchData;
  isLoading?: boolean;
}

const JobMatchVisualizerWrapper: React.FC<DynamicJobMatchVisualizerProps> = (props) => {
  return <DynamicJobMatchVisualizer {...props} />;
};

export default JobMatchVisualizerWrapper; 