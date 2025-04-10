import { type ReactNode } from "react";
import { type Metadata } from "next";
import localFont from "next/font/local";
import Script from "next/script";
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

function googleAnalytics() {
  return (
    <>
      <Script src="https://www.googletagmanager.com/gtag/js?id=G-HL8Q7ZL2TV" strategy="afterInteractive" />
      <Script id="google-analytics" strategy="afterInteractive">
        {`
          window.dataLayer = window.dataLayer || [];
          function gtag(){dataLayer.push(arguments);}
          gtag('js', new Date());
          gtag('config', 'G-HL8Q7ZL2TV');
        `}
      </Script>
    </>
  );
}

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="ja" className={`${geistSans.variable} ${geistMono.variable} antialiased h-full w-full bg-gray-200`}>
      <body className="h-full w-full">
        <ClientLayout>{children}</ClientLayout>
        {googleAnalytics()}
      </body>
    </html>
  );
}
