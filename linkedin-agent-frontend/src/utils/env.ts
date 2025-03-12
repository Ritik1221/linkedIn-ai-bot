interface EnvVar {
  key: string;
  required: boolean;
  type: 'string' | 'number' | 'boolean' | 'url';
}

const requiredEnvVars: EnvVar[] = [
  { key: 'NEXT_PUBLIC_API_URL', required: true, type: 'url' },
  { key: 'NEXTAUTH_URL', required: true, type: 'url' },
  { key: 'NEXTAUTH_SECRET', required: true, type: 'string' },
  { key: 'LINKEDIN_CLIENT_ID', required: true, type: 'string' },
  { key: 'LINKEDIN_CLIENT_SECRET', required: true, type: 'string' },
];

class EnvironmentError extends Error {
  constructor(message: string) {
    super(message);
    this.name = 'EnvironmentError';
  }
}

function validateUrl(value: string, key: string): void {
  try {
    new URL(value);
  } catch (error) {
    throw new EnvironmentError(`Invalid URL for environment variable ${key}: ${value}`);
  }
}

export function validateEnv(): void {
  for (const envVar of requiredEnvVars) {
    const value = process.env[envVar.key];

    if (envVar.required && !value) {
      throw new EnvironmentError(`Missing required environment variable: ${envVar.key}`);
    }

    if (value) {
      switch (envVar.type) {
        case 'number':
          if (isNaN(Number(value))) {
            throw new EnvironmentError(
              `Environment variable ${envVar.key} must be a number`
            );
          }
          break;
        case 'boolean':
          if (value !== 'true' && value !== 'false') {
            throw new EnvironmentError(
              `Environment variable ${envVar.key} must be a boolean`
            );
          }
          break;
        case 'url':
          validateUrl(value, envVar.key);
          break;
      }
    }
  }
}

export function getEnvVar(key: string): string {
  const value = process.env[key];
  if (!value) {
    throw new EnvironmentError(`Environment variable ${key} is not defined`);
  }
  return value;
}

// Validate environment variables during development
if (process.env.NODE_ENV === 'development') {
  validateEnv();
} 