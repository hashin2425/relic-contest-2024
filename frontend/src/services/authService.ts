import urlCreator from "@/lib/UrlCreator";
import { LoginCredentials, LoginResponse, User, AuthState } from "@/types/auth";

const TOKEN_KEY = 'token';
const USER_KEY = 'username';

class AuthService {
  private static instance: AuthService;

  private constructor() {}

  static getInstance(): AuthService {
    if (!AuthService.instance) {
      AuthService.instance = new AuthService();
    }
    return AuthService.instance;
  }

  async login(credentials: LoginCredentials): Promise<void> {
    const response = await fetch(urlCreator("/api/auth/login"), {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(credentials),
    });

    if (!response.ok) {
      throw new Error("Login failed");
    }

    const data = await response.json() as LoginResponse;
    this.setToken(data.access_token);
    this.setUser(credentials.id);
  }

  async verifyAuth(): Promise<AuthState> {
    const token = this.getToken();
    
    if (!token) {
      return this.getInitialState();
    }

    try {
      const response = await fetch(urlCreator("/api/auth/is-logged-in"), {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (!response.ok) {
        throw new Error("Auth verification failed");
      }

      const data = await response.json() as User;
      return {
        isLoggedIn: true,
        user: { id: data.id },
        token
      };
    } catch (error) {
      this.logout();
      return this.getInitialState();
    }
  }

  logout(): void {
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(USER_KEY);
  }

  private setToken(token: string): void {
    localStorage.setItem(TOKEN_KEY, token);
  }

  private setUser(userId: string): void {
    localStorage.setItem(USER_KEY, userId);
  }

  private getToken(): string | null {
    return localStorage.getItem(TOKEN_KEY);
  }

  private getInitialState(): AuthState {
    return {
      isLoggedIn: false,
      user: null,
      token: null
    };
  }
}

export const authService = AuthService.getInstance();
