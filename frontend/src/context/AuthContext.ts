import { createContext } from 'react';
import { AuthState } from '@/types/auth';

interface AuthContextType extends AuthState {
  showLoginForm: () => void;
  hideLoginForm: () => void;
  logout: () => void;
}

export const AuthContext = createContext<AuthContextType | null>(null);

export const useAuth = () => {
  const context = AuthContext;
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
};
