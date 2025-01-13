"use client";

import urlCreator from "@/lib/UrlCreator";
import React, { useEffect, useState } from "react";

export default function UserPage() {
  const [username, setUsername] = useState("");

  useEffect(() => {
    const fetchUserData = async () => {
      try {
        const response = await fetch(urlCreator("/api/auth/me"), {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        });
        const data = await response.json();
        if (response.ok) {
          setUsername(data.id);
        }
      } catch (error) {
        console.error("Failed to fetch user data:", error);
      }
    };

    fetchUserData();
  }, []);

  return (
    <main className="flex justify-center p-4">
      <div className="p-4 bg-white w-1/2 min-w-96 border rounded">
        <h1 className="text-3xl font-bold">ユーザー情報</h1>

        <h2 className="text-2xl font-bold py-4">基本情報</h2>
        <table className="w-full">
          <tbody>
            <tr>
              <th className="py-1 px-2 bg-gray-100 text-left w-40">ユーザー名</th>
              <td className="py-1 px-2">{username === "" ? "（未ログインです）" : username}</td>
            </tr>
            <tr className="border-t">
              <th className="py-1 px-2 bg-gray-100 text-left w-40">メールアドレス</th>
              <td className="py-1 px-2">（未対応です）</td>
            </tr>
            <tr className="border-t">
              <th className="py-1 px-2 bg-gray-100 text-left w-40">パスワード</th>
              <td className="py-1 px-2">（未対応です）</td>
            </tr>
          </tbody>
        </table>

        <h2 className="text-2xl font-bold py-4">プレイ記録</h2>
        <p>（未対応です）</p>

        <h2 className="text-2xl font-bold py-4">英語力測定</h2>
        <p>（未対応です）</p>
      </div>
    </main>
  );
}
