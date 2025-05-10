"use client";

import urlCreator from "@/lib/UrlCreator";
import React, { useEffect, useState } from "react";
import Link from "next/link";

type SubmissionDisplayItems = {
  submission_id: string;
  challenge_id: string;
  created_at: string;
  images: string[];
  submissions: Submission[];
};

type Submission = {
  timestamp: string;
  score: number;
  content: string;
};
export default function UserPage() {
  const [username, setUsername] = useState("");
  const [submissionDataList, setSubmissionDataList] = useState<SubmissionDisplayItems[]>([]);

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

  useEffect(() => {
    fetch(urlCreator("/api/challenges-func/get-all-submission"), {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${localStorage.getItem("token")}`,
      },
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("Submission Data:", data.submissions);
        if (data.submissions) { setSubmissionDataList(data.submissions); }
      })
      .catch((error) => console.error("Error:", error));
  }
    , []);

  const h2style = "text-2xl font-bold my-4 mt-8 pl-2 border-l-8 border-orange-400";

  return (
    <main className="flex justify-center p-4">
      <div className="p-4 bg-white w-1/2 min-w-96 border rounded">
        <h1 className="text-3xl font-bold">ユーザー情報</h1>

        <h2 className={h2style}>基本情報</h2>
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

        <h2 className={h2style}>プレイ記録</h2>
        {submissionDataList.length === 0 ?
          <p>
            記録がありません
          </p>
          :
          <table className="w-full">
            <thead>
              <tr>
                <th className="py-1 px-2 bg-gray-100 text-left w-40">提出日時</th>
                <th className="py-1 px-2 bg-gray-100 text-left">チャレンジID</th>
                <th className="py-1 px-2 bg-gray-100 text-left">振り返る</th>
              </tr>
            </thead>
            <tbody>
              {submissionDataList.map((submission) => (
                <tr key={submission.submission_id} className="border-t">
                  {new Date(submission.created_at).toLocaleString('ja-JP', {
                    timeZone: 'Asia/Tokyo'
                  })}
                  <td className="py-1 px-2">{submission.challenge_id}</td>
                  <td className="py-1 px-2">
                    <Link className="text-blue-500 underline" href={`/submissions/${submission.submission_id}`}>振り返る</Link>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        }
        <h2 className={h2style}>英語力測定</h2>
        <p>（未対応です）</p>
      </div>
    </main>
  );
}
