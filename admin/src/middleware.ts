import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';
import { updateSession } from '@/lib/auth';

export async function middleware(request: NextRequest) {
  // Update session expiration if valid
  const res = await updateSession(request);
  const isAuthenticated = !!res;

  // Protect dashboard routes
  // Assuming dashboard routes are at the root "/" or specific paths excluding public ones
  // The request says "Make sure teh project is not accessible untill the users log in".
  // And "the login page is located here @[admin/src/app/(auth)/login]".
  
  const isLoginPage = request.nextUrl.pathname.startsWith('/login');
  const isApiAuth = request.nextUrl.pathname.startsWith('/api/auth');
  const isStatic = request.nextUrl.pathname.startsWith('/_next') || request.nextUrl.pathname.startsWith('/images') || request.nextUrl.pathname.startsWith('/favicon.ico');
  
  // If NOT authenticated and trying to access protected route (anything not login, api/auth, or static)
  if (!isAuthenticated && !isLoginPage && !isApiAuth && !isStatic) {
    return NextResponse.redirect(new URL('/login', request.url));
  }
  
  // If authenticated and visiting login page, redirect to dashboard
  if (isAuthenticated && isLoginPage) {
     return NextResponse.redirect(new URL('/', request.url));
  }

  // If we have a new response (refreshed session), return it.
  // Otherwise proceed (for public routes or if valid session but somehow no res? - unlikely with above logic, or if we are on login page but invalid session)
  return res || NextResponse.next();
}

export const config = {
  matcher: ['/((?!_next/static|_next/image|favicon.ico|images).*)'],
};
