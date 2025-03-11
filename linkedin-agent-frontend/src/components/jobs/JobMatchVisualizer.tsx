'use client';

import React, { useEffect, useState } from 'react';
import { Chart as ChartJS, ArcElement, Tooltip, Legend, RadialLinearScale } from 'chart.js';
import { Doughnut, PolarArea } from 'react-chartjs-2';

// Register ChartJS components
ChartJS.register(ArcElement, RadialLinearScale, Tooltip, Legend);

export interface SkillMatch {
  skill: string;
  matchPercentage: number;
}

export interface JobMatchData {
  overallMatch: number;
  skillMatches: SkillMatch[];
  experienceMatch: number;
  educationMatch: number;
  locationMatch: number;
}

interface JobMatchVisualizerProps {
  matchData: JobMatchData;
  isLoading?: boolean;
}

const JobMatchVisualizer: React.FC<JobMatchVisualizerProps> = ({ 
  matchData, 
  isLoading = false 
}) => {
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  // Don't render on server
  if (!mounted) {
    return null;
  }

  if (isLoading) {
    return (
      <div className="flex flex-col space-y-4 p-4 bg-card rounded-lg border shadow-sm w-full">
        <div className="h-64 w-full flex items-center justify-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
        </div>
      </div>
    );
  }

  // Overall match doughnut chart data
  const overallMatchData = {
    labels: ['Match', 'Gap'],
    datasets: [
      {
        data: [matchData.overallMatch, 100 - matchData.overallMatch],
        backgroundColor: [
          'rgba(54, 162, 235, 0.8)',
          'rgba(234, 236, 239, 0.8)',
        ],
        borderColor: [
          'rgba(54, 162, 235, 1)',
          'rgba(234, 236, 239, 1)',
        ],
        borderWidth: 1,
      },
    ],
  };

  // Category match data
  const categoryMatchData = {
    labels: ['Skills', 'Experience', 'Education', 'Location'],
    datasets: [
      {
        data: [
          matchData.skillMatches.reduce((acc, skill) => acc + skill.matchPercentage, 0) / matchData.skillMatches.length,
          matchData.experienceMatch,
          matchData.educationMatch,
          matchData.locationMatch,
        ],
        backgroundColor: [
          'rgba(54, 162, 235, 0.5)',
          'rgba(75, 192, 192, 0.5)',
          'rgba(153, 102, 255, 0.5)',
          'rgba(255, 159, 64, 0.5)',
        ],
        borderWidth: 1,
      },
    ],
  };

  return (
    <div className="flex flex-col space-y-8 p-6 bg-card rounded-lg border shadow-sm w-full">
      <div className="text-center">
        <h2 className="text-2xl font-bold mb-2">Job Match Analysis</h2>
        <p className="text-muted-foreground">
          Overall match: <span className="font-bold">{matchData.overallMatch}%</span>
        </p>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        <div className="flex flex-col items-center">
          <h3 className="text-lg font-semibold mb-4">Overall Match</h3>
          <div className="h-64 w-full max-w-xs">
            <Doughnut 
              data={overallMatchData} 
              options={{
                cutout: '70%',
                plugins: {
                  legend: {
                    position: 'bottom',
                  },
                },
              }}
            />
          </div>
        </div>
        
        <div className="flex flex-col items-center">
          <h3 className="text-lg font-semibold mb-4">Category Breakdown</h3>
          <div className="h-64 w-full max-w-xs">
            <PolarArea 
              data={categoryMatchData} 
              options={{
                plugins: {
                  legend: {
                    position: 'bottom',
                  },
                },
              }}
            />
          </div>
        </div>
      </div>
      
      <div className="mt-6">
        <h3 className="text-lg font-semibold mb-4">Skill Match Details</h3>
        <div className="space-y-3">
          {matchData.skillMatches.map((skill) => (
            <div key={skill.skill} className="space-y-1">
              <div className="flex justify-between text-sm">
                <span>{skill.skill}</span>
                <span className="font-medium">{skill.matchPercentage}%</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div 
                  className="bg-blue-600 h-2 rounded-full" 
                  style={{ width: `${skill.matchPercentage}%` }}
                ></div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default JobMatchVisualizer; 