"use client";

import React, { use, useState, useEffect } from "react";
import CircularProgressBar from "@/app/components/circleProgressBar";
import urlCreator from "@/lib/UrlCreator";
import { useAuth } from "@/app/layout-client";
import Link from "next/link";

// app/challenge/[content_id]/page.tsx
//urlの[content_id]を取得
type PageProps = {
  params: Promise<{ content_id: string }>;
};

type SubmissionDisplayItems = {
  timestamp?: string;
  content: string;
  score?: number;
};

export default function ContentPage({ params }: PageProps) {
  const { content_id: challengeId } = use(params);
  const [isVisibleNotLoggedInMessage, setIsVisibleNotLoggedInMessage] =
    useState<boolean>(false);
  const [challengeImageUrl, setChallengeImageUrl] = useState<string>("");
  const [generatedImageUrl, setGeneratedImageUrl] = useState<string>("");
  const [currentScore, setCurrentScore] = useState<number>(0);
  const [submissions, setSubmissions] = useState<SubmissionDisplayItems[]>([]);
  const [draftText, setDraftText] = useState<string>("");
  const { isLoggedIn } = useAuth();

  useEffect(() => {
    setTimeout(() => {
      //////////////////setIsVisibleNotLoggedInMessage(true);
    }, 1000);
  });

  useEffect(() => {
    if (!isLoggedIn) {
      return;
    }

    // 問題のデータを取得
    fetch(urlCreator("/api/challenges-list/get/" + challengeId))
      .then((response) => response.json())
      .then((data) => {
        const imgUrl = data.problem.imgUrl;
        setChallengeImageUrl(urlCreator(imgUrl));
      })
      .catch((error) => console.error("Error:", error));

    // プレイ開始を通知
    fetch(urlCreator("/api/challenges-func/start-challenge"), {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${localStorage.getItem("token")}`,
      },
      body: JSON.stringify({ challenge_id: challengeId }),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("Start Challenge:", data);
        if (data.submissions) {
          setSubmissions(data.submissions);
        }
        if (data.last_submission_score) {
          setCurrentScore(data.last_submission_score);
        }
        if (data.last_submission_content) {
          setDraftText(data.last_submission_content);
        }
        if (data.generated_img_url) {
          setGeneratedImageUrl(urlCreator(data.generated_img_url));
        }
      })
      .catch((error) => console.error("Error:", error));
  }, [challengeId, isLoggedIn]);

  fetch(urlCreator("/api/challenges-func/end-challenge"), {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${localStorage.getItem("token")}`,
    },
    body: JSON.stringify({ challenge_id: challengeId }),
  });

  return (
    <div className="flex flex-col h-screen">
      {isLoggedIn === false && isVisibleNotLoggedInMessage === true ? (
        <>
          <div className="bg-red-500 text-white p-4 m-4 rounded shadow-lg">
            プレイにはログインが必要です
          </div>
        </>
      ) : (
        <></>
      )}
      <div className="flex flex-1">
        {/* 上段部 */}
        <div className="flex-1 p-4">
          {/* 左 */}
          <ChallengeImageCard imageUrl={challengeImageUrl} />
        </div>
        <div className="flex-1 p-4">
          {/* 右 */}
          <GeneratedImageCard generatedImageUrl={generatedImageUrl} />
        </div>
      </div>

      <div className="flex flex-1">
        {/* 上段部 */}
        <div className="flex-[7] p-4">
          {/* 左 */}
          <TextAreaCard submissions={submissions} />
        </div>
        <div className="flex-[3] p-4">
          {/* 右 */}
          <ScoreCard currentScore={currentScore} challengeId={challengeId} />
        </div>
      </div>
    </div>
  );
}

const TextAreaCard = ({
  submissions,
}: {
  submissions: SubmissionDisplayItems[];
}) => {
  return (
    <div className="bg-white p-4 h-96 w-full rounded-lg shadow-lg flex flex-col">
      <div className="flex-[9] bg-gray-100 p-2 overflow-y-auto">
        {submissions.map((submission, index) => (
          <div key={index} className="bg-white p-4 my-3 rounded-lg shadow-lg">
            {submission.timestamp ? (
              <p className="py-1 px-2 bg-gray-500 text-white inline rounded">
                {submission.timestamp}
              </p>
            ) : (
              <></>
            )}
            {submission.score ? (
              <p className="py-1 px-2 mx-2 bg-orange-400 text-white font-bold inline rounded">
                スコア: {submission.score}
              </p>
            ) : (
              <></>
            )}
            <p className="pt-2">{submission.content}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

function ChallengeImageCard({ imageUrl }: { imageUrl: string }) {
  return (
    <div
      className="bg-white p-4 h-full w-full rounded-lg shadow-lg bg-cover bg-center"
      style={{ backgroundImage: `url(${imageUrl})` }}
    >
      <p className="bg-white p-2">お題の画像</p>
    </div>
  );
}

function GeneratedImageCard({
  generatedImageUrl,
}: {
  generatedImageUrl: string;
}) {
  return (
    <div
      className="bg-white p-4 h-full w-full rounded-lg shadow-lg bg-cover bg-center"
      style={{ backgroundImage: `url(${generatedImageUrl})` }}
    >
      <p className="bg-white p-2">AIが作った画像</p>
    </div>
  );
}

function ScoreCard({
  currentScore,
  challengeId,
}: {
  currentScore: number;
  challengeId: string;
}) {
  return (
    <div className="bg-white p-4 w-full min-w-96 rounded-lg shadow-lg">
      <p className="pt-2 text-center font-bold text-xl">
        最終的なスコアは {currentScore} でした！
      </p>
      <div className="flex justify-center my-2">
        <CircularProgressBar
          maxValue={100}
          currentValue={currentScore}
          size={260}
        />
      </div>
      <div className="">
        <Link
          href="/"
          className="bg-blue-500 text-white block rounded-xl p-2 text-center"
        >
          トップページに戻る
        </Link>
      </div>
    </div>
  );
}
