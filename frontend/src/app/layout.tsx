import { type ReactNode } from "react";
import { type Metadata } from "next";
import localFont from "next/font/local";
import ClientLayout from "./layout-client";
import "./globals.css";

const geistSans = localFont({
  src: "./fonts/GeistVF.woff",
  variable: "--font-geist-sans",
  weight: "100 900",
  preload: true,
  display: "swap",
});

const geistMono = localFont({
  src: "./fonts/GeistMonoVF.woff",
  variable: "--font-geist-mono",
  weight: "100 900",
  preload: true,
  display: "swap",
});

export const metadata: Metadata = {
  title: "PictoWrite - 英語学習アプリ",
  description: "英語学習Webアプリ「PictoWrite」は、画像生成AIを用いて英作文のスキルを伸ばすものです。",
  viewport: "width=device-width, initial-scale=1",
  robots: "index, follow",
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="ja" className={`${geistSans.variable} ${geistMono.variable}`}>
      <body className="antialiased flex flex-col min-h-screen overflow-hidden bg-gray-50">
        <ClientLayout>{children}</ClientLayout>
      </body>
    </html>
  );
}
