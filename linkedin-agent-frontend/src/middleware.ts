import { withAuth } from 'next-auth/middleware';
import { NextResponse } from 'next/server';

export default withAuth(
  function middleware(req) {
    // Add custom headers or modify the request/response here
    return NextResponse.next();
  },
  {
    callbacks: {
      authorized: ({ token }) => {
        // Return true if the token exists and doesn't have an error
        return !!token && !token.error;
      },
    },
    pages: {
      signIn: '/login',
    },
  }
);

export const config = {
  // Protect all routes under /dashboard, /jobs, /networking, /applications, and /profile
  matcher: [
    '/dashboard/:path*',
    '/jobs/:path*',
    '/networking/:path*',
    '/applications/:path*',
    '/profile/:path*',
  ],
}; 