"use client";

import { ReactNode, createContext, useContext, useEffect, useState } from "react";
import Header from "./components/header";
import LoginForm from "./components/loginForm";
import urlCreator from "@/lib/UrlCreator";

interface AuthContextType {
  isLoggedIn: boolean;
  username: string | null;
  showLoginForm: () => void;
  hideLoginForm: () => void;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | null>(null);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
};

interface ClientLayoutProps {
  children: ReactNode;
}

export default function ClientLayout({ children }: ClientLayoutProps) {
  const [isLoginFormVisible, setLoginFormVisible] = useState(false);
  const [isLoggedIn, setIsLoggedIn] = useState<boolean | null>(null);
  const [username, setUsername] = useState<string | null>(null);

  useEffect(() => {
    const verifyAuthAndFetchUser = async () => {
      const token = localStorage.getItem("token");

      if (!token) {
        localStorage.removeItem("token");
        localStorage.removeItem("username");
        setIsLoggedIn(false);
        setUsername(null);
        return;
      }

      try {
        const response = await fetch(urlCreator("/api/auth/me"), {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        const data = await response.json();

        if (response.ok) {
          // APIレスポンスが正常な場合、ユーザー情報を更新
          setIsLoggedIn(true);
          setUsername(data.id);
          localStorage.setItem("username", data.id);
        } else {
          // APIレスポンスがエラーの場合、ログアウト
          handleLogout();
        }
      } catch (error) {
        console.error("Failed to fetch user data:", error);
        handleLogout();
      }
    };

    verifyAuthAndFetchUser();
  }, []);

  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("username");
    setIsLoggedIn(false);
    setUsername(null);
    window.location.reload();
  };

  const handleLoginClick = () => setLoginFormVisible(true);
  const handleCloseLogin = () => setLoginFormVisible(false);

  const authContextValue: AuthContextType = {
    isLoggedIn,
    username,
    showLoginForm: handleLoginClick,
    hideLoginForm: handleCloseLogin,
    logout: handleLogout,
  };

  return (
    <AuthContext.Provider value={authContextValue}>
      <Header isLoggedIn={isLoggedIn} onLoginClick={handleLoginClick} handleLogout={handleLogout} />
      <main>{children}</main>
      {isLoginFormVisible && <LoginForm onClose={handleCloseLogin} />}
    </AuthContext.Provider>
  );
}
