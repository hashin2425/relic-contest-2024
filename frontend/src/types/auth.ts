export interface LoginCredentials {
  id: string;
  password: string;
}

export interface LoginResponse {
  access_token: string;
}

export interface User {
  id: string;
}

export interface AuthState {
  isLoggedIn: boolean;
  user: User | null;
  token: string | null;
}
