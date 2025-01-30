import { useState, useEffect, useCallback } from 'react';
import { authService } from '@/services/authService';
import { AuthState, LoginCredentials } from '@/types/auth';

interface UseAuthState extends AuthState {
  login: (credentials: LoginCredentials) => Promise<void>;
  logout: () => void;
  showLoginForm: () => void;
  hideLoginForm: () => void;
  isLoginFormVisible: boolean;
}

export function useAuthState(): UseAuthState {
  const [authState, setAuthState] = useState<AuthState>({
    isLoggedIn: false,
    user: null,
    token: null,
  });
  const [isLoginFormVisible, setLoginFormVisible] = useState(false);

  useEffect(() => {
    verifyAuth();
  }, []);

  const verifyAuth = async () => {
    const state = await authService.verifyAuth();
    setAuthState(state);
  };

  const login = async (credentials: LoginCredentials) => {
    try {
      await authService.login(credentials);
      await verifyAuth();
      setLoginFormVisible(false);
    } catch (error) {
      throw error;
    }
  };

  const logout = useCallback(() => {
    authService.logout();
    setAuthState({
      isLoggedIn: false,
      user: null,
      token: null,
    });
    window.location.reload();
  }, []);

  const showLoginForm = useCallback(() => setLoginFormVisible(true), []);
  const hideLoginForm = useCallback(() => setLoginFormVisible(false), []);

  return {
    ...authState,
    login,
    logout,
    showLoginForm,
    hideLoginForm,
    isLoginFormVisible,
  };
}
