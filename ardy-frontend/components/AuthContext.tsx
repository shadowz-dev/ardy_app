import { useContext, createContext, type PropsWithChildren } from 'react';
import { useStorageState } from './useStorageState';

const AuthContext = createContext<{
  signIn: (type: string) => void;
  signOut: () => void;
  session?: string | null;
  userType?: string | null;
  isLoading: boolean;
} | null>(null);

export function useSession() {
  const value = useContext(AuthContext);
  if (!value) {
    throw new Error('useSession must be wrapped in a <SessionProvider />');
  }
  return value;
}

export function SessionProvider({ children }: PropsWithChildren) {
  const [session, setSession] = useStorageState<string | null>('session', null);
  const [userType, setUserType] = useStorageState<string | null>('userType', null);

  const isLoading = session === undefined || userType === undefined;

  return (
    <AuthContext.Provider
      value={{
        signIn: (type: string) => {
          setSession('xxx'); // Replace with actual session logic
          setUserType(type);
        },
        signOut: () => {
          setSession(null);
          setUserType(null);
        },
        session,
        userType,
        isLoading,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}
