import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';
import { getToken } from 'next-auth/jwt';

// Paths that require authentication
const protectedPaths = [
  '/dashboard',
  '/profile',
  '/jobs',
  '/applications',
  '/networking',
];

// Paths that are accessible only to non-authenticated users
const authPaths = [
  '/auth/login',
  '/auth/register',
  '/auth/forgot-password',
  '/auth/reset-password',
];

/**
 * Middleware function to handle authentication and authorization
 * @param request Next.js request object
 * @returns Next.js response object
 */
export async function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;
  
  // Check if the path is protected
  const isProtectedPath = protectedPaths.some(path => 
    pathname === path || pathname.startsWith(`${path}/`)
  );
  
  // Check if the path is for authentication
  const isAuthPath = authPaths.some(path => 
    pathname === path || pathname.startsWith(`${path}/`)
  );
  
  // Get the authentication token
  const token = await getToken({
    req: request,
    secret: process.env.NEXTAUTH_SECRET,
  });
  
  // If the path is protected and the user is not authenticated, redirect to login
  if (isProtectedPath && !token) {
    const url = new URL('/auth/login', request.url);
    url.searchParams.set('callbackUrl', encodeURI(pathname));
    return NextResponse.redirect(url);
  }
  
  // If the path is for authentication and the user is already authenticated, redirect to dashboard
  if (isAuthPath && token) {
    return NextResponse.redirect(new URL('/dashboard', request.url));
  }
  
  // Allow the request to proceed
  return NextResponse.next();
}

// Configure the middleware to run on specific paths
export const config = {
  matcher: [
    /*
     * Match all paths except for:
     * 1. /api routes
     * 2. /_next (Next.js internals)
     * 3. /_static (static files)
     * 4. /favicon.ico, /robots.txt, /sitemap.xml (SEO files)
     */
    '/((?!api|_next|_static|favicon.ico|robots.txt|sitemap.xml).*)',
  ],
}; 