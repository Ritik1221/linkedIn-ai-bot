'use client';

import React from 'react';

const JobMatchSkeletonLoader: React.FC = () => {
  return (
    <div className="flex flex-col space-y-8 p-6 bg-card rounded-lg border shadow-sm w-full animate-pulse">
      <div className="text-center">
        <div className="h-8 w-48 bg-gray-200 mx-auto rounded mb-2"></div>
        <div className="h-4 w-36 bg-gray-200 mx-auto rounded"></div>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        <div className="flex flex-col items-center">
          <div className="h-5 w-32 bg-gray-200 rounded mb-4"></div>
          <div className="h-64 w-full max-w-xs rounded-full bg-gray-200"></div>
        </div>
        
        <div className="flex flex-col items-center">
          <div className="h-5 w-40 bg-gray-200 rounded mb-4"></div>
          <div className="h-64 w-full max-w-xs rounded-full bg-gray-200"></div>
        </div>
      </div>
      
      <div className="mt-6">
        <div className="h-5 w-36 bg-gray-200 rounded mb-4"></div>
        <div className="space-y-3">
          {Array.from({ length: 5 }).map((_, i) => (
            <div key={i} className="space-y-1">
              <div className="flex justify-between">
                <div className="h-4 w-32 bg-gray-200 rounded"></div>
                <div className="h-4 w-12 bg-gray-200 rounded"></div>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2"></div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default JobMatchSkeletonLoader; 