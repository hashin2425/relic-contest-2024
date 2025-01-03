"use client";
import { useState } from "react";
import localFont from "next/font/local";
import "./globals.css";

import Header from "./components/header";
import LoginForm from "./components/loginForm";

const geistSans = localFont({
  src: "./fonts/GeistVF.woff",
  variable: "--font-geist-sans",
  weight: "100 900",
});
const geistMono = localFont({
  src: "./fonts/GeistMonoVF.woff",
  variable: "--font-geist-mono",
  weight: "100 900",
});

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  const [isLoginFormVisible, setLoginFormVisible] = useState(false);

  return (
    <html lang="ja">
      <title>relic-2024</title>
      <meta name="description" content="Generated by create next app with Tailwind CSS"/>
      
      <body className={`${geistSans.variable} ${geistMono.variable} antialiased
      flex flex-col min-h-screen overflow-hidden bg-gray-50`}>
        <Header onLoginClick={() => setLoginFormVisible(true)} />
        {children}
        {isLoginFormVisible && <LoginForm onClose={() => setLoginFormVisible(false)} />}
      </body>
    </html>
  );
}
