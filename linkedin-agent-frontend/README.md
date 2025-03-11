# LinkedIn AI Agent Frontend

A modern, responsive web application for the LinkedIn AI Agent platform.

## Overview

The LinkedIn AI Agent frontend provides an intuitive user interface for managing LinkedIn profiles, job searches, applications, and networking. It connects to the LinkedIn AI Agent backend API and presents AI-powered insights and recommendations to users.

## Features

- **User Authentication**: Secure login with email/password and LinkedIn OAuth
- **Profile Management**: View and edit LinkedIn profile information
- **Job Search**: Search, filter, and save job opportunities
- **Application Tracking**: Manage job applications and track their status
- **AI-Powered Assistance**: 
  - Profile optimization suggestions
  - Job matching visualization
  - Cover letter generation
  - Resume tailoring
- **Networking**: Manage connections and messages
- **Analytics**: Track job search and application metrics

## Tech Stack

- **Framework**: Next.js 14
- **Language**: TypeScript
- **State Management**: Redux Toolkit, React Query
- **Authentication**: NextAuth.js
- **Styling**: Tailwind CSS, Radix UI
- **Animation**: Framer Motion
- **Charts**: Recharts
- **Form Handling**: React Hook Form, Zod
- **Testing**: Jest, React Testing Library
- **Analytics**: PostHog
- **Containerization**: Docker

## Project Structure

```
linkedin-agent-frontend/
├── public/              # Static assets
├── src/
│   ├── app/             # Next.js app router pages
│   ├── components/      # Reusable UI components
│   ├── hooks/           # Custom React hooks
│   ├── lib/             # Utility functions
│   ├── services/        # API service functions
│   ├── store/           # Redux store configuration
│   ├── styles/          # Global styles
│   └── types/           # TypeScript type definitions
├── .env                 # Environment variables
├── .env.example         # Example environment variables
├── Dockerfile.dev       # Development Dockerfile
├── next.config.js       # Next.js configuration
├── package.json         # Dependencies and scripts
├── tailwind.config.js   # Tailwind CSS configuration
├── tsconfig.json        # TypeScript configuration
└── README.md            # Project documentation
```

## Setup

### Prerequisites

- Node.js 18+
- npm or yarn

### Local Development

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/linkedin-agent.git
   cd linkedin-agent/linkedin-agent-frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   # or
   yarn install
   ```

3. Create a `.env` file based on `.env.example` and fill in your configuration.

4. Start the development server:
   ```bash
   npm run dev
   # or
   yarn dev
   ```

5. Open [http://localhost:3000](http://localhost:3000) in your browser.

### Docker Development

1. Build and start the container:
   ```bash
   docker-compose -f docker-compose.dev.yml up -d
   ```

2. Open [http://localhost:3000](http://localhost:3000) in your browser.

## Building for Production

```bash
npm run build
# or
yarn build
```

## Testing

Run the test suite:

```bash
npm test
# or
yarn test
```

## Linting

```bash
npm run lint
# or
yarn lint
```

## Formatting

```bash
npm run format
# or
yarn format
```

## License

[MIT License](LICENSE) 