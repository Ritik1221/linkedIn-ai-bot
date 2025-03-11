'use client';

import { useReportWebVitals } from 'next/web-vitals';
import { useCallback } from 'react';

/**
 * Interface for analytics service
 */
interface AnalyticsService {
  trackEvent: (eventName: string, eventData: Record<string, any>) => void;
}

/**
 * Default analytics service implementation that logs to console in development
 */
const defaultAnalyticsService: AnalyticsService = {
  trackEvent: (eventName, eventData) => {
    if (process.env.NODE_ENV === 'development') {
      console.log(`[Analytics] ${eventName}:`, eventData);
    }
  },
};

interface WebVitalsReporterProps {
  /**
   * Optional analytics service implementation
   * If not provided, will use the default service which logs to console in development
   */
  analyticsService?: AnalyticsService;
}

/**
 * Component that reports Web Vitals metrics to analytics
 * Place this component in your app layout to track web vitals for all pages
 */
export default function WebVitalsReporter({ 
  analyticsService = defaultAnalyticsService 
}: WebVitalsReporterProps) {
  const reportWebVital = useCallback(
    (metric: any) => {
      // Destructure the metric object
      const { id, name, label, value } = metric;
      
      // Create a readable name for the metric
      const metricName = `web-vital-${name}`;
      
      // Log the metric to analytics
      analyticsService.trackEvent(metricName, {
        id,
        name,
        label,
        value: Math.round(name === 'CLS' ? value * 1000 : value), // Convert CLS to milliseconds for consistency
        page: window.location.pathname,
        timestamp: new Date().toISOString(),
      });
    },
    [analyticsService]
  );

  // Register the web vitals reporter
  useReportWebVitals(reportWebVital);

  // This component doesn't render anything
  return null;
} 