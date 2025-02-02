"use client";

import { ReactNode } from "react";
import Header from "./components/header";
import LoginForm from "./components/loginForm";
import { useAuthState } from "@/hooks/useAuthState";

interface ClientLayoutProps {
  children: ReactNode;
}

export default function ClientLayout({ children }: ClientLayoutProps) {
  const { isLoggedIn, user, isLoginFormVisible, showLoginForm, hideLoginForm, logout } = useAuthState();

  return (
    <>
      <Header 
        isLoggedIn={isLoggedIn} 
        username={user?.id || null} 
        onLoginClick={showLoginForm} 
        handleLogout={logout} 
      />
      <main>{children}</main>
      {isLoginFormVisible && <LoginForm onClose={hideLoginForm} />}
    </>
  );
}
