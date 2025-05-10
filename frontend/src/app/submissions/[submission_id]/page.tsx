"use client";

import React, { use, useState, useEffect } from "react";
import Image from "next/image";
import urlCreator from "@/lib/UrlCreator";
import { useAuth } from "@/app/layout-client";

// app/submissions/[submission_id]/page.tsx
//urlの[submission_id]を取得
type PageProps = {
  params: Promise<{ submission_id: string }>;
};

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

export default function ContentPage({ params }: PageProps) {
  const { submission_id } = use(params);
  const [submissionData, setSubmissionData] = useState<SubmissionDisplayItems | null>(null);

  useEffect(() => {
    fetch(urlCreator("/api/challenges-func/get-submission/" + submission_id), {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${localStorage.getItem("token")}`,
      },
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("Submission Data:", data);
        data?.images.map((imgUrl, index) => {
          console.log("Image URL:", urlCreator(imgUrl));
        });
        setSubmissionData(data);
      })
      .catch((error) => console.error("Error:", error));
  }, [submission_id]);

  return (
    <div className="mx-4">
      <div>提出ID：{submission_id}</div>
      <div>チャレンジID：{submissionData?.challenge_id}</div>
      <div>作成日時：{submissionData?.created_at}</div>

      <div className="flex mt-4">

        <div className="w-1/2 pr-2">
          {submissionData?.images?.map((imgUrl, index) => (
            <div className="mb-4" key={index}>
              <div className="bg-white p-4 h-full w-full rounded-lg shadow-lg flex flex-col min-h-96">
                <p>{index + 1}枚目</p>
                <div className="flex-1 relative">
                  <div className="absolute inset-0 bg-center bg-no-repeat bg-contain" style={{ backgroundImage: `url(${urlCreator(imgUrl)})` }}></div>
                </div>
              </div>
            </div>
          ))}
        </div>

        <div className="w-1/2 pl-2">
          <div className="overflow-y-auto">
            {submissionData?.submissions?.map((submission, index) => (
              <div key={index} className="bg-white p-4 mb-4 rounded-lg shadow-lg">
                {submission.timestamp ? <p className="py-1 px-2 bg-gray-500 text-white inline rounded">{submission.timestamp}</p> : <></>}
                {submission.score ? <p className="py-1 px-2 mx-2 bg-orange-400 text-white font-bold inline rounded">スコア: {submission.score}</p> : <></>}
                <p className="pt-2">{submission.content}</p>
              </div>
            ))}
          </div>
        </div>

      </div>
    </div>
  )
}