"use client";

import { ReactNode, useEffect, useState } from "react";
import Header from "./components/header";
import LoginForm from "./components/loginForm";
import urlCreator from "@/lib/UrlCreator";

interface ClientLayoutProps {
  children: ReactNode;
}

export default function ClientLayout({ children }: ClientLayoutProps) {
  const [isLoginFormVisible, setLoginFormVisible] = useState(false);
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  useEffect(() => {
    const verifyAuthAndFetchUser = async () => {
      const token = localStorage.getItem("token");

      if (!token) {
        localStorage.removeItem("token");
        localStorage.removeItem("username");
        setIsLoggedIn(false);
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
    //window.location.reload();
  };

  const handleLoginClick = () => setLoginFormVisible(true);
  const handleCloseLogin = () => setLoginFormVisible(false);

  return (
    <>
      <Header isLoggedIn={isLoggedIn} onLoginClick={handleLoginClick} handleLogout={handleLogout} />
      <main>{children}</main>
      <>{isLoginFormVisible && <LoginForm onClose={handleCloseLogin} />}</>
    </>
  );
}
