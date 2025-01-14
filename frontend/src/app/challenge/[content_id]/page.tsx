"use client";

import React, { use, useState, useEffect } from "react";
import CircularProgressBar from "@/app/components/circleProgressBar";
import urlCreator from "@/lib/UrlCreator";
import { useAuth } from "@/app/layout-client";

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
  const { content_id: id } = use(params);
  const [isVisibleNotLoggedInMessage, setIsVisibleNotLoggedInMessage] = useState<boolean>(false);
  const [challengeImageUrl, setChallengeImageUrl] = useState<string>("");
  const [generatedImageUrl, setGeneratedImageUrl] = useState<string>("");
  const [currentScore, setCurrentScore] = useState<number>(0);
  const [submissions, setSubmissions] = useState<SubmissionDisplayItems[]>([]);
  const [draftText, setDraftText] = useState<string>("");
  const { isLoggedIn } = useAuth();

  useEffect(() => {
    setTimeout(() => {
      setIsVisibleNotLoggedInMessage(true);
    }, 1000);
  });

  useEffect(() => {
    if (!isLoggedIn) {
      return;
    }

    // 問題のデータを取得
    fetch(urlCreator("/api/challenges-list/get/" + id))
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
      body: JSON.stringify({ challenge_id: id }),
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
          setGeneratedImageUrl(data.generated_img_url);
        }
      })
      .catch((error) => console.error("Error:", error));
  }, [id, isLoggedIn]);

  function handleSubmit() {
    fetch(urlCreator("/api/challenges-func/submit"), {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${localStorage.getItem("token")}`,
      },
      body: JSON.stringify({ submission: draftText }),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("Submit Response:", data);
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
          setGeneratedImageUrl(data.generated_img_url);
        }
      })
      .catch((error) => console.error("Error:", error));
  }

  return (
    <div className="flex flex-col h-screen">
      {isLoggedIn === false && isVisibleNotLoggedInMessage === true ? (
        <>
          <div className="bg-red-500 text-white p-4 m-4 rounded shadow-lg">プレイにはログインが必要です</div>
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
          <TextAreaCard submissions={submissions} draftText={draftText} setDraftText={setDraftText} handleSubmit={handleSubmit} />
        </div>
        <div className="flex-[3] p-4">
          {/* 右 */}
          <ScoreCard currentScore={currentScore} />
        </div>
      </div>
    </div>
  );
}

const TextAreaCard = ({ submissions, draftText, setDraftText, handleSubmit }: { submissions: SubmissionDisplayItems[]; draftText: string; setDraftText: React.Dispatch<React.SetStateAction<string>>; handleSubmit: () => void }) => {
  const [errorMessage, setErrorMessage] = useState<string>("");
  const [lastSubmissionTime, setLastSubmissionTime] = useState<number>(0);
  const [coolDownRemaining, setCoolDownRemaining] = useState<number>(0);
  const COOL_DOWN_DURATION = 120; // seconds

  useEffect(() => {
    const timer = setInterval(() => {
      const now = Date.now();
      const timeElapsed = Math.floor((now - lastSubmissionTime) / 1000);
      const remaining = Math.max(0, COOL_DOWN_DURATION - timeElapsed);
      setCoolDownRemaining(remaining);
    }, 1000);

    return () => clearInterval(timer);
  }, [lastSubmissionTime]);

  const validateSubmission = (text: string): boolean => {
    // Check if in cooldown
    if (coolDownRemaining > 0) {
      setErrorMessage(`次の提出まで${coolDownRemaining}秒お待ちください！`);
      return false;
    }

    if (text === "" || text === null || text === undefined) {
      setErrorMessage("テキストを入力してください！");
      return false;
    }

    // Check length
    if (text.length > 1000) {
      setErrorMessage("テキストが長すぎます！（1000文字以内）");
      return false;
    }

    // Check for invalid characters
    const validCharPattern = /^[a-zA-Z0-9., 　]+$/;
    if (!validCharPattern.test(text)) {
      setErrorMessage("使用できない文字が含まれています！（英数字、ピリオド、カンマのみ使用可能）");
      return false;
    }

    setErrorMessage("");
    return true;
  };

  function handleSubmitWithoutReload(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();

    if (validateSubmission(draftText)) {
      setLastSubmissionTime(Date.now());
      handleSubmit();
    }
  }

  return (
    <div className="bg-white p-4 h-96 w-full rounded-lg shadow-lg flex flex-col">
      <div className="flex-[9] bg-gray-100 p-2 overflow-y-auto">
        {submissions.map((submission, index) => (
          <div key={index} className="bg-white p-4 my-3 rounded-lg shadow-lg">
            {submission.timestamp ? <p className="py-1 px-2 bg-gray-500 text-white inline rounded">{submission.timestamp}</p> : <></>}
            {submission.score ? <p className="py-1 px-2 mx-2 bg-orange-400 text-white font-bold inline rounded">スコア: {submission.score}</p> : <></>}
            <p className="pt-2">{submission.content}</p>
          </div>
        ))}
      </div>
      <div className="flex-[1] bg-gray-200 p-2">
        <form className="flex flex-col space-y-2 mx-1" onSubmit={handleSubmitWithoutReload}>
          <div className="flex items-center space-x-1">
            <input
              type="text"
              value={draftText || ""}
              onChange={(e) => {
                setDraftText(e.target.value);
                validateSubmission(e.target.value);
              }}
              placeholder="英語で説明してみよう！"
              className="p-2 flex-1 border border-gray-300 rounded-l-xl"
            />
            <button type="submit" className={`p-2 text-white rounded-r-xl transition-colors ${coolDownRemaining > 0 ? "bg-gray-400 cursor-not-allowed" : "bg-blue-500 hover:bg-blue-600"}`} disabled={coolDownRemaining > 0}>
              {coolDownRemaining > 0 ? `${coolDownRemaining}秒待機中...` : "とりあえず提出してみる"}
            </button>
          </div>
          {errorMessage && <div className="text-red-500 text-sm font-bold px-2">{errorMessage}</div>}
        </form>
      </div>
    </div>
  );
};

function ChallengeImageCard({ imageUrl }: { imageUrl: string }) {
  return <div className="bg-white p-4 h-full w-full rounded-lg shadow-lg bg-cover bg-center" style={{ backgroundImage: `url(${imageUrl})` }}></div>;
}

function GeneratedImageCard({ generatedImageUrl }: { generatedImageUrl: string }) {
  return <div className="bg-white p-4 h-full w-full rounded-lg shadow-lg bg-cover bg-center" style={{ backgroundImage: `url(${generatedImageUrl})` }}></div>;
}

function ScoreCard({ currentScore }: { currentScore: number }) {
  return (
    <div className="bg-white p-4 w-full rounded-lg shadow-lg">
      <p className="pt-2 pb-4">
        スコアが
        <span className="mx-1 px-2 rounded text-white bg-red-500 font-bold">50</span>
        <span className="px-2 rounded text-white bg-orange-500 font-bold">75</span>
        <span className="mx-1 px-2 rounded text-white bg-green-500 font-bold">90</span>
        を超えたときにAIが画像を作ってくれます！
      </p>
      <CircularProgressBar maxValue={100} currentValue={currentScore} size={280} />
    </div>
  );
}
