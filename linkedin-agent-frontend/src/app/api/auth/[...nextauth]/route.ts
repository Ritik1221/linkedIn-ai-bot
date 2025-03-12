import NextAuth, { AuthOptions, Session, User } from 'next-auth';
import { JWT } from 'next-auth/jwt';
import LinkedInProvider from 'next-auth/providers/linkedin';
import { apiClient } from '@/lib/api';
import { getEnvVar } from '@/utils/env';

// Extend the built-in session type
declare module 'next-auth' {
  interface Session {
    accessToken?: string;
    refreshToken?: string;
    error?: string;
  }
}

// Extend the built-in JWT type
declare module 'next-auth/jwt' {
  interface JWT {
    accessToken?: string;
    refreshToken?: string;
    expiresAt?: number;
    error?: string;
  }
}

interface LinkedInProfile {
  sub: string;
  name: string;
  email: string;
  picture: string;
}

interface TokenResponse {
  access_token: string;
  refresh_token: string;
  expires_in: number;
}

export const authOptions: AuthOptions = {
  providers: [
    LinkedInProvider({
      clientId: getEnvVar('LINKEDIN_CLIENT_ID'),
      clientSecret: getEnvVar('LINKEDIN_CLIENT_SECRET'),
      authorization: {
        params: {
          scope: 'openid profile email w_member_social r_liteprofile r_emailaddress',
        },
      },
      async profile(profile: LinkedInProfile): Promise<User> {
        return {
          id: profile.sub,
          name: profile.name,
          email: profile.email,
          image: profile.picture,
        };
      },
    }),
  ],
  session: {
    strategy: 'jwt',
    maxAge: 30 * 24 * 60 * 60, // 30 days
  },
  callbacks: {
    async jwt({ token, account, profile }) {
      // Initial sign in
      if (account && profile) {
        try {
          // Exchange LinkedIn token for our backend tokens
          const response = await apiClient.post<TokenResponse>('/auth/linkedin', {
            access_token: account.access_token,
          });

          return {
            ...token,
            accessToken: response.access_token,
            refreshToken: response.refresh_token,
            expiresAt: Date.now() + response.expires_in * 1000,
          };
        } catch (error) {
          console.error('Error exchanging LinkedIn token:', error);
          return token;
        }
      }

      // Return previous token if the access token has not expired yet
      if (token.expiresAt && typeof token.expiresAt === 'number' && Date.now() < token.expiresAt) {
        return token;
      }

      // Access token has expired, try to refresh it
      try {
        const response = await apiClient.post<TokenResponse>('/auth/refresh', {
          refresh_token: token.refreshToken,
        });

        return {
          ...token,
          accessToken: response.access_token,
          refreshToken: response.refresh_token,
          expiresAt: Date.now() + response.expires_in * 1000,
        };
      } catch (error) {
        console.error('Error refreshing token:', error);
        return { ...token, error: 'RefreshAccessTokenError' };
      }
    },
    async session({ session, token }: { session: Session; token: JWT }) {
      session.accessToken = token.accessToken;
      session.refreshToken = token.refreshToken;
      session.error = token.error;

      return session;
    },
  },
  pages: {
    signIn: '/login',
    error: '/login',
  },
  events: {
    async signOut({ token }) {
      try {
        await apiClient.post('/auth/logout', {
          refresh_token: token.refreshToken,
        });
      } catch (error) {
        console.error('Error during logout:', error);
      }
    },
  },
};

const handler = NextAuth(authOptions);
export { handler as GET, handler as POST }; 