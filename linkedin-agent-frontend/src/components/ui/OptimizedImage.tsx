'use client';

import React from 'react';
import Image from 'next/image';
import { cn } from '@/lib/utils';

interface OptimizedImageProps {
  src: string;
  alt: string;
  width?: number;
  height?: number;
  priority?: boolean;
  className?: string;
  objectFit?: 'fill' | 'contain' | 'cover' | 'none' | 'scale-down';
  quality?: number;
  isAboveFold?: boolean;
  onLoad?: () => void;
}

/**
 * Optimized image component that uses Next.js Image component with best practices
 * @param props Component props
 * @returns JSX element
 */
const OptimizedImage: React.FC<OptimizedImageProps> = ({
  src,
  alt,
  width = 400,
  height = 300,
  priority = false,
  className,
  objectFit = 'cover',
  quality = 75,
  isAboveFold = false,
  onLoad,
}) => {
  // Apply priority for images above the fold
  const shouldPrioritize = priority || isAboveFold;
  
  // Determine loading strategy
  const loadingStrategy = shouldPrioritize ? 'eager' : 'lazy';
  
  return (
    <div className={cn('overflow-hidden', className)}>
      <Image
        src={src}
        alt={alt}
        width={width}
        height={height}
        priority={shouldPrioritize}
        quality={quality}
        loading={loadingStrategy}
        onLoad={onLoad}
        style={{
          objectFit,
          width: '100%',
          height: '100%',
        }}
      />
    </div>
  );
};

export default OptimizedImage; 