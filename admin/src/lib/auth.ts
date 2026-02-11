import { SignJWT, jwtVerify } from 'jose';
import { cookies } from 'next/headers';
import { NextRequest, NextResponse } from 'next/server';

const secretKey = 'secret'; // TODO: Move to .env
const key = new TextEncoder().encode(secretKey);

export async function encrypt(payload: any) {
  return await new SignJWT(payload)
    .setProtectedHeader({ alg: 'HS256' })
    .setIssuedAt()
    .setExpirationTime('1d') // Session expires in 1 day
    .sign(key);
}

export async function decrypt(input: string): Promise<any> {
  const { payload } = await jwtVerify(input, key, {
    algorithms: ['HS256'],
  });
  return payload;
}

export async function login(userData: any) {
  // Create user session
  const session = await encrypt({ user: userData, expires: new Date(Date.now() + 24 * 60 * 60 * 1000) });

  // Set cookie
  (await cookies()).set('session', session, { expires: new Date(Date.now() + 24 * 60 * 60 * 1000), httpOnly: true, sameSite: 'lax', path: '/' });
}

export async function logout() {
  (await cookies()).set('session', '', { expires: new Date(0), path: '/' });
}

export async function getSession() {
  const session = (await cookies()).get('session')?.value;
  if (!session) return null;
  try {
    return await decrypt(session);
  } catch (error) {
    return null;
  }
}

export async function updateSession(request: NextRequest) {
  const session = request.cookies.get('session')?.value;
  if (!session) return;

  try {
    // Refresh user session if valid
    const parsed = await decrypt(session);
    parsed.expires = new Date(Date.now() + 24 * 60 * 60 * 1000);
    const res = NextResponse.next();
    res.cookies.set({
      name: 'session',
      value: await encrypt(parsed),
      httpOnly: true,
      expires: parsed.expires,
    });
    return res;
  } catch (error) {
    // If session is invalid, just ignore it (middleware will handle redirection if needed)
    return;
  }
}
